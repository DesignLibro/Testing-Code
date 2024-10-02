# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:45
@File         : PLAF107_Manual_Vacuuming.py
@Interpreter Version: python 3.12
@Description: 1.最新的APP版本分为3种模式：喂食结束抽、喂食结束后隔5min抽、手动抽真空，为了跑这个专项，需要在抽真空完成后，下发手动喂食，把里面的真空放走，才能跑下一轮；
'''

import time
from loguru import logger
from appium import webdriver


class ManualVacuum(object):
    def __init__(self, testTimes, intervalTime, manualFeedingMode):
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
        self.manualFeedingMode = manualFeedingMode
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

    def test(self):
        time.sleep(5)
        self.driver.tap([(0.3 * self.width, 0.475 * self.height)], duration=1)  # 尝试多次用id和xpath的方式都无法捕获元素，因此采用相对坐标
        logger.info('step 1: 点击"首页设备卡片"入口')
        time.sleep(3)

    def handleFeed(self):
        ManualFeeding(self.testTimes, self.intervalTime, self.manualFeedingMode).main()

    def handleVacuum(self):
        self.driver.tap([(0.6102 * self.width, 0.9510 * self.height)], duration=1)
        logger.info('step 2: 点击"抽真空"按钮')
        time.sleep(2)

        self.driver.tap([(0.5102 * self.width, 0.6802 * self.height)], duration=1)
        logger.info('step 3: 点击"手动抽真空"按钮')
        time.sleep(2)

        self.driver.tap([(0.4972 * self.width, 0.8560 * self.height)], duration=1)
        logger.info('step 4: 点击"确认"按钮')
        time.sleep(2)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF107 手动抽真空专项测试.log', rotation='50MB', encoding='utf-8',
                   enqueue=True)
        # self.test()
        for count in range(1, self.testTimes + 1):
            try:
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.handleFeed()
                time.sleep(self.intervalTime)
                self.handleVacuum()
                logger.info(f'执行第 {count} 次手动抽真空 SUCCESS')
                time.sleep(self.intervalTime)
            except:
                logger.info(f'执行第 {count} 次手动抽真空 FAIL')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试手动抽真空的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info(f'PLAF107 手动抽真空专项自动化测试结束！')


if __name__ == '__main__':
    testTimes = input('请输入测试次数：----').strip()
    intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于240S)----').strip()
    manualFeedingMode = input('请输入喂食单位定量模式：(0 最小、1 最大、2 随机)----').strip()

    logger.info('开始执行PLAF107 手动抽真空专项自动化测试...')
    try:
        reconnectWIFI = ManualVacuum(testTimes, intervalTime, manualFeedingMode)
        reconnectWIFI.main()
    except Exception as error:
        logger.info('An exception happened: \n' + str(error))
