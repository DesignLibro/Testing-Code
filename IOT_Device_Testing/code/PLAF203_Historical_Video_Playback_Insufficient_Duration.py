# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:44
@File         : PLAF203_Historical_Video_Playback_Insufficient_Duration.py
@Interpreter Version: python 3.12
@Description:
'''

import io
import time
import re
import subprocess
from datetime import datetime
from loguru import logger
from appium import webdriver
from PIL import Image


class NoHistoryPlayAF203(object):
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
            'appium:waitForIdleTimeout': 1000,
            'keep_live': True  # 使手机屏幕维持常亮的状态
        }

        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

        self.adb_command = 'adb shell dumpsys power | grep "mScreenOn=true"'

    def brightScreenAndBreathingScreen(self):
        adb_cmd = 'adb shell input keyevent 26'
        subprocess.run(adb_cmd, shell=True)  # 执行 ADB 命令

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    def getHistoryPlayScreenshotSuccess(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次PLAF203查看历史视频 SUCCESS.png')
        logger.info('PLAF203查看历史视频时长满足预期的APP截图保存')

    def getHistoryPlayScreenshotFail(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次PLAF203查看历史视频 FAIL.png')
        logger.info('PLAF203查看历史视频时长不满足预期的APP截图保存')

    def getHistoryPlay(self, count):
        for i in range(2):
            if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                logger.info('step1：当前APP处于设备首页')
                break
            else:
                logger.error('step1：当前APP未处于设备首页')
                self.swipeDown()

        time.sleep(2)
        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step2：点击设备卡片')

        time.sleep(3)
        if 'Schedule' in self.driver.page_source:
            logger.info('step3：当前APP处于设备面板')
            time.sleep(2)
            self.driver.tap([(0.6630 * self.width, 0.5390 * self.height)], duration=1)  #点击实时流窗口的“回放”按钮
            for i in range(30):
                screenshot = self.driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot))
                rgb1 = image.getpixel((0.0361 * self.width, 0.1161 * self.height))
                rgb2 = image.getpixel((0.9472 * self.width, 0.1296 * self.height))
                rgb3 = image.getpixel((0.0796 * self.width, 0.2726 * self.height))
                rgb4 = image.getpixel((0.8861 * self.width, 0.2726 * self.height))
                confidents = [
                    rgb1[0] == 0,  # 实时流左上角的像素点RGB值
                    rgb1[1] == 0,
                    rgb1[2] == 0,

                    rgb2[0] == 0,  # 实时流右上角的像素点RGB值
                    rgb2[1] == 0,
                    rgb2[2] == 0,

                    rgb3[0] == 0,  # 实时流左下角的像素点RGB值
                    rgb3[1] == 0,
                    rgb3[2] == 0,

                    rgb4[0] == 0,  # 实时流右下角的像素点RGB值
                    rgb4[1] == 0,
                    rgb4[2] == 0,
                ]
                if all(confidents):
                    time.sleep(1)
                else:
                    self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                    logger.info('step4：设备查看回放成功！')
                    result = re.findall('<android.view.View index="6" package="com.designlibro.petlibro" class="android.view.View" text="" content-desc="(.*?)"', self.driver.page_source)
                    time_obj = datetime.strptime(result[0], '%M:%S')  # 使用 datetime.strptime() 解析时间字符串
                    seconds = time_obj.minute * 60 + time_obj.second
                    logger.info(f'该历史视频时长为{seconds} S')
                    for i in range(seconds):  # 循环监控历史视频有没有播放完（拿播放滚珠的RGB）
                        screenshot = self.driver.get_screenshot_as_png()
                        image = Image.open(io.BytesIO(screenshot))
                        rgb5 = image.getpixel((0.8342 * self.width, 0.3232 * self.height))
                        confidents = [
                            rgb5[0] == 219,
                            rgb5[1] == 192,
                            rgb5[2] == 165,
                        ]
                        self.driver.tap([(0.4907 * self.width, 0.2610 * self.height)], duration=1)  # 点击回放流窗口的任意位置
                        if all(confidents):
                            logger.info('该历史视频播放完全！')
                            self.getHistoryPlayScreenshotSuccess(count);time.sleep(3)
                            self.driver.tap([(0.1259 * self.width, 0.6902 * self.height)], duration=1)  # 点击回放流窗口的任意位置
                            logger.info('点击"上一个"历史视频按钮')
                            count += 1
                            break
                        else:
                            time.sleep(1)
                    else:
                        logger.error('该历史视频播放不完全！')
                        self.getHistoryPlayScreenshotFail(count);time.sleep(3)
                        self.driver.tap([(0.1259 * self.width, 0.6902 * self.height)], duration=1)  # 点击回放流窗口的任意位置
                        logger.info('点击"上一个"历史视频按钮')
                        count += 1
            else:
                count += 1
                logger.error('step4：设备回放出流超过30S失败！')
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.getHistoryPlayScreenshotFail(count)
                time.sleep(2)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--AF203历史视频播放时长不足预期压测.log', rotation='100MB', encoding='utf-8', enqueue=True)
        count = 1
        self.getHistoryPlay(count)
        time.sleep(self.intervalTime)


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：---- ').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)---- ').strip()
    testTimes = 10000
    intervalTime = 2
    logger.info('开始执行PLAF203历史视频播放时长不足预期专项自动化测试...')
    # try:
    #     noHistoryPlayAF203 = NoHistoryPlayAF203(testTimes, intervalTime)
    #     noHistoryPlayAF203.main()
    # except Exception as error:
    #     logger.info('An exception happened: ' + str(error))
    noHistoryPlayAF203 = NoHistoryPlayAF203(testTimes, intervalTime)
    noHistoryPlayAF203.main()

