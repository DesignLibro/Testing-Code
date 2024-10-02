# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 16:55
# @File         : general_manual_feed.py
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


class ManualFeed(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.width = reload_yaml.width  # 测试手机的长像素
        self.height = reload_yaml.height  # 测试手机的宽像素
        self.mainTimeoutDuration = reload_yaml.mainTimeoutDuration  # APP登录成功后在首页的判断超时时间

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

    '''APP首页点击设备卡片'''
    def clickDeviceCard(self):
        self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1)
        logger.info('step1：点击首页设备卡片')
        return True

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
                    self.swipeUp()
        else:
            logger.error('step2：当前未处于设备面板，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step2：当前未处于设备面板，后续用例无法执行')
            return False

    '''点击单/双食盆蒙版的DONE按钮'''
    def deviceFaceAboutSignalOrDual(self):
        time.sleep(5)
        self.driver.tap([(0.0777 * self.width, 0.5037 * self.height)], duration=1)
        time.sleep(2)
        logger.info('点击单/双食盆蒙版的DONE按钮')
        return True

    '''点击设备面板底部的手动喂食入口'''
    def clickDeviceFaceMealCall(self):
        self.driver.tap([(0.2083 * self.width, 0.9999 * self.height)], duration=1)
        logger.info('step3：点击设备面板底部的手动喂食入口')
        time.sleep(2)
        return True

    '''手动喂食弹框判断'''
    def manualFeedFaceJudge(self):  # 适用103、
        for i in range(self.mainTimeoutDuration-15):
            if self.driver.page_source:
                if 'FEEDING AMOUNT' in self.driver.page_source:
                    logger.info('step4：打开手动喂食弹框')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step4：当前未打开手动喂食弹框，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step4：当前未打开手动喂食弹框，后续用例无法执行')
            return False

    '''设置手动喂食3份'''
    def setManualFeed30g(self):  # 适用103、
        time.sleep(3)
        for i in range(2):
            self.driver.tap([(0.8898 * self.width, 0.7680 * self.height)], duration=1)
            time.sleep(2)
        logger.info('step5：设置手动喂食3份')
        return True

    '''点击Feed Now按钮'''
    def clickFeedNowButton(self):  # 适用103、
        self.driver.tap([(0.5018 * self.width, 0.8844 * self.height)], duration=1)
        logger.info('step6：点击Feed Now按钮')
        return True

    '''手动喂食份数判断'''
    def manualFeedNumJudge(self):  # 适用103、
        try:
            for i in range(self.mainTimeoutDuration+40):
                if '3/12' in self.driver.page_source:
                    logger.info('Finally：手动喂食3份成功')
                    # self.phoneRecord.stop_screen_recording()
                    return True
                else:
                    self.swipeUp()
                    time.sleep(1)
            else:
                logger.error('Finally：手动喂食3份失败，后续用例无法执行')
                # self.phoneRecord.stop_screen_recording()
                send_feishu_text_Message('Finally：手动喂食3份失败，后续用例无法执行')
                return False
        except:
            logger.error('Finally：手动喂食3份失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('Finally：手动喂食3份失败，后续用例无法执行')
            return False
