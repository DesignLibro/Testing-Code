# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 16:31
# @File         : general_unbind_device.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
import time
from loguru import logger
from ..generalModule.general_take_down_pop import TakeDownPOP
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_permission_click import PermissionClick
from ..generalModule.general_phone_record import PhoneRecord
from feishu_send_message import send_feishu_text_Message


class UnbindDevice(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.width = reload_yaml.width  # 测试手机的长像素
        self.height = reload_yaml.height  # 测试手机的宽像素
        self.mainTimeoutDuration = reload_yaml.mainTimeoutDuration  # APP登录成功后在首页的判断超时时间
        self.failRetryCount = reload_yaml.failRetryCount  # 用例执行失败时的最大尝试次数
        self.diyDeviceName = reload_yaml.diyDeviceName  # 自定义设备名称
        self.AF103_MODEL = reload_yaml.AF103_MODEL  # 测试设备的型号
        self.AF103_MAC = reload_yaml.AF103_MAC  # 测试设备的MAC

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

    '''APP首页长按解绑设备卡片'''
    def longPressDeviceCard(self):
        self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1500)
        logger.info('step2：APP首页长按设备卡片')

        time.sleep(1)
        self.driver.tap([(0.9009 * self.width, 0.3255 * self.height)], duration=1)
        logger.info('step3：点击删除设备卡片按钮')

        time.sleep(1)
        self.driver.tap([(0.5222 * self.width, 0.6314 * self.height)], duration=1)
        logger.info('step4：点击确认删除设备卡片按钮')
        time.sleep(2)
        return True

    '''解绑设备验证'''
    def unbindDeviceJudge(self):
        for y in range(self.failRetryCount):  # 尝试
            for i in range(self.mainTimeoutDuration):
                if self.driver.page_source:
                    if self.diyDeviceName not in self.driver.page_source:
                        logger.info(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行成功')
                        # self.phoneRecord.stop_screen_recording()
                        return True
                    elif self.diyDeviceName in self.driver.page_source:
                        logger.error(f'{self.AF103_MODEL}设备{self.AF103_MAC}解绑失败，重试解绑步骤')
                        self.longPressDeviceCard()

                        for i in range(self.mainTimeoutDuration):
                            if self.driver.page_source:
                                if self.diyDeviceName not in self.driver.page_source:
                                    logger.info(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行成功')
                                    # self.phoneRecord.stop_screen_recording()
                                    return True
                                elif self.diyDeviceName in self.driver.page_source:
                                    logger.error(
                                        f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}重试解绑失败，后续用例无法执行')
                                    # self.phoneRecord.stop_screen_recording()
                                    send_feishu_text_Message(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}重试解绑失败，后续用例无法执行')
                                    return False
                            else:
                                time.sleep(1)
                                self.swipeUp()
                                time.sleep(2)
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'Finally：{self.AF103_MODEL}设备{self.AF103_MAC}解绑设备用例执行失败，后续用例无法执行')
            return False
