# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:46
@File         : PLAF107_Reconnect_Wifi.py
@Interpreter Version: python 3.12
@Description:
'''

import time
import os
import uiautomator2 as u2
from loguru import logger
from appium import webdriver
from config.config_controlScreen import ControlScreen
from ppadb.client import Client as AdbClient


class ReconnectWIFI(object):
    def __init__(self, testTimes, restScreenTime, intervalTime=30):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            'platformName': 'Android',  # 固定值Android
            'platformVersion': '10',  # 系统版本号（在关于手机中查看）
            'deviceName': 'Galaxy S9',  # 手机型号
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
            'appium:waitForIdleTimeout': 1000,
            'skipServerInstallation': True,
            'skipDeviceInitialization': True
        }
        self.testTimes = int(testTimes)
        self.intervalTime = intervalTime
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        self.restScreenTime = restScreenTime
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004
        self.d = u2.connect_usb(self.desired_capabilities['udid'])  # 使用usb线的方式连接测试手机
        # self.d = u2.connect('192.168.1.100:7912') # 使用WIFI的方式连接测试手机
        # self.d.debug = False # 关闭调试开关
        # ControlScreen().__init__()

    def appHandle(self):
        time.sleep(5)
        self.driver.tap([(0.3 * self.width, 0.475 * self.height)], duration=1)  # 尝试多次用id和xpath的方式都无法捕获元素，因此采用相对坐标
        logger.info('step 1: 点击"首页设备卡片"入口')
        time.sleep(3)

        self.driver.tap([(0.9111 * self.width, 0.0843 * self.height)], duration=1)
        logger.info('step 2: 点击"设置"按钮')
        time.sleep(3)

        self.swipeUp()
        time.sleep(3)

        self.driver.tap([(0.5555 * self.width, 0.5934 * self.height)], duration=1)
        logger.info('step 3: 点击"WIFI Settings"入口')
        time.sleep(3)

    def reconnectWIFI(self, count):
        self.driver.tap([(0.4870 * self.width, 0.6647 * self.height)], duration=1)
        logger.info('step 4: 点击"RECONNECT THE CURRENT WIFI"按钮')

        time.sleep(self.intervalTime)

        self.reconnectWIFIScreenshot(count)
        time.sleep(3)

        self.closeScreen()
        time.sleep(self.intervalTime)

        self.openScreen()
        time.sleep(self.intervalTime)

        self.swipeScreen()
        time.sleep(6)

        self.driver.tap([(0.5139 * self.width, 0.8767 * self.height)], duration=1)
        logger.info('step 5: 点击"CONFIRM"按钮')
        time.sleep(3)

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeUp(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 1000)
        logger.info('正在向下滑动至"WIFI Settings"入口...')

    def swipeScreen(self):
        x1 = int(0.5231 * self.width)
        y1 = int(0.9827 * self.height)
        y2 = int(0.1349 * self.height)
        self.d.swipe(x1, y1, x1, y2, duration=0.1)
        logger.info('正在上滑解锁屏幕...')

    def closeScreen(self):
        self.d.screen_off()
        logger.info('关闭屏幕')

    def openScreen(self):
        self.d.screen_on()
        logger.info('打开屏幕')

    def reconnectWIFIScreenshot(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次重连WIFI.png')
        logger.info('APP截图保存')

    def main(self):
        logger.add(rf'../log/{self.logFilename}--重连WIFI专项测试.log', rotation='50MB', encoding='utf-8', enqueue=True)
        self.appHandle()
        for count in range(1, self.testTimes + 1):
            try:
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.reconnectWIFI(count)
                logger.info(f'执行第 {count} 次重连WIFI SUCCESS')
            except:
                logger.info(f'执行第 {count} 次重连WIFI FAIL')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试重连WIFI的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info(f'PLAF107重连WIFI专项自动化测试结束！')


if __name__ == '__main__':
    testTimes = input('请输入测试次数：----').strip()
    intervalTime = int(input('请输入每次重连WIFI的等待时间：(单位：S，不低于30S)----').strip())
    restScreenTime = input('请输入手机屏幕息屏时间：(单位：S，不低于600S)----').strip()
    logger.info('开始执行PLAF107重连WIFI专项自动化测试...')
    # try:
    #     reconnectWIFI = ReconnectWIFI(testTimes, restScreenTime, intervalTime)
    #     reconnectWIFI.main()
    # except Exception as error:
    #     logger.info('An exception happened: \n' + str(error))
    reconnectWIFI = ReconnectWIFI(testTimes, restScreenTime, intervalTime)
    reconnectWIFI.main()
