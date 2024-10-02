# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/1 18:16
# @File         : general_blu_bind_device.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
import re
import time
from loguru import logger
from ..generalModule.general_permission_click import PermissionClick
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_login import Login
from ..generalModule.general_take_down_pop import TakeDownPOP
from ..generalModule.general_phone_record import PhoneRecord
from feishu_send_message import send_feishu_text_Message


class BluBindDevice(object):
    def __init__(self, ):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.wifi1 = reload_yaml.wifi1  # 测试wifi名称1
        self.passwd1 = reload_yaml.passwd1  # 测试wifi密码1
        self.mainTimeoutDuration = reload_yaml.mainTimeoutDuration  # APP登录成功后在首页的判断超时时间
        self.failRetryCount = reload_yaml.failRetryCount  # 用例执行失败时的最大尝试次数
        self.searchDeviceTimeoutDuration = reload_yaml.searchDeviceTimeoutDuration  # 蓝牙搜索设备超时时间
        self.AF103_MAC = reload_yaml.AF103_MAC  # 测试设备的MAC
        self.AF103_MODEL = reload_yaml.AF103_MODEL  # 测试设备的型号
        self.AF103_NAME = reload_yaml.AF103_NAME  # 测试设备的名称
        self.bluetoothBindingDeviceTimeout = reload_yaml.bluetoothBindingDeviceTimeout  # 蓝牙绑定设备的超时时间
        self.diyDeviceName = reload_yaml.diyDeviceName  # 自定义设备名称
        self.width = reload_yaml.width  # 测试手机的长像素
        self.height = reload_yaml.height  # 测试手机的宽像素

        '''实例化Login对象login'''
        self.login = Login()

        '''实例化PermissionClick对象permissionClick'''
        self.permissionClick = PermissionClick()
        self.driver = self.permissionClick.runGetDriver()

        '''实例化TakeDownPOP对象takeDownPOP'''
        self.takeDownPOP = TakeDownPOP()
        self.takeDownPOP.takeDownoperationalPromotionPopup()

        '''获取当前脚本文件'''
        self.file_path = os.path.abspath(__file__)  # 获取当前脚本的文件名（包括路径）
        self.file_name = os.path.basename(self.file_path)  # 获取文件名和扩展名
        self.file_name_without_extension = os.path.splitext(self.file_name)[0]

        '''实例化PhoneRecord对象phoneRecord'''
        self.recordName = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        self.output_file_name = f'record_{self.file_name_without_extension}_{self.recordName}.mp4'
        self.phoneRecord = PhoneRecord(self.output_file_name)
        # self.phoneRecord.start_screen_recording(self.output_file_name)
        
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    '''控制手机屏幕上滑'''
    def swipeUp(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.1498 * self.height)
        y2 = int(0.9855 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    '''控制手机屏幕下滑'''
    def swipeDown(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

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
                    self.swipeUp()
        else:
            logger.error('step1：当前APP未处于设备首页，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step1：当前APP未处于设备首页，后续用例无法执行')
            return False

    '''点击添加设备按钮'''
    def clickAddDeviceButton(self):
        time.sleep(2)
        self.driver.tap([(0.8861 * self.width, 0.0865 * self.height)], duration=1)
        logger.info('step2：点击添加设备按钮')
        return True

    '''同意授权location权限(While using the app)'''
    def acceptLocationPermissions(self):
        time.sleep(3)
        self.driver.tap([(0.4833 * self.width, 0.6468 * self.height)], duration=1)
        logger.info('点击同意授权location权限')
        return True

    '''同意授权APP发现设备的权限'''
    def acceptAPPFindDevicePermissions(self):
        time.sleep(2)
        self.driver.tap([(0.4925 * self.width, 0.6361 * self.height)], duration=1)
        logger.info('点击同意授权APP发现设备的权限')
        return True

    '''蓝牙搜索设备界面判断'''
    def bluetoothDeviceSearchInterfaceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'ADD DEVICE' in self.driver.page_source:
                    logger.info('step3：蓝牙搜索指定设备中...')
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step3：当前APP未处于蓝牙搜索设备界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step3：当前APP未处于蓝牙搜索设备界面，后续用例无法执行')
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
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'step4：重试蓝牙搜索指定{self.AF103_MODEL}设备{self.AF103_MAC}超时{self.searchDeviceTimeoutDuration}S，后续用例无法执行')
            return False

    '''点击MAC卡片'''
    def clickMAC(self):
        mainText = re.findall(r'MAC:(\S+)', self.driver.page_source)
        mainTextNew = [i.replace('"', '') for i in mainText]
        for text in mainTextNew:
            if self.AF103_MAC == text:
                index = mainTextNew.index(text)
                time.sleep(2)
                bound = re.findall(
                    rf'package="com.designlibro.petlibro" class="android.widget.ImageView" text="" content-desc="{self.AF103_NAME}&#10;MAC:{self.AF103_MAC}" resource-id="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
                    self.driver.page_source)
                self.driver.tap([(int((bound[0][2])) / self.width * self.width - 26,
                                  int((bound[0][3])) / self.height * self.height - 120)], duration=1)
                logger.info('step5：点击设备MAC卡片，进入输入WIFI信息界面')
                return True
        else:
            # self.phoneRecord.stop_screen_recording()
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
                    self.swipeUp()
        else:
            logger.error(f'step6：当前APP未处于输入WIFI信息界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'step6：当前APP未处于输入WIFI信息界面，后续用例无法执行')
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
            # self.phoneRecord.stop_screen_recording()
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
                    self.swipeUp()
        else:
            logger.error(f'step14：当前APP未处于蓝牙绑定设备界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'step14：当前APP未处于蓝牙绑定设备界面，后续用例无法执行')
            return False

    '''蓝牙绑定设备结果判断'''
    def bluetoothDeviceBindingResultJudge(self):
        for y in range(self.failRetryCount):  # 尝试
            for i in range(self.bluetoothBindingDeviceTimeout):
                if self.driver.page_source:
                    if 'success' in self.driver.page_source:
                        logger.info(
                            f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}成功，需在首页进一步验证是否绑定成功')
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
                                    logger.error(
                                        f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}失败，后续用例无法执行')
                                    # self.phoneRecord.stop_screen_recording()
                                    send_feishu_text_Message(f'step15：蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}失败，后续用例无法执行')
                                    return False
                            else:
                                time.sleep(1)
                    else:
                        time.sleep(1)
        else:
            logger.error(f'step15：重试蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}超时{self.bluetoothBindingDeviceTimeout}S失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'step15：重试蓝牙绑定{self.AF103_MODEL}设备{self.AF103_MAC}超时{self.bluetoothBindingDeviceTimeout}S失败，后续用例无法执行')
            return False

    '''对设备进行重命名'''
    def renameDevice(self):
        try:
            time.sleep(2)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText').click()
            logger.info(f'step16：点击设备命名输入栏')

            time.sleep(1)
            self.driver.tap([(0.8638 * self.width, 0.5668 * self.height)], duration=1)
            logger.info(f'step17：点击一键删除设备名称按钮')

            time.sleep(1)
            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText').send_keys(self.diyDeviceName)
            logger.info(f'step18：输入自定义设备名称 {self.diyDeviceName}')
            time.sleep(2)

            self.driver.tap([(0.5111 * self.width, 0.9663 * self.height)], duration=1)
            logger.info(f'step19：点击GET STARTED按钮')
            return True
        except:
            # self.phoneRecord.stop_screen_recording()
            return False

    # '''点击AF103设备的one last step'''
    # def skipAF103OneLastStep(self):
    #     try:
    #         time.sleep(3)
    #         self.driver.tap([(0.8805 * self.width, 0.9900 * self.height)], duration=1)
    #         logger.info(f'step20：AF103设备的one last step页面点击下一步')
    #         return True
    #     except:
    #         self.phoneRecord.stop_screen_recording()
    #         return False

    '''选择单/双盆'''
    def selectSingalOrDual(self):
        time.sleep(3)
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'TRAY' in self.driver.page_source:
                    self.driver.tap([(0.2314 * self.width, 0.5130 * self.height)], duration=1)
                    time.sleep(2)
                    self.driver.tap([(0.5250 * self.width, 0.9677 * self.height)], duration=1)
                    logger.info('选择单盆并确认')
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
            else:
                time.sleep(1)
                self.swipeUp()
        else:
            logger.error('未跳转到单/双盆选择页面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('未跳转到单/双盆选择页面，后续用例无法执行')
            return False

    '''跳过Alexa Dash页面'''
    def skipAF103AlexaDashFace(self):
        time.sleep(3)
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Smart Reordering' in self.driver.page_source:
                    self.driver.tap([(0.9166 * self.width, 0.0902 * self.height)], duration=1)
                    logger.info(f'step21：跳过AF103设备的Alexa Dash页面')
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
            else:
                time.sleep(1)
                self.swipeUp()
        else:
            logger.error('step20：未跳转到Alexa Dash页面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step20：未跳转到Alexa Dash页面，后续用例无法执行')
            return False

    '''首页设备判断'''
    def mainDeviceJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if self.diyDeviceName in self.driver.page_source:
                    logger.info(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}蓝牙绑定成功')
                    # self.phoneRecord.stop_screen_recording()
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}蓝牙绑定，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}蓝牙绑定，后续用例无法执行')
            return False
