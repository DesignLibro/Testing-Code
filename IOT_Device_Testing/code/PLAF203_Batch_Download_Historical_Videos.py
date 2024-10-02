# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:47
@File         : PLAF203_Batch_Download_Historical_Videos.py
@Interpreter Version: python 3.12
@Description: 1. 为了让脚本能一直进行，需要加上清空手机相册文件的功能；
'''

import io
import time
import re
import subprocess
from datetime import datetime
from loguru import logger
from appium import webdriver
from PIL import Image
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


class DownloadMoreHistoryVideo(object):
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
        self.directory_path = '/sdcard/Movies/PETLIBRO'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

        self.adb_command = 'adb shell dumpsys power | grep "mScreenOn=true"'

    def count_files_in_android_directory(self):
        adb_command = f'adb shell ls -l {self.directory_path}'  # 构建adb命令
        result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)  # 执行adb命令并获取输出结果

        '''提取文件数目'''
        output = result.stdout.strip().split('\n')
        if len(output) > 1:
            files_count = len(output) - 1  # 减去目录本身的行数
            return files_count
        elif len(output) == 1:
            return 1
        else:
            return 0

    def delete_files_in_android_directory(self):
        adb_command = f'adb shell rm -rf {self.directory_path}/*'  # 构建adb命令
        subprocess.run(adb_command, shell=True)  # 执行adb命令

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

    def getHistoryPlayDownloadScreenshotSuccess(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203批量下载多个历史视频 SUCCESS.png')
        logger.info('PLAF203查看下载多个历史视频成功的APP截图保存')

    def getHistoryPlayDownloadScreenshotFail(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203批量下载多个历史视频 FAIL.png')
        logger.info('PLAF203查看下载多个历史视频超时或失败的APP截图保存')

    def downloadHistoryVide(self, count):
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
            logger.info('step3：当前APP处于设备面板');
            time.sleep(6)
            self.driver.tap([(0.6601 * self.width, 0.4831 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
            logger.info('step4：点击实时流窗口的“回放”按钮')
            self.flag = False
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
                    logger.info('step5：设备回放出流成功！')
                    self.driver.tap([(0.4907 * self.width, 0.4210 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
                    start_time = time.time()
                    logger.info('step6：点击回放流窗口的“下载”按钮');
                    time.sleep(2)
                    # result = re.findall('<android.view.View index="6" package="com.designlibro.petlibro" class="android.view.View" text="" content-desc="(.*?)"', self.driver.page_source)
                    # time_obj = datetime.strptime(result[0], '%M:%S')  # 使用 datetime.strptime() 解析时间字符串
                    # seconds = time_obj.minute * 60 + time_obj.second
                    # logger.info(f'该历史视频时长为{seconds} S')
                    # self.driver.tap([(0.5129 * self.width, 0.7061 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
                    self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'SAVE').click()
                    logger.info('step7：点击“确认下载”按钮')
                    for i in range(6000):
                        if 'Succeeded' in self.driver.page_source:
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            logger.info(f'历史视频下载耗时：---- {elapsed_time:.2f} 秒')
                            self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                            self.getHistoryPlayDownloadScreenshotSuccess(count)
                            logger.info('历史视频下载成功！')
                            self.flag = True
                            break
                        elif 'Fail' in self.driver.page_source:
                            self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                            self.getHistoryPlayDownloadScreenshotFail(count)
                            logger.error('历史视频下载失败！')
                            self.flag = True
                            break
                        else:
                            time.sleep(1)
                    else:
                        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                        self.getHistoryPlayDownloadScreenshotFail(count)
                        logger.error('历史视频下载超时/下载失败')
                        self.flag = True
                        break
                    if self.flag:
                        break
            else:
                logger.error('step5：设备出流超过10S失败！')
                self.getHistoryPlayDownloadScreenshotFail(count)

            time.sleep(3)
            for i in range(600):
                if 'loading' in self.driver.page_source:
                    time.sleep(1)
                else:
                    break
            self.driver.tap([(0.9 * self.width, 0.4696 * self.height)], duration=1)
            # self.driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.Button').click()
            # self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.Button').click()
            logger.info('step8：点击“关闭下载弹框”按钮');
            time.sleep(3)
            if 'Succeeded' in self.driver.page_source:
                self.driver.tap([(0.9 * self.width, 0.4026 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
                logger.info('step8：再次点击“关闭下载弹框”按钮');
                time.sleep(3)
            self.driver.tap([(0.0732 * self.width, 0.0664 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
            logger.info('step9：点击“返回设备面板”按钮');
            time.sleep(3)
            self.driver.tap([(0.0732 * self.width, 0.0664 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
            logger.info('step10：点击“设备卡片”按钮');
            time.sleep(3)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203批量下载历史视频专项测试.log', rotation='100MB',
                   encoding='utf-8', enqueue=True)
        for count in range(1, self.testTimes + 1):
            try:
                self.downloadHistoryVide(count)
                logger.info(f'执行第 {count} 次PLAF203批量下载历史视频完成')
                logger.info(f'当前该文件数目：{self.count_files_in_android_directory()}');
                time.sleep(3)
                # self.delete_files_in_android_directory();time.sleep(3)
                logger.info(f'当前该文件数目：{self.count_files_in_android_directory()}')
                time.sleep(self.intervalTime)
            except:
                logger.error(f'执行第 {count} 次PLAF203批量下载历史视频出现异常')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203批量下载历史视频的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info('PLAF203批量下载历史视频专项测试结束！')

            #
            # self.driver.find_element('xpath', '//android.widget.Button[@content-desc="ALL PLAYBACK VIDEOS"]').click()
            # logger.info('step5：点击回放界面的“ALL PLAYBACK VIDEOS”按钮')
            # time.sleep(2)
            # self.driver.tap([(0.2 * self.width, 0.4547 * self.height)], duration=1)
            # logger.info('step6：点击该天历史视频列表的第一个文件夹')
            # time.sleep(2)
            # self.driver.tap([(0.8824 * self.width, 0.1628 * self.height)], duration=1)
            # logger.info('step7：在跳转的页面中点击“编辑”按钮');time.sleep(2)
            # self.driver.tap([(0.1925 * self.width, 0.2519 * self.height)], duration=1);time.sleep(1)
            # self.driver.tap([(0.4972 * self.width, 0.2519 * self.height)], duration=1);time.sleep(1)
            # self.driver.tap([(0.8037 * self.width, 0.2519 * self.height)], duration=1);time.sleep(1)
            # logger.info('step8：选择3个历史视频进行下载');time.sleep(2)
            # self.driver.tap([(0.2537 * self.width, 0.8742 * self.height)], duration=1);time.sleep(3)
            # self.driver.find_element('xpath', '//android.widget.Button[@content-desc="SAVE"]').click()
            # logger.info('step9：在下载弹框中点击SAVE按钮');time.sleep(2)

    #         start_time = time.time()
    #         for i in range(1800):
    #             screenshot = self.driver.get_screenshot_as_png()
    #             image = Image.open(io.BytesIO(screenshot))
    #             rgb1 = image.getpixel((0.5148 * self.width, 0.6421 * self.height))
    #             rgb2 = image.getpixel((0.5166 * self.width, 0.5900 * self.height))
    #             confidents = [
    #                 rgb1[0] == 144,  # 实时流左上角的像素点RGB值
    #                 rgb1[1] == 213,
    #                 rgb1[2] == 208,
    #
    #                 rgb2[0] == 144,  # 实时流右上角的像素点RGB值
    #                 rgb2[1] == 213,
    #                 rgb2[2] == 208,
    #             ]
    #             confident1 = [
    #                 rgb1[0] == 244,  # 实时流左上角的像素点RGB值
    #                 rgb1[1] == 73,
    #                 rgb1[2] == 76,
    #
    #                 rgb2[0] == 244,  # 实时流右上角的像素点RGB值
    #                 rgb2[1] == 73,
    #                 rgb2[2] == 76,
    #             ]
    #             if all(confidents):
    #                 end_time = time.time()
    #                 elapsed_time = end_time - start_time
    #                 logger.info(f'历史视频下载耗时：---- {elapsed_time:.2f} 秒')
    #                 self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    #                 self.getHistoryPlayDownloadScreenshotSuccess(count)
    #                 logger.info('历史视频下载成功！')
    #                 break
    #
    #             elif any(confident1):
    #                 self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    #                 self.getHistoryPlayDownloadScreenshotFail(count)
    #                 logger.error('历史视频下载失败！')
    #                 break
    #             else:
    #                 time.sleep(1)
    #         else:
    #             self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    #             self.getHistoryPlayDownloadScreenshotFail(count)
    #             logger.error('历史视频下载超时/下载失败')
    #
    #         self.driver.tap([(0.9 * self.width, 0.4007 * self.height)], duration=1)
    #         logger.info('step10：点击下载成功弹框右上角的X按钮');time.sleep(2)
    #         self.driver.tap([(0.0759 * self.width, 0.0631 * self.height)], duration=1)
    #         logger.info('step11：点击视频列表左上角的返回按钮');time.sleep(2)
    #         self.driver.tap([(0.0759 * self.width, 0.0631 * self.height)], duration=1)
    #         logger.info('step12：点击上一个视频列表左上角的返回按钮');time.sleep(2)
    #         self.driver.tap([(0.0759 * self.width, 0.0631 * self.height)], duration=1)
    #         logger.info('step13：点击回放界面左上角的返回按钮');time.sleep(2)
    #         self.driver.tap([(0.0759 * self.width, 0.0631 * self.height)], duration=1)
    #         logger.info('f：点击设备面板左上角的返回按钮');time.sleep(2)
    #
    # def main(self):
    #     logger.add(rf'../log/{self.logFilename}--PLAF203批量下载历史视频专项测试.log', rotation='100MB', encoding='utf-8', enqueue=True)
    #     for count in range(1, self.testTimes + 1):
    #         try:
    #             self.downloadHistoryVide(count)
    #             logger.info(f'执行第 {count} 次PLAF203批量下载历史视频完成')
    #             time.sleep(self.intervalTime)
    #         except:
    #             logger.error(f'执行第 {count} 次PLAF203批量下载历史视频出现异常')
    #         remainingTimes = self.testTimes - count
    #         logger.info(f'剩余测试PLAF203批量下载历史视频的次数为：{remainingTimes}')
    #         if count == self.testTimes:
    #             logger.info('PLAF203批量下载历史视频专项测试结束！')


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：---- ').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)---- ').strip()
    testTimes = 10000
    intervalTime = 5
    logger.info('开始执行PLAF203批量下载历史视频专项自动化测试...')
    # try:
    #     downloadMoreHistoryVideo = DownloadMoreHistoryVideo(testTimes, intervalTime)
    #     downloadMoreHistoryVideo.main()
    # except Exception as error:
    #     logger.info('An exception happened: ' + str(error))
    downloadMoreHistoryVideo = DownloadMoreHistoryVideo(testTimes, intervalTime)
    downloadMoreHistoryVideo.main()
