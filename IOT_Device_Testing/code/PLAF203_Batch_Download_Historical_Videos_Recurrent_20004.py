# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:49
@File         : PLAF203_Batch_Download_Historical_Videos_Recurrent_20004.py
@Interpreter Version: python 3.12
@Description:
'''

import io
import time
import subprocess
from loguru import logger
from appium import webdriver
from PIL import Image
from appium.webdriver.connectiontype import ConnectionType


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

    def brightScreenAndBreathingScreen(self):
        adb_cmd = 'adb shell input keyevent 26'
        subprocess.run(adb_cmd, shell=True)  # 执行 ADB 命令

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown1(self):
        x1 = int(0.7954 * self.width)
        y1 = int(0.7346 * self.height)
        y2 = int(0.7900 * self.height)
        self.swipe(x1, y1, x1, y2, 2000)

    def swipeDown2(self):
        x1 = int(0.6166 * self.width)
        y1 = int(0.7346 * self.height)
        y2 = int(0.7900 * self.height)
        self.swipe(x1, y1, x1, y2, 2000)

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
                self.swipeDown1()

        time.sleep(2)
        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step2：点击设备卡片')

        time.sleep(3)
        if 'Schedule' in self.driver.page_source:
            logger.info('step3：当前APP处于设备面板')
            time.sleep(2)
            self.driver.tap([(0.6630 * self.width, 0.5390 * self.height)], duration=1)  # 点击实时流窗口的“回放”按钮
            logger.info('step4：点击实时流窗口的“回放”按钮');
            time.sleep(20)
            # time.sleep(20)
            time.sleep(2)
            # self.driver.set_network_connection(ConnectionType.AIRPLANE_MODE);time.sleep(5)  # 切换到手机的飞行模式（关闭网络连接）
            # self.driver.set_network_connection(ConnectionType.ALL_NETWORK_ON);time.sleep(10)  # 切换到正常模式（开启网络连接）
            #  adb shell svc wifi disable  # 开启飞行模式
            #  adb shell svc wifi enable  # 打开WALN模式

            self.driver.tap([(0.6731 * self.width, 0.5091 * self.height)], duration=1)  # 点击回放界面的“切换日期”按钮
            logger.info('step5：点击回放界面的“切换日期”按钮');
            time.sleep(3)
            self.swipeDown2();
            time.sleep(3)
            self.swipeDown1()
            logger.info('step6：下滑切换到昨天的日期')
            self.driver.tap([(0.4861 * self.width, 0.9055 * self.height)], duration=1)
            logger.info('step7：点击回放界面的“CONFIRM”按钮');
            time.sleep(2)
            self.driver.find_element('xpath', '//android.widget.Button[@content-desc="ALL PLAYBACK VIDEOS"]').click()
            logger.info('step8：点击回放界面的“ALL PLAYBACK VIDEOS”按钮');
            time.sleep(20)
            self.driver.tap([(0.1972 * self.width, 0.6974 * self.height)], duration=1)
            logger.info('step9：点击该天历史视频列表的第7个文件夹')
            time.sleep(2)

            # def apphandle(self, count):
            self.driver.tap([(0.8824 * self.width, 0.1628 * self.height)], duration=1)
            logger.info('step10：在跳转的页面中点击“编辑”按钮');
            time.sleep(2)
            self.driver.tap([(0.5861 * self.width, 0.2283 * self.height)], duration=1);
            time.sleep(1)
            self.driver.tap([(0.5861 * self.width, 0.3429 * self.height)], duration=1);
            time.sleep(1)
            self.driver.tap([(0.5861 * self.width, 0.4571 * self.height)], duration=1);
            time.sleep(1)
            logger.info('step11：选择任意3个时长短的历史视频进行下载');
            time.sleep(2)
            self.driver.tap([(0.2537 * self.width, 0.8742 * self.height)], duration=1);
            time.sleep(3)
            logger.info('step12：点击Download按钮')
            self.driver.find_element('xpath', '//android.widget.Button[@content-desc="SAVE"]').click()
            logger.info('step13：在下载弹框中点击SAVE按钮');
            time.sleep(2)

            start_time = time.time()
            for i in range(180):
                # screenshot = self.driver.get_screenshot_as_png()
                # image = Image.open(io.BytesIO(screenshot))
                # rgb1 = image.getpixel((0.5148 * self.width, 0.6421 * self.height))
                # rgb2 = image.getpixel((0.5166 * self.width, 0.5900 * self.height))
                # confidents = [
                #     rgb1[0] == 144,  # 实时流左上角的像素点RGB值
                #     rgb1[1] == 213,
                #     rgb1[2] == 208,
                #
                #     rgb2[0] == 144,  # 实时流右上角的像素点RGB值
                #     rgb2[1] == 213,
                #     rgb2[2] == 208,
                # ]
                # confident1 = [
                #     rgb1[0] == 244,  # 实时流左上角的像素点RGB值
                #     rgb1[1] == 73,
                #     rgb1[2] == 76,
                #
                #     rgb2[0] == 244,  # 实时流右上角的像素点RGB值
                #     rgb2[1] == 73,
                #     rgb2[2] == 76,
                # ]
                # if all(confidents):
                if 'Succeeded' in self.driver.page_source:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f'历史视频下载耗时：---- {elapsed_time:.2f} 秒')
                    self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                    self.getHistoryPlayDownloadScreenshotSuccess(count)
                    logger.info('历史视频下载成功！')
                    break

                elif 'Fail' in self.driver.page_source:
                    self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                    self.getHistoryPlayDownloadScreenshotFail(count)
                    logger.error('历史视频下载失败！')
                    break
                else:
                    time.sleep(1)
            else:
                self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                self.getHistoryPlayDownloadScreenshotFail(count)
                logger.error('历史视频下载超时/下载失败')

            self.driver.tap([(0.9 * self.width, 0.4706 * self.height)], duration=1)
            logger.info('step11：点击下载成功弹框右上角的X按钮');
            time.sleep(2)

            self.driver.tap([(0.9 * self.width, 0.4706 * self.height)], duration=1)
            logger.info('step11：点击下载成功弹框右上角的X按钮');
            time.sleep(2)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203批量下载历史视频专项测试.log', rotation='100MB',
                   encoding='utf-8', enqueue=True)
        for count in range(1, self.testTimes + 1):
            try:
                # self.apphandle(count)
                self.downloadHistoryVide(count)
                logger.info(f'执行第 {count} 次PLAF203批量下载历史视频完成')
                logger.info(f'当前该文件数目：{self.count_files_in_android_directory()}');
                time.sleep(3)
                self.delete_files_in_android_directory();
                time.sleep(3)
                logger.info(f'当前该文件数目：{self.count_files_in_android_directory()}')
                time.sleep(self.intervalTime)
            except:
                logger.error(f'执行第 {count} 次PLAF203批量下载历史视频出现异常')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203批量下载历史视频的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info('PLAF203批量下载历史视频专项测试结束！')


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
