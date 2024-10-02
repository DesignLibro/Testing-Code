# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:42
@File         : PLAF203_Historical_Video_Playback.py
@Interpreter Version: python 3.12
@Description:
'''

import io
import time
import subprocess
from loguru import logger
from appium import webdriver
from PIL import Image


class HistoryPlayChangeDateAF203(object):
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
            'udid': '3637513754573398',  # 在cmd窗口中敲adb devices获取（三星手机）
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
        x1 = int(0.7954 * self.width)
        y1 = int(0.7346 * self.height)
        y2 = int(0.7900 * self.height)
        self.swipe(x1, y1, x1, y2, 2000)

    def getHistoryPlayChangeDateScreenshotSuccess(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203查看历史视频切换日期 SUCCESS.png')
        logger.info('PLAF203查看历史视频切换日期成功的APP截图保存')

    def getHistoryPlayChangeDateScreenshotFail(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203查看历史视频切换日期 FAIL.png')
        logger.info('PLAF203查看历史视频切换日期超时或失败的APP截图保存')

    def getHistoryPlayChangeDate(self, count):
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
            self.driver.tap([(0.6630 * self.width, 0.5390 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
            logger.info('step4：点击实时流窗口的“回放”按钮')
            time.sleep(10)

            self.driver.tap([(0.6713 * self.width, 0.5024 * self.height)], duration=1)  # 点击回放界面的“切换日期”按钮
            logger.info('step5：点击回放界面的“切换日期”按钮')
            time.sleep(3)
            self.swipeDown()
            logger.info('step6：下滑切换到昨天的日期')
            time.sleep(3)
            # self.driver.tap([(0.4954 * self.width, 0.9408 * self.height)], duration=1)
            self.driver.find_element('xpath', '//android.widget.Button[@content-desc="CONFIRM"]').click()
            logger.info('step7：点击“确认”按钮')

            time.sleep(3)
            if 'CONFIRM' in self.driver.page_source:
                self.driver.find_element('xpath', '//android.widget.Button[@content-desc="CONFIRM"]').click()
                logger.info('step7：再次点击“确认”按钮')

            start_time = time.time()
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
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f'设备回放出流耗时：---- {elapsed_time:.2f} 秒')
                    self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                    self.getHistoryPlayChangeDateScreenshotSuccess(count)
                    logger.info('step8：设备查看回放成功！')
                    break
            else:
                logger.error('step8：设备回放出流超过30S失败！')
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.getHistoryPlayChangeDateScreenshotFail(count)
                time.sleep(2)
                if 'load' in self.driver.page_source:
                    time.sleep(2)
                    self.driver.tap([(0.8102 * self.width, 0.2428 * self.height)], duration=1)  # 点击回放窗口的“reload”
                    logger.info('step9：在回放出流窗口中点击Reload按钮')
                    for i in range(10):
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
                            logger.info('step10：设备重试回放出流成功！')
                            break
                    else:
                        logger.error('step11：设备重试出流超过10S失败！')
                        self.getHistoryPlayChangeDateScreenshotFail(count)
        time.sleep(3)
        self.driver.tap([(0.0842 * self.width, 0.0665 * self.height)], duration=1)  # 点击回放界面左上角的返回按钮
        logger.info('step8：点击左上角的返回按钮')
        time.sleep(1)

        for i in range(2):
            if 'Schedule' in self.driver.page_source:
                logger.info('step8：当前APP处于设备面板')
                break
            else:
                logger.error('step8：当前APP未处于设备面板')
                self.swipeDown()

        self.driver.tap([(0.0824 * self.width, 0.0621 * self.height)], duration=1)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203历史视频切换日期专项测试.log', rotation='100MB',
                   encoding='utf-8', enqueue=True)
        for count in range(1, self.testTimes + 1):
            try:
                self.getHistoryPlayChangeDate(count)
                logger.info(f'执行第 {count} 次PLAF203回放出流切换日期完成')
                time.sleep(self.intervalTime)
            except:
                logger.error(f'执行第 {count} 次PLAF203回放出流出现切换日期异常')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203回放出流切换日期的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info('PLAF203历史视频切换日期专项测试结束！')


if __name__ == '__main__':
    testTimes = input('请输入测试次数：---- ').strip()
    intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)---- ').strip()
    logger.info('开始执行PLAF203历史视频切换日期专项自动化测试...')
    # try:
    #     historyPlayChangeDateAF203 = HistoryPlayChangeDateAF203(testTimes, intervalTime)
    #     historyPlayChangeDateAF203.main()
    # except Exception as error:
    #     logger.info('An exception happened: ' + str(error))
    historyPlayChangeDateAF203 = HistoryPlayChangeDateAF203(testTimes, intervalTime)
    historyPlayChangeDateAF203.main()
