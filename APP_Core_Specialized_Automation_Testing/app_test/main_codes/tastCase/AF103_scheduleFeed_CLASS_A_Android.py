# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 18:35
# @File         : AF103_scheduleFeed_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_login import Login
from ..generalModule.general_schedule_feed import ScheduleFeed
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml


class AF103_scheduleFeed(object):
    def __init__(self):
        '''实例化Login对象login'''
        self.login = Login()

        '''实例化ScheduleFeed对象scheduleFeed'''
        self.scheduleFeed = ScheduleFeed()

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''AF103计划喂食的业务代码'''
    def aF103_scheduleFeed(self):
        if not self.scheduleFeed.mainJudge():  # APP首页判断
            return False

        if not self.scheduleFeed.clickDeviceCard():  # APP首页点击设备卡片
            return False

        if not self.scheduleFeed.deviceFaceJudge():  # 设备面板判断
            return False

        if not self.scheduleFeed.deviceFaceAboutSignalOrDual():  # 点击单/双食盆蒙版的DONE按钮
            return False

        if not self.scheduleFeed.clickDeviceFaceMealCall():  # 点击设备面板底部的计划喂食入口
            return False

        if not self.scheduleFeed.scheduleListFaceJudge():  # 计划总列表界面判断
            return False

        if not self.scheduleFeed.addAndSaveSchedule():  # 添加并保存喂食计划
            return False

        if not self.scheduleFeed.scheduleFeedNumJudge():  # 计划喂食份数判断
            return False
        return True
