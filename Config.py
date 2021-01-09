# -*- coding: utf-8 -*-


class MonkeyConfig(object):
    # 测试的app包名
    package_name = "com.example.myapplication"

    # 测试app中模块的关键词
    module_key = "com.example.myapplication.MainActivity"

    # todo 自动找到apk中exported的activity
    # 卡死状态随机跳转的activity,第一个元素为测试初始页
    activity = [
                "com.example.myapplication.LoginActivity",
                "com.example.myapplication.MainActivity"

               ]

    monkeyCmd = f"monkey -p {package_name} --throttle 300  " \
                "--pct-appswitch 5 --pct-touch 30 --pct-motion 60 --pct-anyevent 5  " \
                "--ignore-timeouts --ignore-crashes   --monitor-native-crashes -v -v -v 5 > "
