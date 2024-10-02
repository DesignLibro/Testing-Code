# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:39
@File         : PLAF103_Manual_Feed.py
@Interpreter Version: python 3.12
@Description: 1.将python的第三方库appium-python-client安装版本为1.3.0，其中selenium为依赖，不用单独安装；
                 2.需要将测试手机的自动息屏功能关闭；
                 3.让设备在最小单位下手动喂食1次，方便后面支持最小、最大单位模式；
                 4.重置设备，让今日喂食次数清零；
                 5.执行最小单位时，测试时间间隔>30S；执行最大单位测试时，测试时间间隔>510S；执行随机单位测试时，测试时间间隔>510S；
'''

import time
import random
from loguru import logger
from appium import webdriver


class ManualFeeding(object):
    def __init__(self, testTimes, intervalTime, manualFeedingMode):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            'platformName': 'Android',  # 固定值Android
            'platformVersion': '13',  # 系统版本号（在关于手机中查看）
            # 'deviceName': 'Galaxy S9',  # 手机型号
            'automationName': 'UiAutomator2',  # 固定值UiAutomator2
            'appPackage': 'com.designlibro.petlibro',
            # 在cmd窗口中敲adb shell dumpsys activity recents |find "intent={"命令获取包名和Activity名称
            'appActivity': '.MainActivity',
            'udid': '10AD1B02QN000Y9',  # 在cmd窗口中敲adb devices获取
            'autoLaunch': True,  # 在手机中启动appium服务，但不开启界面
            'noReset': True,  # 不要重置APP
            'fullReset': False,
            'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填写True
            'resetKeyboard': True,  # 执行完程序恢复原来的输入法
            'appium:newCommandTimeout': 360000,
            'appium:waitForSelectorTimeout': 1000,
            'appium:waitForIdleTimeout': 1000
        }
        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)
        self.manualFeedingMode = manualFeedingMode
        if self.manualFeedingMode == 0:
            self.mode = '最小'
        elif self.manualFeedingMode == 1:
            self.mode = '最大'
        elif self.manualFeedingMode == 2:
            self.mode = '随机'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

    def appHandle(self):
        time.sleep(5)
        self.driver.tap([(0.3 * self.width, 0.475 * self.height)], duration=1)  # 尝试多次用id和xpath的方式都无法捕获元素，因此采用相对坐标
        logger.info('step 1: 点击"首页设备卡片"入口')
        time.sleep(3)

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeLeft(self):
        x1 = int(self.width * 0.7917)
        y1 = int(self.height * 0.7794)
        x2 = int(self.width * 0.2314)
        self.swipe(x1, y1, x2, y1, 1000)
        logger.info('正在向左最大滑动屏幕...')

    def swipeRight(self):
        x1 = int(self.width * 0.2314)
        y1 = int(self.height * 0.7794)
        x2 = int(self.width * 0.7917)
        self.swipe(x1, y1, x2, y1, 1000)
        logger.info('正在向右最大滑动屏幕...')

    def swipeRandom(self):
        num = random.randint(0, 47)
        logger.info(f'循环点击“+”按钮的次数为：{num}')
        logger.info(f'实际出粮份数为：{num + 1}')
        if num < 5:
            for i in range(1, num + 1):
                self.driver.tap([(0.8917 * self.width, 0.7726 * self.height)], duration=1)
                logger.info(f'正在单击“+”按钮 第{i + 1}次...')
            else:
                self.driver.tap([(0.516 * self.width, 0.884 * self.height)], duration=1)
                logger.info('step 3: 点击"Feed now"按钮')
                time.sleep(3)

        elif num >= 5:
            for i in range(num):
                self.driver.tap([(0.8917 * self.width, 0.7726 * self.height)], duration=1)
                logger.info(f'正在单击“+”按钮 第{i + 1}次...')

            else:
                self.driver.tap([(0.516 * self.width, 0.884 * self.height)], duration=1)
                logger.info('step 3: 点击"Feed now"按钮')
                time.sleep(3)

                self.driver.tap([(0.4880 * self.width, 0.5770 * self.height)], duration=1)
                logger.info('step 4: 点击"Yes"按钮')

    def feedingScreenshot(self, count):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--第{count}次{self.mode}单位手动喂食.png')
        logger.info('APP截图保存')

    def beforeFeedingScreenshot(self):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--执行{self.mode}单位手动喂食测试前截图.png')
        logger.info(f'执行{self.mode}单位手动喂食测试前APP截图保存')

    def afterFeedingScreenshot(self):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--执行{self.mode}单位手动喂食测试完截图.png')
        logger.info(f'执行{self.mode}单位喂食测试完APP截图保存')

    def minManualFeeding(self):
        # 如果后台部署了建议升级，需要在升级弹框中点击Cancel按钮
        # self.driver.tap([(0.5111 * self.width, 0.6821 * self.height)], duration=1)
        # logger.info('点击"OTA Cancel"按钮')
        # time.sleep(2)

        self.driver.tap([(0.2842 * self.width, 0.9296 * self.height)], duration=1)
        logger.info('step 2: 点击"Feed now"入口')
        time.sleep(2)

        self.driver.tap([(0.5064 * self.width, 0.8877 * self.height)], duration=1)
        logger.info('step 3: 点击"Feed now"按钮')
        time.sleep(2)

    def maxManualFeeding(self):
        self.driver.tap([(0.209 * self.width, 0.923 * self.height)], duration=1)
        logger.info('step 2: 点击"Feed now"入口')
        time.sleep(2)

        self.swipeLeft()
        time.sleep(2)

        self.swipeRight()
        time.sleep(3)

        self.driver.tap([(0.516 * self.width, 0.884 * self.height)], duration=1)
        logger.info('step 3: 点击"Feed now"按钮')
        time.sleep(3)

        self.driver.tap([(0.4880 * self.width, 0.5770 * self.height)], duration=1)
        logger.info('step 4: 点击"Yes"按钮')
        time.sleep(2)

    def randomManualFeeding(self):
        self.driver.tap([(0.209 * self.width, 0.923 * self.height)], duration=1)
        logger.info('step 2: 点击"Feed now"入口')
        time.sleep(2)

        self.swipeLeft()
        time.sleep(2)

        self.swipeRandom()
        time.sleep(2)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--{self.mode}单位手动喂食专项测试.log', rotation='50MB',
                   encoding='utf-8', enqueue=True)
        if self.manualFeedingMode == 0:
            self.appHandle()
            self.beforeFeedingScreenshot()
            for count in range(1, self.testTimes + 1):
                try:
                    self.minManualFeeding()
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 SUCCESS')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                except:
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 FAIL')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                remainingTimes = self.testTimes - count
                logger.info(f'剩余测试{self.mode}单位手动喂食次数为：{remainingTimes}')
                if count == self.testTimes:
                    self.afterFeedingScreenshot()
                    logger.info(f'PLAF103{self.mode}单位手动喂食专项自动化测试结束！')

        elif self.manualFeedingMode == 1:
            self.appHandle()
            self.beforeFeedingScreenshot()
            for count in range(1, self.testTimes + 1):
                try:
                    self.maxManualFeeding()
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 SUCCESS')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                except:
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 FAIL')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                remainingTimes = self.testTimes - count
                logger.info(f'剩余测试{self.mode}单位手动喂食次数为：{remainingTimes}')
                if count == self.testTimes:
                    self.afterFeedingScreenshot()
                    logger.info(f'PLAF103{self.mode}单位手动喂食专项自动化测试结束！')

        elif self.manualFeedingMode == 2:
            self.appHandle()
            self.beforeFeedingScreenshot()
            for count in range(1, self.testTimes + 1):
                try:
                    self.randomManualFeeding()
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 SUCCESS')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                except:
                    logger.info(f'执行第 {count} 次{self.mode}单位手动喂食 FAIL')
                    time.sleep(self.intervalTime)
                    self.feedingScreenshot(count)
                remainingTimes = self.testTimes - count
                logger.info(f'剩余测试{self.mode}单位手动喂食次数为：{remainingTimes}')
                if count == self.testTimes:
                    self.afterFeedingScreenshot()
                    logger.info(f'PLAF103{self.mode}单位手动喂食专项自动化测试结束！')


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：----').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)----').strip()
    # manualFeedingMode = input('请输入喂食单位定量模式：(0 最小、1 最大、2 随机)----').strip()
    testTimes = 1000000000
    intervalTime = 15
    manualFeedingMode = 0
    logger.info('开始执行PLAF103手动喂食专项自动化测试...')
    # try:
    #     manualFeedingTest = ManualFeeding(testTimes, intervalTime, manualFeedingMode)
    #     manualFeedingTest.main()
    # except Exception as error:
    #     logger.info('An exception happened: \n' + str(error))
    manualFeedingTest = ManualFeeding(testTimes, intervalTime, manualFeedingMode)
    manualFeedingTest.main()
