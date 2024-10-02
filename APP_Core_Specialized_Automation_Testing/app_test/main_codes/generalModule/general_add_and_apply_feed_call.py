
# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/4 20:05
# @File         : general_add_and_apply_feed_call.py
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


class AddAndApplyFeedCall(object):
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

    '''APP首页点击设备卡片'''
    def clickDeviceCard(self):
        self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1)
        logger.info('step1：点击首页设备卡片')
        time.sleep(2)
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

    '''点击设备面板底部的喂食录音入口'''
    def clickDeviceFaceMealCall(self):
        self.driver.tap([(0.8000 * self.width, 0.9999 * self.height)], duration=1)
        logger.info('step3：点击设备面板底部的喂食录音入口')
        time.sleep(2)
        return True

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
                    self.swipeUp()
        else:
            logger.error('step4：当前未处于喂食录音编辑界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step4：当前未处于喂食录音编辑界面，后续用例无法执行')
            return False

    '''在喂食录音编辑界面添加并应用新录音'''
    def addAndApplyNewCall(self):
        self.driver.tap([(0.8703 * self.width, 0.3985 * self.height)], duration=1)
        logger.info('step5：点击Add按钮')
        time.sleep(2)
        self.driver.tap([(0.5111 * self.width, 0.9466 * self.height)], duration=1)
        logger.info('step6：点击开始录制按钮')
        time.sleep(5)

        self.permissionClick.acceptMicroPermissions()

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
                        logger.info('step12：点击删除按钮')
                        time.sleep(2)
                        self.driver.tap([(0.5287 * self.width, 0.5972 * self.height)], duration=1)
                        logger.info('step13：点击确认删除按钮')
                        time.sleep(2)

                        for i in range(self.mainTimeoutDuration):
                            if 'Success' in self.driver.page_source:
                                logger.info('喂食录音删除成功')
                                break
                            elif 'Fail' in self.driver.page_source:
                                logger.error('Finally：喂食录音删除失败，后续用例无法执行')
                                # self.phoneRecord.stop_screen_recording()
                                send_feishu_text_Message('Finally：喂食录音删除失败，后续用例无法执行')
                                return False
                            else:
                                time.sleep(1)

                        logger.info('Finally：设备添加&应用喂食录音用例执行成功')
                        # self.phoneRecord.stop_screen_recording()
                        return True
                    elif 'Fail' in self.driver.page_source:
                        logger.error('Finally：喂食录音应用失败，后续用例无法执行')
                        # self.phoneRecord.stop_screen_recording()
                        send_feishu_text_Message('Finally：喂食录音应用失败，后续用例无法执行')
                        return False
                    else:
                        time.sleep(1)
            logger.error('Finally：喂食录音保存失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('Finally：喂食录音保存失败，后续用例无法执行')
            return False
        else:
            logger.error('Finally：喂食录音录制失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('Finally：喂食录音录制失败，后续用例无法执行')
            return False
