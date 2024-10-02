# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/2/4 16:18
# @File         : general_module.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import yaml
import time
import re
import os
import subprocess
from loguru import logger
from appium import webdriver
# from appium.webdriver.common.mobileby import MobileBy
# from appium.webdriver.common.touch_action import TouchAction
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC



class General_module(object):
    '''初始化函数'''
    def __init__(self, apk_path_name):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

        # try:
        #     logger.info('正在安装Android APK...')
        #     process = subprocess.run(['adb', 'install', '-r', apk_path_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #
        #     # 检查结果
        #     if process.returncode == 0:
        #         logger.info(f'{apk_path_name} 安装成功')
        #     else:
        #         logger.error(f'{apk_path_name} 安装失败')
        #         logger.error(process.stdout.decode())
        #         logger.error(process.stderr.decode())
        # except Exception as error:
        #     logger.error(f'安装APK包{apk_path_name} 时发生错误：{error}')

        # try:
        #     current_script_path = os.path.abspath(__file__)  # 获取当前脚本文件的绝对路径
        #     script_dir = os.path.dirname(current_script_path)  # 获取脚本所在的目录
        #     os.chdir(script_dir)  # 切换工作目录至脚本所在目录
        #     time.sleep(2)
        #
        #     with open('../config/config.yaml', 'r', encoding='UTF-8') as config_file:
        #         data = yaml.safe_load(config_file)
        # except:
        #     current_script_path = os.path.abspath(__file__)  # 获取当前脚本文件的绝对路径
        #     script_dir = os.path.dirname(current_script_path)  # 获取脚本所在的目录
        #     os.chdir(script_dir)  # 切换工作目录至脚本所在目录
        #     time.sleep(2)
        #
        #     with open('../config/config.yaml', 'r', encoding='UTF-8') as config_file:
        #         data = yaml.safe_load(config_file)
        #
        # self.desired_capabilities = data['desired_capabilities']  # 测试手机的固定参数
        # logger.info(self.desired_capabilities)
        # self.width = data['width']  # 测试手机的长像素
        # self.height = data['height']  # 测试手机的宽像素
        # self.AF103_MAC = data['AF103_MAC']  # 测试设备的MAC
        # self.AF103_NAME = data['AF103_NAME']  # 测试设备的名称
        # self.AF103_MODEL = data['AF103_MODEL']  # 测试设备的型号
        # self.wifi1 = data['wifi1']  # 测试蓝牙绑定设备的wifi1
        # self.passwd1 = data['passwd1']  # 测试蓝牙绑定设备的密码1
        # self.mainTimeoutDuration = data['mainTimeoutDuration']  # APP登录成功后在首页的判断超时时间
        # self.searchDeviceTimeoutDuration = data['searchDeviceTimeoutDuration']  # 蓝牙搜索设备超时时间
        # self.bluetoothBindingDeviceTimeout = data['bluetoothBindingDeviceTimeout']  # 蓝牙绑定设备的超时时间
        # self.diyDeviceName = data['diyDeviceName']  # 自定义设备名称
        # self.failRetryCount = data['failRetryCount']  # 用例执行失败时的最大尝试次数

        # self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_capabilities)  # 连接Appium Server，初始化自动化环境

    # '''控制手机屏幕滑动'''
    # def swipe(self, start_x, start_y, end_x, end_y, duration=None):
    #     self.driver.swipe(start_x, start_y, end_x, end_y)
    #
    # '''控制手机屏幕下滑'''
    # def swipeDown(self):
    #     x1 = int(0.7130 * self.width)
    #     y1 = int(0.9855 * self.height)
    #     y2 = int(0.1498 * self.height)
    #     self.swipe(x1, y1, x1, y2, 20000)

    '''APP首页长按解绑设备卡片'''
    def longPressDeviceCard(self):
        try:
            self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1500)
            logger.info('step22：APP首页长按设备卡片')

            time.sleep(1)
            self.driver.tap([(0.9009 * self.width, 0.3255 * self.height)], duration=1)
            logger.info('step23：点击删除设备卡片按钮')

            time.sleep(1)
            self.driver.tap([(0.5222 * self.width, 0.6314 * self.height)], duration=1)
            logger.info('step24：点击确认删除设备卡片按钮')
            time.sleep(2)
            return True
        except:
            return False

    '''APP首页点击设备卡片'''
    def clickDeviceCard(self):
        try:
            self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1)
            logger.info('step1：点击首页设备卡片')
            return True
        except:
            return False

    '''出现异常时APP截图保存'''
    def getHistoryPlayScreenshotSuccess(self):
        try:
            self.driver.get_screenshot_as_file(rf'../screenshot/failScreenshot_{self.logFilename}.png')
            logger.info('用例执行异常截图保存')
            return True
        except:
            return False

    # -----------------------------------------------------------------------------------------------------------------

    # '''不允许petlibro app通知'''
    # def notAllowAPPNotification(self):
    #     try:
    #         self.driver.tap([(0.5037 * self.width, 0.6796 * self.height)], duration=1)
    #         logger.info('点击不允许petlibro app通知按钮')
    #         time.sleep(2)
    #         return True
    #     except:
    #         return False

    # '''取消邀评弹窗'''
    # def commentCancel(self):
    #     try:
    #         if 'ENJOYING PETLIBRO' in self.driver.page_source:
    #             self.driver.tap([(0.6398 * self.width, 0.7460 * self.height)], duration=1)
    #             logger.info('点击取消邀评弹窗')
    #             time.sleep(2)
    #             return True
    #     except:
    #         return False
    #
    #
    # '''取消POP_UP弹窗'''
    # def popCancel(self):
    #     try:
    #         self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
    #         logger.info('点击取消POP_UP弹窗')
    #         time.sleep(2)
    #         return True
    #     except:
    #         return True

    '''同意授权location权限'''
    def acceptLocationPermissions(self):
        try:
            time.sleep(3)
            self.driver.tap([(0.5435 * self.width, 0.7076 * self.height)], duration=1)
            logger.info('点击同意授权location权限')
            return True
        except:
            return False

    '''同意授权APP发现设备的权限'''
    def acceptAPPFindDevicePermissions(self):
        try:
            time.sleep(3)
            self.driver.tap([(0.4972 * self.width, 0.6384 * self.height)], duration=1)
            logger.info('点击同意授权APP发现设备的权限')
            return True
        except:
            return False

    '''同意麦克风权限'''
    def acceptMicroPermissions(self):
        pass


    # -----------------------------------------------------------------------------------------------------------------

    '''APP首页判断'''
    def mainJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Device' in self.driver.page_source and 'Me' in self.driver.page_source:
                    logger.info('step1：当前APP处于设备首页')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error('step1：当前APP未处于设备首页，后续用例无法执行')
            return False

    '''点击添加设备按钮'''
    def clickAddDeviceButton(self):
        try:
            time.sleep(2)
            self.driver.tap([(0.8861 * self.width, 0.0865 * self.height)], duration=1)
            logger.info('step2：点击添加设备按钮')
            return True
        except:
            return False

    '''蓝牙搜索设备界面判断'''
    def bluetoothDeviceSearchInterfaceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'ADD MANUALLY' in self.driver.page_source:
                    logger.info('step3：蓝牙搜索指定设备中...')
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error('step3：当前APP未处于蓝牙搜索设备界面，后续用例无法执行')
            return False

    '''蓝牙搜索设备'''
    def bluetoothDeviceSearch(self):
        time.sleep(2)
        startSearchTime = time.time()
        for y in range(self.failRetryCount):  # 尝试
            for i in range(self.searchDeviceTimeoutDuration):
                if self.driver.page_source:
                    if self.AF103_MAC in self.driver.page_source:
                        endSearchTime = time.time()
                        timeConsumed = endSearchTime - startSearchTime
                        logger.info(f'step4：蓝牙搜索指定{self.AF103_MODEL}设备{self.AF103_MAC}成功，耗时 {timeConsumed:.2f} 秒')
                        return True
                    else:
                        time.sleep(1)
                        self.swipeDown()
        else:
            logger.error(f'step4：重试蓝牙搜索指定{self.AF103_MODEL}设备{self.AF103_MAC}超时{self.searchDeviceTimeoutDuration}S，后续用例无法执行')
            return False

    '''点击MAC卡片'''
    def clickMAC(self):
        mainText = re.findall(r'MAC:(\S+)', self.driver.page_source)
        mainTextNew = [i.replace('"', '') for i in mainText]
        for text in mainTextNew:
            if self.AF103_MAC == text:
                index = mainTextNew.index(text)
                time.sleep(2)
                bound = re.findall(rf'<android.widget.ImageView index="{index}" package="com.designlibro.petlibro" class="android.widget.ImageView" text="" content-desc="{self.AF103_NAME}&#10;MAC:{self.AF103_MAC}" resource-id="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', self.driver.page_source)
                self.driver.tap([(int((bound[0][2])) / self.width * self.width - 26, int((bound[0][3])) / self.height * self.height - 120)], duration=1)
                logger.info('step5：点击设备MAC卡片，进入输入WIFI信息界面')
                return True
        else:
            return False

    '''WIFI信息编辑界面判断'''
    def WIFIFaceJudge(self):
        time.sleep(3)
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Common router settings' in self.driver.page_source:
                    logger.info('step6：当前APP处于输入WIFI信息界面')
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error(f'step6：当前APP未处于输入WIFI信息界面，后续用例无法执行')
            return False

    '''输入WIFI信息并点击下一步'''
    def inputWIFIInfoAndNext(self):
        try:
            time.sleep(2)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').click()
            logger.info('step7：点击WIFI名称输入栏')

            time.sleep(2)
            self.driver.tap([(0.7981 * self.width, 0.3545 * self.height)], duration=1)
            logger.info(f'step8：点击一键删除WIFI名称按钮')

            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').send_keys(
                self.wifi1)
            logger.info(f'step9：输入WIFI名称：{self.wifi1}')

            time.sleep(2)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').click()
            logger.info('step10：点击WIFI密码输入栏')

            time.sleep(2)
            self.driver.tap([(0.7981 * self.width, 0.4747 * self.height)], duration=1)
            logger.info(f'step11：点击一键删除WIFI密码按钮')

            time.sleep(2)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').send_keys(
                self.passwd1)
            logger.info(f'step12：输入WIFI密码：{self.passwd1}')

            time.sleep(2)
            self.driver.tap([(0.5222 * self.width, 0.9246 * self.height)], duration=1)
            logger.info(f'step13：点击Next按钮')
            return True
        except:
            return False

    '''蓝牙绑定设备界面判断'''
    def bluetoothDeviceBindingInterfaceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'The device has been found' in self.driver.page_source:
                    logger.info('step14：蓝牙绑定设备中...')
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error(f'step14：当前APP未处于蓝牙绑定设备界面，后续用例无法执行')
            return False

    '''蓝牙绑定设备结果判断'''
    def bluetoothDeviceBindingResultJudge(self):
        for y in range(self.failRetryCount):  # 尝试
            for i in range(self.bluetoothBindingDeviceTimeout):
                if self.driver.page_source:
                    if 'success' in self.driver.page_source:
                        logger.info(f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}成功，需在首页进一步验证是否绑定成功')
                        return True
                    elif 'Fail' in self.driver.page_source:
                        logger.error(f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}失败，重试蓝牙配网步骤')
                        time.sleep(2)
                        self.driver.tap([(0.5009 * self.width, 0.8741 * self.height)], duration=1)
                        logger.info('点击Retry按钮')

                        time.sleep(2)
                        self.bluetoothDeviceSearch()  # 蓝牙搜索设备
                        self.clickMAC()  # 点击MAC卡片
                        self.WIFIFaceJudge()  # WIFI信息编辑界面判断
                        self.inputWIFIInfoAndNext()  # 输入WIFI信息并点击下一步
                        self.bluetoothDeviceBindingInterfaceJudge()  # 蓝牙绑定设备界面判断

                        # 蓝牙绑定设备结果判断
                        for i in range(self.bluetoothBindingDeviceTimeout):
                            if self.driver.page_source:
                                if 'success' in self.driver.page_source:
                                    logger.info(
                                        f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}成功，需在首页进一步验证是否绑定成功')
                                    return True
                                elif 'Fail' in self.driver.page_source:
                                    logger.error(f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}失败，后续用例无法执行')
                                    return False
                            else:
                                time.sleep(1)
                    else:
                        time.sleep(1)
        else:
            logger.error(f'step15：重试蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}超时{self.bluetoothBindingDeviceTimeout}S失败，后续用例无法执行')
            return False

    '''对设备进行重命名'''
    def renameDevice(self):
        try:
            time.sleep(2)
            self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText').click()
            logger.info(f'step16：点击设备命名输入栏')

            time.sleep(2)
            self.driver.tap([(0.8638 * self.width, 0.5668 * self.height)], duration=1)
            logger.info(f'step17：点击一键删除设备名称按钮')

            time.sleep(2)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText').send_keys(self.diyDeviceName)
            logger.info(f'step18：输入自定义设备名称 {self.diyDeviceName}')
            time.sleep(2)

            self.driver.tap([(0.5111 * self.width, 0.9663 * self.height)], duration=1)
            logger.info(f'step19：点击GET STARTED按钮')
            return True
        except:
            return False

    '''跳过AF103设备的one last step'''
    def skipAF103OneLastStep(self):
        try:
            time.sleep(3)
            self.driver.tap([(0.8805 * self.width, 0.9900 * self.height)], duration=1)
            logger.info(f'step20：跳过AF103设备的one last step页面')
            return True
        except:
            return False

    '''首页设备判断'''
    def mainDeviceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if self.diyDeviceName in self.driver.page_source:
                    logger.info(f'step21：{self.AF103_MODEL}设备{self.AF103_MAC}蓝牙绑定成功')
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error(f'step21：{self.AF103_MODEL}设备{self.AF103_MAC}蓝牙绑定失败，后续用例无法执行')
            return False

    '''解绑设备验证'''
    def unbindDeviceJudge(self):
        for y in range(self.failRetryCount):  # 尝试
            for i in range(self.mainTimeoutDuration):
                if self.driver.page_source:
                    if self.diyDeviceName not in self.driver.page_source:
                        logger.info(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行成功')
                        return True
                    elif self.diyDeviceName in self.driver.page_source:
                        logger.error(f'{self.AF103_MODEL}设备{self.AF103_MAC}解绑失败，重试解绑步骤')
                        self.longPressDeviceCard()

                        for i in range(self.mainTimeoutDuration):
                            if self.driver.page_source:
                                if self.diyDeviceName not in self.driver.page_source:
                                    logger.info(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行成功')
                                    return True
                                elif self.diyDeviceName in self.driver.page_source:
                                    logger.error(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}重试解绑失败，后续用例无法执行')
                                    return False
                            else:
                                time.sleep(1)
                                self.swipeDown()
                                time.sleep(2)
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行失败，后续用例无法执行')
            return False

    '''设备面板判断'''
    def deviceFaceJudge(self):  # 适用103、
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Meal Call' in self.driver.page_source:
                    logger.info('step2：跳转到设备面板')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error('step2：当前未处于设备面板，后续用例无法执行')
            return False

    '''点击设备面板底部的喂食录音入口'''
    def clickDeviceFaceMealCall(self):
        try:
            self.driver.tap([(0.8000 * self.width, 0.9999 * self.height)], duration=1)
            logger.info('step3：点击设备面板底部的喂食录音入口')
            time.sleep(2)
            return True
        except:
            return False

    '''喂食录音编辑界面判断'''
    def mealCallFaceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'mealtime' in self.driver.page_source:
                    logger.info('step4：跳转到喂食录音编辑界面')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeDown()
        else:
            logger.error('step4：当前未处于喂食录音编辑界面，后续用例无法执行')
            return False

    '''在喂食录音编辑界面添加并应用新录音'''
    def addAndApplyNewCall(self):
        self.driver.tap([(0.8703 * self.width, 0.3985 * self.height)], duration=1)
        logger.info('step5：点击Add按钮')
        time.sleep(2)
        self.driver.tap([(0.5111 * self.width, 0.9466 * self.height)], duration=1)
        logger.info('step6：点击开始录制按钮')
        time.sleep(5)
        self.driver.tap([(0.5111 * self.width, 0.9466 * self.height)], duration=1)
        logger.info('step7：点击结束录制按钮')
        time.sleep(2)
        if '202' in self.driver.page_source:
            self.driver.tap([(0.9037 * self.width, 0.7970 * self.height)], duration=1)
            logger.info('step8：点击保存按钮')
            time.sleep(10)
            if '202' in self.driver.page_source:
                self.driver.tap([(0.8851 * self.width, 0.4752 * self.height)], duration=1)
                logger.info('step9：点击应用按钮')
                for i in range(self.mainTimeoutDuration):
                    if 'Success' in self.driver.page_source:
                        time.sleep(5)
                        logger.info('喂食录音应用成功')
                        self.driver.tap([(0.8851 * self.width, 0.4752 * self.height)], duration=1)
                        logger.info('step10：点击取消应用按钮')
                        time.sleep(8)
                        self.driver.tap([(0.5259 * self.width, 0.4714 * self.height)], duration=1)
                        logger.info('step11：点击喂食录音')
                        time.sleep(1.5)
                        self.driver.tap([(0.3935 * self.width, 0.5505 * self.height)], duration=1)
                        logger.info('step11：点击删除按钮')
                        time.sleep(2)
                        self.driver.tap([(0.5287 * self.width, 0.5972 * self.height)], duration=1)
                        logger.info('step12：点击确认删除按钮')
                        time.sleep(2)

                        for i in range(self.mainTimeoutDuration):
                            if 'Success' in self.driver.page_source:
                                logger.info('喂食录音删除成功')
                                break
                            elif 'Fail' in self.driver.page_source:
                                logger.error('喂食录音删除失败，后续用例无法执行')
                                return False
                            else:
                                time.sleep(1)

                        logger.info('Finally：设备添加&应用喂食录音用例执行成功')
                        return True
                    elif 'Fail' in self.driver.page_source:
                        logger.error('喂食录音应用失败，后续用例无法执行')
                        return False
                    else:
                        time.sleep(1)
            logger.error('喂食录音保存失败，后续用例无法执行')
            return False
        else:
            logger.error('喂食录音录制失败，后续用例无法执行')
            return False