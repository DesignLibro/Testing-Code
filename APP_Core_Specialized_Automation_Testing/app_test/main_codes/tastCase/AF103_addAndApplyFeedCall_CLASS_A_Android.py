# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/2/4 15:12
# @File         : AF103_addAndApplyFeedCall_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_login import Login
from ..generalModule.general_add_and_apply_feed_call import AddAndApplyFeedCall
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml


class AF103_addAndApplyFeedCall(object):
    def __init__(self):
        '''实例化Login对象login'''
        self.login = Login()

        '''实例化AddAndApplyFeedCall对象addAndApplyFeedCall'''
        self.addAndApplyFeedCall = AddAndApplyFeedCall()

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''AF103添加&应用喂食录音的业务代码'''
    def aF103_addAndApplyFeedCall(self):
        if not self.addAndApplyFeedCall.mainJudge():  # APP首页判断
            return False

        if not self.addAndApplyFeedCall.clickDeviceCard():  # APP首页点击设备卡片
            return False

        if not self.addAndApplyFeedCall.deviceFaceAboutSignalOrDual():  # 点击单/双食盆蒙版的DONE按钮
            return False

        if not self.addAndApplyFeedCall.deviceFaceJudge():  # 设备面板判断
            return False

        if not self.addAndApplyFeedCall.clickDeviceFaceMealCall():  # 点击设备面板底部的喂食录音入口
            return False

        if not self.addAndApplyFeedCall.mealCallFaceJudge():  # 喂食录音编辑界面判断
            return False

        if not self.addAndApplyFeedCall.addAndApplyNewCall():  # 在喂食录音编辑界面添加并应用新录音
            return False
        return True

# AF103_addAndApplyFeedCall().aF103_addAndApplyFeedCall()  # 调试本脚本时解除注释