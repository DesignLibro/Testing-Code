# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:49
@File         : Oscilloscope_Monitoring.py
@Interpreter Version: python 3.12
@Description:
'''

import requests
import json
import time
from loguru import logger
from appium import webdriver


class AF203ChangeNightVision(object):
    def __init__(self, ):
        self.headers1 = {
            'source': 'ANDROID',
            'language': 'ZH',
            'timezone': 'Asia/Shanghai',
            'version': '1.2.20',
            'accept-encoding': 'gzip',
            'content-length': '407',
            'host': 'test-api.dl-aiot.com',
            'content-type': 'application/json;charset=utf-8',
            'token': '2ebc2e16ac5340ba8a8b6bee62335eff',
        }
        self.url = 'https://test-api.dl-aiot.com/device/setting/updateCameraSetting'

        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            'platformName': 'Android',  # 固定值Android
            'platformVersion': '10',  # 系统版本号（在关于手机中查看）
            # 'deviceName': 'Galaxy S9',  # 手机型号
            'automationName': 'UiAutomator2',  # 固定值UiAutomator2
            'appPackage': 'com.designlibro.petlibro',
            # 在cmd窗口中敲adb shell dumpsys activity recents |find "intent={"命令获取包名和Activity名称
            'appActivity': '.MainActivity',
            'udid': '3637513754573398',  # 在cmd窗口中敲adb devices获取
            'autoLaunch': True,  # 在手机中启动appium服务，但不开启界面
            'noReset': True,  # 不要重置APP
            'fullReset': False,
            'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填写True
            'resetKeyboard': True,  # 执行完程序恢复原来的输入法
            'appium:newCommandTimeout': 360000,
            'appium:waitForSelectorTimeout': 1000,
            'appium:waitForIdleTimeout': 1000
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率

        time.sleep(8)

    def nightVisionOpen(self):
        parameter1 = {
            'afterManualFeedingTime': 10,
            'automaticRecording': 10,
            'beforeFeedingPlanTime': 1,
            'cameraAgingType': 1,
            'cameraSwitch': True,
            'deviceSn': 'AF0301308CE8731BC',
            'enableVideoAfterManualFeeding': False,
            'enableVideoStartFeedingPlan': False,
            'feedingVideoSwitch': False,
            'nightVision': 'OPEN',
            'resolution': 'P1080',
            'videoRecordAgingType': 1,
            'videoRecordMode': 'CONTINUOUS',
            'videoRecordSwitch': True,
            'videoWatermarkSwitch': True,
        }
        send_requests = requests.post(url=self.url, headers=self.headers1, data=json.dumps(parameter1))
        if send_requests.status_code == 200:
            logger.info('夜视 OPEN')

    def nightVisionClose(self):
        parameter2 = {
            'afterManualFeedingTime': 10,
            'automaticRecording': 10,
            'beforeFeedingPlanTime': 1,
            'cameraAgingType': 1,
            'cameraSwitch': True,
            'deviceSn': 'AF0301308CE8731BC',
            'enableVideoAfterManualFeeding': False,
            'enableVideoStartFeedingPlan': False,
            'feedingVideoSwitch': False,
            'nightVision': 'CLOSE',
            'resolution': 'P1080',
            'videoRecordAgingType': 1,
            'videoRecordMode': 'CONTINUOUS',
            'videoRecordSwitch': True,
            'videoWatermarkSwitch': True,
        }
        send_requests = requests.post(url=self.url, headers=self.headers1, data=json.dumps(parameter2))
        if send_requests.status_code == 200:
            logger.info('夜视  CLOSE')

    def apphandle(self):
        self.driver.tap([(0.4953 * self.width, 0.5852 * self.height)], duration=1)
        logger.info('step1：点击取消升级APP')
        time.sleep(3)

        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step2：点击设备卡片')

    def screenShotOpen(self, count):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result123/{logFilename}--第{count}次夜视 OPEN.png')

    def screenShotClose(self, count):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result123/{logFilename}--第{count}次夜视 CLOSE.png')

    def main(self):
        logger.add(rf'../log/{self.logFilename}--示波器监控.log', rotation='50MB', encoding='utf-8', enqueue=True)
        self.apphandle()
        time.sleep(10)
        count = 1
        while True:
            logger.info(f'执行第{count}次夜视切换')
            # self.nightVisionOpen()
            # time.sleep(5)
            self.screenShotOpen(count)
            count += 1
            time.sleep(15)

            # self.nightVisionClose()
            # time.sleep(5)
            self.screenShotClose(count)
            time.sleep(15)


if __name__ == '__main__':
    aF203ChangeNightVision = AF203ChangeNightVision()
    aF203ChangeNightVision.main()
