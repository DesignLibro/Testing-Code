# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:54
@File         : PLAF203_TUTK_Audio_And_Video_Encryption.py
@Interpreter Version: python 3.12
@Description: 1. AttributeError: 'NoneType' object has no attribute 'to_capabilities'
# 解决方法1:
# from appium.options.android import UiAutomator2Options
# options = UiAutomator2Options().load_capabilities(capabilities)
# webdriver.Remote(command_executor=appium_server_url, options=options)
'''

import io
import time
import re
import subprocess
from datetime import datetime
from loguru import logger
from appium import webdriver
from PIL import Image
from appium.options.android import UiAutomator2Options


class RealTimeStreamingAF203(object):
    def __init__(self, testTimes, intervalTime):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            'platformName': 'Android',  # 固定值Android
            'platformVersion': '10',  # 系统版本号（在关于手机中查看）
            'deviceName': 'Galaxy S9',  # 手机型号
            'automationName': 'UiAutomator2',  # 固定值UiAutomator2
            'appPackage': 'com.designlibro.petlibro', # 在cmd窗口中敲adb shell dumpsys activity recents |find "intent={"命令获取包名和Activity名称
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
        self.options = UiAutomator2Options().load_capabilities(self.desired_capabilities)
        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)
        self.driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', options=self.options)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

    def getRealTimeStreamingScreenshotSuccess(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次PLAF203出流 Success.png')
        logger.info('PLAF203出流成功的APP截图保存')

    def getRealTimeStreamingScreenshotFail(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次PLAF203出流 FAIL.png')
        logger.info('PLAF203出流超时或失败的APP截图保存')

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    def getRealTimeStreaming(self, count):
        for i in range(2):
            if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                logger.info('step1：当前APP处于设备首页')
                break
            else:
                logger.error('step1：当前APP未处于设备首页')
                self.swipeDown()

        time.sleep(2)
        start_time = time.time()
        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step2：点击设备卡片')

        time.sleep(3)
        if 'Schedule' in self.driver.page_source:
            logger.info('step3：当前APP处于设备面板')
            for i in range(20):
                screenshot = self.driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot))
                rgb1 = image.getpixel((0.1194 * self.width, 0.2076 * self.height))
                rgb2 = image.getpixel((0.9324 * self.width, 0.2634 * self.height))
                rgb3 = image.getpixel((0.2259 * self.width, 0.4219 * self.height))
                rgb4 = image.getpixel((0.7777 * self.width, 0.4176 * self.height))
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
                    time.sleep(1.2)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f'设备出流耗时：---- {elapsed_time - 3:.2f} 秒')  # 需要减少3秒的等待时间
                    self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                    self.getRealTimeStreamingScreenshotSuccess(count)
                    logger.info('step4：设备出流成功！')
                    break
            else:
                logger.error('step4：设备出流超过20S失败！')
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.getRealTimeStreamingScreenshotFail(count)
                time.sleep(2)
                if 'Failed to load with network exception' in self.driver.page_source:
                    time.sleep(2)
                    self.driver.tap([(0.8101 * self.width, 0.3227 * self.height)], duration=1)
                    logger.info('step5：在实时流窗口中点击Reload按钮')
                    for i in range(10):
                        screenshot = self.driver.get_screenshot_as_png()
                        image = Image.open(io.BytesIO(screenshot))
                        rgb1 = image.getpixel((0.0537 * self.width, 0.2076 * self.height))
                        rgb2 = image.getpixel((0.9064 * self.width, 0.2100 * self.height))
                        rgb3 = image.getpixel((0.0796 * self.width, 0.3983 * self.height))
                        rgb4 = image.getpixel((0.9018 * self.width, 0.3959 * self.height))
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
                            logger.info('step6：设备重试出流成功！')
                            break
                    else:
                        logger.error('step6：设备重试出流超过10S失败！')
                        self.getRealTimeStreamingScreenshotFail(count)
        time.sleep(3)
        self.driver.tap([(0.0824 * self.width, 0.0621 * self.height)], duration=1)
        logger.info('step5：点击左上角的返回按钮')

        for i in range(2):
            if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                logger.info('step6：当前APP处于设备首页')
                break
            else:
                logger.error('step6：当前APP未处于设备首页')
                self.swipeDown()

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203出流专项测试.log', rotation='100MB', encoding='utf-8',
                   enqueue=True)
        for count in range(1, self.testTimes + 1):
            try:
                # self.getRealTimeStreaming(count)
                # logger.info(f'执行第 {count} 次PLAF203出流完成')
                # result = subprocess.getoutput(self.adb_command)
                # if 'mScreenOn=true' in result:
                #     logger.info('手机亮屏')
                # else:
                #     time.sleep(2)
                #     self.brightScreenAndBreathingScreen()
                #     result = subprocess.getoutput(self.adb_command)
                #     if 'mScreenOn=true' not in result:
                #         logger.info('手机息屏')
                #     time.sleep(2)
                #     self.brightScreenAndBreathingScreen()
                #     result = subprocess.getoutput(self.adb_command)
                #     if 'mScreenOn=true' in result:
                #         logger.info('手机亮屏')
                # time.sleep(self.intervalTime)

                self.getRealTimeStreaming(count)
                logger.info(f'执行第 {count} 次PLAF203出流完成')
                time.sleep(self.intervalTime)

            except:
                logger.error(f'执行第 {count} 次PLAF203出流出现异常')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203出流的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info('PLAF203出流专项自动化测试结束！')


if __name__ == '__main__':
    testTimes = 999999999999999
    intervalTime = 60
    logger.info('开始执行脚本...')
    realTimeStreamingAF203 = RealTimeStreamingAF203(testTimes, intervalTime)
    realTimeStreamingAF203.main()