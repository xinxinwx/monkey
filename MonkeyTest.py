# -*- coding: utf-8 -*-
import datetime
import os
import random
import time
import platform
import AdbCommon
import Config
from multiprocessing import Pool
from typing import Dict, Union
from AdbCommon import AndroidDebugBridge
from sendEmail import SendEmail


adb = AdbCommon.AndroidDebugBridge()
monkeyConfig = Config.MonkeyConfig()

monkeyLogFile="log/monkey.Log"
logFileName="log/logcat.Log"
traceFilename="log/anr_traces.log"

def runnerPool():
    devices_Pool = []
    # 检查设备
    devices = adb.attached_devices()
    if devices:
        for item in range(0, len(devices)):
            _app: Dict[str, Union[str, int]] = {"devices": devices[item], "num": len(devices)}
            devices_Pool.append(_app)
        pool = Pool(len(devices))
        pool.map(start, devices_Pool)
        pool.close()
        pool.join()

        #读取logcat日志  获取crash数量  大于0发送邮件
        with open(logFileName, "r", encoding='utf-8') as f:
            data = f.read()
            crash=data.count('Caused by')
            if crash > 0:
                SendEmail().send_main(crash)

    else:
        print("设备不存在?")


def start(devices):
    device = devices["devices"]
    deviceNum = devices["num"]
    print(f"start device {device};num {deviceNum}")

    # 打开想要的activity
    adb.open_app(monkeyConfig.package_name, monkeyConfig.activity[0], device)

    monkeyConfig.monkeyCmd = f"adb -s {device} shell {monkeyConfig.monkeyCmd + (monkeyLogFile)}"


    # 开始测试
    start_monkey(monkeyConfig.monkeyCmd)

    # 启动activty的时间
    start_activity_time = time.time()

    while True:
        # 判断测试的app的module是否在top
        if AndroidDebugBridge().isOnTop(monkeyConfig.package_name,monkeyConfig.module_key) is False:
            # 如果不在则选择第一个
            adb.open_app(monkeyConfig.package_name, monkeyConfig.activity[0],
                         device)

        #获取当前页面的activity
        currentActivity = AndroidDebugBridge().getCurrentAty()
        time.sleep(2)


        # 判断测试app是否在某个页面停留过久，防止测试卡死
        if AndroidDebugBridge().isStopHow(start_activity_time, currentActivity, 5):
            adb.open_app(monkeyConfig.package_name,
                         random.choice(monkeyConfig.activity), device)
            start_activity_time = time.time()

        #执行完成终止死循环
        with open(monkeyLogFile, "r", encoding='utf-8') as monkeyLog:
            if monkeyLog.read().count('Monkey finished') > 0:
                print(f"{device}\n测试完成咯")
                break




# 开始脚本测试
def start_monkey(monkeyCmd):

    #执行monkey 的命令
    os.popen(monkeyCmd)
    print(f"start_monkey {monkeyCmd}")

    #导出crash文件   用于分析crash
    cmd2 = f"adb logcat -c && adb logcat >{logFileName}"
    os.popen(cmd2)


    # "导出traces文件 用于分析ANR"
    cmd3 = f"adb shell cat /data/anr/traces.txt>{traceFilename}"
    os.popen(cmd3)


def killPort():
    os.popen("adb kill-server")
    os.popen("adb start-server")
    os.popen("adb root")


if __name__ == '__main__':
    print(f"当前操作系统 {platform.system()}")
    killPort()
    time.sleep(1)
    runnerPool()
