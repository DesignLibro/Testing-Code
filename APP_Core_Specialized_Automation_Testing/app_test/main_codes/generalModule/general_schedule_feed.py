# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 17:51
# @File         : general_schedule_feed.py
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


class ScheduleFeed(object):
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

    def getCurrentMin(self):
        currentMin = time.localtime().tm_min
        return currentMin

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

    def swipeUpHour(self):
        x1 = int(0.4333 * self.width)
        y1 = int(0.3600 * self.height)
        y2 = int(0.2993 * self.height)
        self.swipe(x1, y1, x1, y2, 1000)
        logger.info('正在向下滑动时钟数加1...')

    def swipeUpMin(self):
        x1 = int(0.5611 * self.width)
        y1 = int(0.3788 * self.height)
        y2 = int(0.3050 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)
        logger.info('正在向下滑动分钟数加1...')

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

    '''点击设备面板底部的计划喂食入口'''
    def clickDeviceFaceMealCall(self):
        self.driver.tap([(0.5000 * self.width, 0.9999 * self.height)], duration=1)
        logger.info('step3：点击设备面板底部的计划喂食入口')
        time.sleep(3)
        return True

    '''计划总列表界面判断'''
    def scheduleListFaceJudge(self):
        try:
            for i in range(self.mainTimeoutDuration):
                if 'SCHEDULE' in self.driver.page_source:
                    logger.info('step4：跳转到计划总列表界面')
                    return True
            else:
                logger.error('step4：当前未处于计划总列表界面，后续用例无法执行')
                # self.phoneRecord.stop_screen_recording()
                send_feishu_text_Message('step4：当前未处于计划总列表界面，后续用例无法执行')
                return False
        except:
            logger.error('step4：当前未处于计划总列表界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step4：当前未处于计划总列表界面，后续用例无法执行')
            return False

    '''添加并保存喂食计划'''
    def addAndSaveSchedule(self):
        try:
            self.driver.tap([(0.9212 * self.width, 0.0935 * self.height)], duration=1)
            logger.info('step5：点击计划总列表界面右上角入口')
            for i in range(self.mainTimeoutDuration - 10):
                if 'SCHEDULE' in self.driver.page_source:
                    logger.info('step6：跳转到计划编辑界面')
                    time.sleep(2)
                    if self.getCurrentMin() >= 57:
                        self.swipeUpHour()
                        time.sleep(2)
                        self.swipeUpMin()
                        time.sleep(4)
                    else:
                        self.swipeUpMin()

                    '''设置计划喂食3份'''
                    for i in range(2):
                        self.driver.tap([(0.8870 * self.width, 0.8250 * self.height)], duration=1)
                        time.sleep(2)
                    else:
                        logger.info('step7：设置计划喂食3份')
                        time.sleep(2)
                        self.swipeDown()
                        time.sleep(3)
                        self.driver.tap([(0.4972 * self.width, 0.9429 * self.height)], duration=1)
                        logger.info('step8：点击SAVE按钮')
                        time.sleep(2)
                        for i in range(self.mainTimeoutDuration):
                            if self.scheduleListFaceJudge():
                                break
                            else:
                                time.sleep(1)
                        else:
                            logger.error('当前未处于计划总列表界面，后续用例无法执行')
                            # self.phoneRecord.stop_screen_recording()
                            send_feishu_text_Message('当前未处于计划总列表界面，后续用例无法执行')
                            return False

                        self.driver.tap([(0.0685 * self.width, 0.0944 * self.height)], duration=1)
                        logger.info('step9：点击左上角返回按钮')

                        for i in range(self.mainTimeoutDuration):
                            if self.deviceFaceJudge():
                                break
                            else:
                                time.sleep(1)
                        else:
                            logger.error('当前未处于设备面板，后续用例无法执行')
                            send_feishu_text_Message('当前未处于设备面板，后续用例无法执行')
                            # self.phoneRecord.stop_screen_recording()
                            return False
                        return True
                else:
                    self.swipeUp()
                    time.sleep(1)
            else:
                logger.error('step6：当前未处于计划编辑界面，后续用例无法执行')
                # self.phoneRecord.stop_screen_recording()
                send_feishu_text_Message('step6：当前未处于计划编辑界面，后续用例无法执行')
                return False
        except:
            logger.error('step5：当前未处于计划总列表界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step5：当前未处于计划总列表界面，后续用例无法执行')
            return False

    '''计划喂食份数判断'''
    def scheduleFeedNumJudge(self):  # 适用103、
        try:
            for i in range(self.mainTimeoutDuration * 15):
                if '6/12' in self.driver.page_source:
                    logger.info('Finally：计划喂食3份成功')
                    # self.phoneRecord.stop_screen_recording()
                    return True
                else:
                    self.swipeUp()
                    time.sleep(1)
            else:
                logger.error('Finally：计划喂食3份失败，后续用例无法执行')
                # self.phoneRecord.stop_screen_recording()
                send_feishu_text_Message('Finally：计划喂食3份失败，后续用例无法执行')
                return False
        except:
            logger.error('Finally：计划喂食3份成功')
            return True
