# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:39
@File         : PLAF203_Bluetooth_Bind_Device_Fake_Connections.py
@Interpreter Version: python 3.12
@Description:
'''

import re
import time
import subprocess
from loguru import logger
from appium import webdriver
from selenium.webdriver.common.by import By


class BlueToothBindTestAF203(object):
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

        # self.MAC = 'C4:3C:B0:E4:ED:78'  # demo环境的设备
        self.MAC = '2C:C3:E6:A6:4D:6F'  # 生产环境的设备
        # self.MAC = '00:E0:4C:BD:DB:C4'  # demo环境的设备
        # self.MAC = '34:7D:E4:BA:0B:6E'  # test环境的设备
        self.WIFIName = 'TP-LINK_190E'
        self.WIFIPasswd = '123456789'

        # self.ADBCommand = 'adb shell svc power stayon true'  # 让Android设备保持唤醒状态
        # subprocess.check_output([f'{self.ADBCommand}', self.desired_capabilities['udid']])

        # self.ADBCommand = 'adb shell svc power stayon false'  # 让Android设备保持休眠状态
        # subprocess.check_output([f'{self.ADBCommand}', self.desired_capabilities['udid']])

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    # def on_pause(self, event):
    #     logger.info('屏幕熄灭')
    #
    # def on_resume(self, event):
    #     logger.info('屏幕亮屏')
    #
    # def reopenBluetooth(self):
    #     # 关闭蓝牙功能
    #     subprocess.run(['adb', '-s', f'{self.desired_capabilities["udid"]}', 'shell', 'am', 'start', '-a', 'android.bluetooth.adapter.action.REQUEST_DISABLE'])
    #     time.sleep(2)
    #     # 开启蓝牙功能
    #     subprocess.run(['adb', '-s', f'{self.desired_capabilities["udid"]}', 'shell', 'am', 'start', '-a', 'android.bluetooth.adapter.action.REQUEST_ENABLE'])

    def bingingAndUnbindDevice(self, count):
        time.sleep(8)
        if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
            logger.info('step1：当前APP处于设备首页')
        else:
            logger.error('step1：当前APP未处于设备首页')
            return

        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step2：点击界面中心的添加设备按钮')
        time.sleep(2)

        count = 1
        for i in range(3):
            logger.info('step3：蓝牙搜索指定设备中...')
            start_time = time.time()
            for i in range(20):
                if self.MAC in self.driver.page_source:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f'第{count}次搜索...')
                    logger.info(f'step4：发现设备MAC地址---- {self.MAC}')
                    logger.info(f'蓝牙搜索设备耗时：---- {elapsed_time:.2f} 秒')
                    break
                else:
                    time.sleep(1)
            else:
                logger.error(f'蓝牙搜索设备超时 ---- {self.MAC}')
                time.sleep(2)
                # self.reopenBluetooth()
                self.bingingAndUnbindDeviceScreenshot(count)
                logger.error('停止后续的操作，重新执行整个搜索MAC的流程...')
                self.driver.tap([(0.0712 * self.width, 0.0664 * self.height)], duration=1)
                logger.info('点击搜索MAC左上角的返回按钮')

                if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                    logger.info('step1：当前APP处于设备首页')
                else:
                    logger.error('step1：当前APP未处于设备首页')
                    return
                time.sleep(20)
                self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
                logger.info('step2：点击界面中心的添加设备按钮')
                time.sleep(2)
                count += 1
                continue
            break

        mainText = re.findall(r'MAC:(\S+)', self.driver.page_source)
        mainTextNew = [i.replace('"', '') for i in mainText]
        for text in mainTextNew:
            if self.MAC == text:
                index = mainTextNew.index(text)
                time.sleep(2)
                bound = re.findall(
                    rf'<android.widget.ImageView index="{index}" package="com.designlibro.petlibro" class="android.widget.ImageView" text="" content-desc="Granary Camera Feeder&#10;MAC:{self.MAC}" resource-id="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
                    self.driver.page_source)
                self.driver.tap(
                    [(int((bound[0][2])) / 1080 * self.width - 25, int((bound[0][3])) / 2076 * self.height - 118)],
                    duration=1)
                logger.info('step5：点击进入输入WIFI信息界面')
                break

        time.sleep(4)
        if 'ADD DEVICE' in self.driver.page_source:
            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').click()
            logger.info('step6：点击WIFI名称输入栏')

            time.sleep(2)
            self.driver.tap([(0.7796 * self.width, 0.4075 * self.height)], duration=1)
            logger.info(f'step7：点击一键删除WIFI名称按钮')

            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').send_keys(
                self.WIFIName)
            logger.info(f'step8：输入WIFI名称')

            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').click()
            logger.info('step9：点击WIFI密码输入栏')

            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').send_keys(
                self.WIFIPasswd)
            logger.info(f'step10：输入WIFI密码')

            time.sleep(2)
            self.driver.tap([(0.4889 * self.width, 0.8449 * self.height)], duration=1)
            logger.info(f'step11：点击Next按钮')

        time.sleep(2)
        if 'The device has been found...' in self.driver.page_source:
            logger.info(f'step12：APP处于绑定中...界面')

        for i in range(180):
            if 'GET STARTED' in self.driver.page_source:
                logger.info('step13：蓝牙绑定设备成功！')
                break
            else:
                time.sleep(1)
        else:
            logger.error('step13：蓝牙绑定设备超时或绑定失败！')
            self.swipeDown()

            for i in range(2):
                time.sleep(2)
                self.swipeDown()
                time.sleep(4)
                self.driver.tap([(0.5 * self.width, 0.7890 * self.height)], duration=1)
                logger.info('step13：点击RETRY按钮')

            count = 1
            for i in range(3):
                logger.info('step3：蓝牙搜索指定设备中...')
                start_time = time.time()
                for i in range(20):
                    if self.MAC in self.driver.page_source:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        logger.info(f'第{count}次搜索...')
                        logger.info(f'step4：发现设备MAC地址---- {self.MAC}')
                        logger.info(f'蓝牙搜索设备耗时：---- {elapsed_time:.2f} 秒')
                        break
                    else:
                        time.sleep(1)
                else:
                    logger.error(f'蓝牙搜索设备超时 ---- {self.MAC}')
                    time.sleep(2)
                    # self.reopenBluetooth()
                    self.bingingAndUnbindDeviceScreenshot(count)
                    logger.error('停止后续的操作，重新执行整个搜索MAC的流程...')
                    self.driver.tap([(0.0694 * self.width, 0.0655 * self.height)], duration=1)
                    logger.info('点击搜索MAC左上角的返回按钮')

                    if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                        logger.info('step1：当前APP处于设备首页')
                    else:
                        logger.error('step1：当前APP未处于设备首页')
                        return

                    self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
                    logger.info('step2：点击界面中心的添加设备按钮')
                    time.sleep(2)

                    count += 1
                    continue
                break

            mainText = re.findall(r'MAC:(\S+)', self.driver.page_source)
            mainTextNew = [i.replace('"', '') for i in mainText]
            for text in mainTextNew:
                if self.MAC == text:
                    index = mainTextNew.index(text)
                    time.sleep(2)
                    bound = re.findall(
                        rf'<android.widget.ImageView index="{index}" package="com.designlibro.petlibro" class="android.widget.ImageView" text="" content-desc="Granary Camera Feeder&#10;MAC:{self.MAC}" resource-id="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
                        self.driver.page_source)
                    self.driver.tap(
                        [(int((bound[0][2])) / 1080 * self.width - 25, int((bound[0][3])) / 2076 * self.height - 118)],
                        duration=1)
                    logger.info('step5：点击进入输入WIFI信息界面')
                    break

            time.sleep(4)
            if 'ADD DEVICE' in self.driver.page_source:
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').click()
                logger.info('step6：点击WIFI名称输入栏')

                time.sleep(2)
                self.driver.tap([(0.7796 * self.width, 0.4075 * self.height)], duration=1)
                logger.info(f'step7：点击一键删除WIFI名称按钮')

                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').send_keys(
                    self.WIFIName)
                logger.info(f'step8：输入WIFI名称')

                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').click()
                logger.info('step9：点击WIFI密码输入栏')

                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').send_keys(
                    self.WIFIPasswd)
                logger.info(f'step10：输入WIFI密码')

                time.sleep(2)
                self.driver.tap([(0.4889 * self.width, 0.8449 * self.height)], duration=1)
                logger.info(f'step11：点击Next按钮')

            time.sleep(2)
            if 'The device has been found...' in self.driver.page_source:
                logger.info(f'step12：APP处于绑定中...界面')

            for i in range(135):
                if 'GET STARTED' in self.driver.page_source:
                    logger.info('step13：蓝牙绑定设备成功！')
                    break
                else:
                    time.sleep(1)
            else:
                logger.error('step13：蓝牙绑定设备超时或绑定失败！')

        time.sleep(2)
        self.driver.tap([(0.5167 * self.width, 0.9340 * self.height)], duration=1)
        logger.info('step14：点击GET STARTED按钮')

        time.sleep(2)
        if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
            logger.info('step15：当前APP处于设备首页')
        else:
            logger.error('step15：当前APP未处于设备首页')
            return

        self.swipeDown()
        logger.info('step16：下拉刷新设备首页')

        time.sleep(3)
        if 'Granary Camera Feeder' in self.driver.page_source:
            logger.info('step17：首页设备卡片已存在')
        else:
            logger.error('step17：首页设备卡片不存在')
            self.swipeDown()
            logger.info('step17：重试下拉刷新设备首页')

        self.driver.tap([(0.5 * self.width, 0.4750 * self.height)], duration=1)
        logger.info('step18：点击设备卡片')

        time.sleep(3)
        if 'Schedule' in self.driver.page_source:
            logger.info('step19：当前APP处于设备面板')

        self.driver.tap([(0.8889 * self.width, 0.0640 * self.height)], duration=1)
        logger.info('step20：点击设置按钮')

        for i in range(2):
            time.sleep(3)
            if 'DEVICE SETTINGS' in self.driver.page_source:
                logger.info('step21：当前APP处于设置界面')

            time.sleep(3)
            self.swipeDown()
            time.sleep(3)
            self.swipeDown()
            logger.info('step22：下拉到设置界面底部')

            time.sleep(3)
            self.driver.tap([(0.4954 * self.width, 0.8415 * self.height)], duration=1)
            logger.info('step23：点击解绑设备按钮')

            time.sleep(2)
            self.driver.tap([(0.5167 * self.width, 0.5718 * self.height)], duration=1)
            logger.info('step24：点击确认解绑设备按钮')

        time.sleep(2)
        if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
            logger.info('step25：解绑设备成功')
        else:
            logger.error('step25：解绑设备失败')

    def bingingAndUnbindDeviceScreenshot(self, count):
        self.driver.get_screenshot_as_file(rf'../result/{self.logFilename}--第{count}次PLAF203绑定解绑设备 FAIL.png')
        logger.info('PLAF203蓝牙搜索设备失败或超时的APP截图保存')

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203绑定蓝牙解绑设备专项测试.log', rotation='100MB',
                   encoding='utf-8', enqueue=True)
        for count in range(1, self.testTimes + 1):
            try:
                self.bingingAndUnbindDevice(count)
                logger.info(f'执行第 {count} 次PLAF203蓝牙绑定解绑设备 SUCCESS')
                time.sleep(self.intervalTime)
            except:
                logger.error(f'执行第 {count} 次PLAF203蓝牙绑定解绑设备 FAIL')
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203蓝牙绑定解绑设备的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info(f'PLAF203蓝牙绑定解绑设备专项自动化测试结束！')


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：---- ').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)---- ').strip()
    testTimes = 100000
    intervalTime = 2
    logger.info('开始执行PLAF203蓝牙绑定解绑专项自动化测试...')
    # try:
    #     blueToothBindTestAF203 = BlueToothBindTestAF203(testTimes, intervalTime)
    #     blueToothBindTestAF203.main()
    # except Exception as error:
    #     logger.info('An exception happened: ' + str(error))
    blueToothBindTestAF203 = BlueToothBindTestAF203(testTimes, intervalTime)
    blueToothBindTestAF203.main()
