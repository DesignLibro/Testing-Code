# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:37
@File         : PLAF103_Schedule_Feed.py
@Interpreter Version: python 3.12
@Description:
'''

import time
import random
from loguru import logger
from appium import webdriver


class ScheduleFeeding(object):
    def __init__(self, testTimes, intervalTime):
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
            'appium:waitForIdleTimeout': 1000
        }
        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

    def appHandle(self):
        time.sleep(8)
        self.driver.tap([(0.3 * self.width, 0.475 * self.height)], duration=1)  # 尝试多次用id和xpath的方式都无法捕获元素，因此采用相对坐标
        logger.info('step 1: 点击"首页设备卡片"入口')
        time.sleep(3)

        self.beforeFeedingScreenshot()
        time.sleep(2)

        self.driver.tap([(0.5037 * self.width, 0.923 * self.height)], duration=1)
        logger.info('step 2: 点击"Schedule"入口')
        time.sleep(3)

    def addSchedule(self):
        self.driver.tap([(0.5093 * self.width, 0.8560 * self.height)], duration=1)
        logger.info('step 3: 点击"ADD A FEEDING PLAN"按钮')
        time.sleep(3)

        if self.getCurrentMin() == 59:
            self.swipeUpHour()
            time.sleep(2)
            self.swipeUpMin()
            time.sleep(2)
        else:
            self.swipeUpMin()
            time.sleep(2)

        self.swipeBottom()
        time.sleep(2)

        self.driver.tap([(0.5139 * self.width, 0.8733 * self.height)], duration=1)
        logger.info('step 4: 点击"SAVE"按钮')
        time.sleep(self.intervalTime * 1.8)

    def deleteSchedule(self):
        self.driver.tap([(0.4824 * self.width, 0.3640 * self.height)], duration=1)
        logger.info('step 5: 点击第一个计划')
        time.sleep(2)

        self.driver.tap([(0.8917 * self.width, 0.0788 * self.height)], duration=1)
        logger.info('step 6: 点击"Delete"按钮')
        time.sleep(2)

        self.driver.tap([(0.5185 * self.width, 0.5405 * self.height)], duration=1)
        logger.info('step 7: 点击"Yes"按钮')
        time.sleep(2)

    def feedingScreenshot(self, count):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--第{count}次最小单位计划喂食.png')
        logger.info('APP截图保存')

    def beforeFeedingScreenshot(self):
        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--执行最小单位计划喂食测试前截图.png')
        logger.info(f'执行最小单位计划喂食测试前APP截图保存')

    def afterFeedingScreenshot(self):
        self.driver.tap([(0.0870 * self.width, 0.0862 * self.height)], duration=1)
        logger.info('step 8: 点击"返回"按钮')
        time.sleep(3)

        logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.driver.get_screenshot_as_file(rf'../result/{logFilename}--执行最小单位计划喂食测试完截图.png')
        logger.info(f'执行最小单位计划喂食测试完APP截图保存')

    def getCurrentMin(self):
        currentMin = time.localtime().tm_min
        return currentMin

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeUpHour(self):
        x1 = int(0.4518 * self.width)
        y1 = int(0.4306 * self.height)
        y2 = int(0.3673 * self.height)
        self.swipe(x1, y1, x1, y2, 1000)
        logger.info('正在向下滑动时钟数加1...')

    def swipeUpMin(self):
        x1 = int(0.5935 * self.width)
        y1 = int(0.4306 * self.height)
        y2 = int(0.3673 * self.height)
        self.swipe(x1, y1, x1, y2, 1000)
        logger.info('正在向下滑动分钟数加1...')

    def swipeBottom(self):
        x1 = int(0.8056 * self.width)
        y1 = int(0.8603 * self.height)
        y2 = int(0.2673 * self.height)
        self.swipe(x1, y1, x1, y2, 1000)
        logger.info('正在向下滑动到屏幕底部...')

    def main(self):
        logger.add(rf'../log/{self.logFilename}--最小单位计划喂食专项测试.log', rotation='50MB', encoding='utf-8',
                   enqueue=True)
        self.appHandle()
        for count in range(1, self.testTimes + 1):
            try:
                self.addSchedule()
                logger.info(f'执行第 {count} 次最小单位计划喂食 SUCCESS')
                self.deleteSchedule()
            except:
                logger.info(f'执行第 {count} 次最小单位计划喂食 FAIL')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试最小单位计划喂食的次数为：{remainingTimes}')
            if count == self.testTimes:
                self.afterFeedingScreenshot()
                logger.info(f'PLAF103最小单位计划喂食专项自动化测试结束！')


if __name__ == '__main__':
    testTimes = input('请输入测试次数：----').strip()
    intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)----').strip()
    logger.info('开始执行PLAF103计划喂食专项自动化测试...')
    try:
        ScheduleFeedingTest = ScheduleFeeding(testTimes, intervalTime)
        ScheduleFeedingTest.main()
    except Exception as error:
        logger.info('An exception happened: \n' + str(error))
