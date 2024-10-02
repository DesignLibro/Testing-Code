# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 17:28
# @File         : AF103_manualFeed_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_login import Login
from ..generalModule.general_manual_feed import ManualFeed
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml


class AF103_manualFeed(object):
    def __init__(self):
        '''实例化Login对象login'''
        self.login = Login()

        '''实例化ManualFeed对象manualFeed'''
        self.manualFeed = ManualFeed()

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''AF103手动喂食的业务代码'''
    def aF103_manualFeed(self):
        if not self.manualFeed.mainJudge():  # APP首页判断
            return False

        if not self.manualFeed.clickDeviceCard():  # APP首页点击设备卡片
            return False

        if not self.manualFeed.deviceFaceJudge():  # 设备面板判断
            return False

        if not self.manualFeed.deviceFaceAboutSignalOrDual(): # 103设备面板单/双盆蒙版判断
            return False

        if not self.manualFeed.clickDeviceFaceMealCall():  # 点击设备面板底部的手动喂食入口
            return False

        if not self.manualFeed.manualFeedFaceJudge():  # 手动喂食弹框判断
            return False

        if not self.manualFeed.setManualFeed30g():  # 设置手动喂食3份
            return False

        if not self.manualFeed.clickFeedNowButton():  # 点击Feed Now按钮
            return False

        if not self.manualFeed.manualFeedNumJudge():  # 手动喂食份数判断
            return False
        return True
