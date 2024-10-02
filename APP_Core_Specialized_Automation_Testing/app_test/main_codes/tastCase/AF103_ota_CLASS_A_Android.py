# -*- coding:utf-8 -*-
import time

# @Author       : baolong.wang
# @Date         : 2024/3/15 10:30
# @File         : AF103_ota_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import time
from packaging import version
from ..generalModule.general_login import Login
from ..generalModule.general_schedule_feed import ScheduleFeed
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_permission_click import PermissionClick
from loguru import logger


class AF103_OTA(object):
    def __init__(self):
        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME
        self.AF103_HIGH_VERSION = self.reloadYaml.AF103_HIGH_VERSION
        self.AF103_LOW_VERSION = self.reloadYaml.AF103_LOW_VERSION
        self.AF103_MAC = self.reloadYaml.AF103_MAC
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''根据当前版本号来决定是升级还是降级'''
    def judgeOTADirection(self):
        try:
            a = version.parse(self.buildOtaTask.getCurretntDeviceVersion(self.AF103_MAC))  # 设备的当前版本
            b = version.parse(self.buildOtaTask.AF103_HIGH_VERSION)  # 最高目标版本
            c = version.parse(self.buildOtaTask.AF103_LOW_VERSION)  # 最低目标版本
            if a == b:
                # 降级
                logger.info(f'正在创建降级到{self.AF103_LOW_VERSION}版本的OTA任务')
                self.buildOtaTask.startOTAJob(self.AF103_PRODUCT_NAME, self.AF103_MAC, self.AF103_LOW_VERSION)
            elif a == c:
                # 升级
                logger.info(f'正在创建升级到{self.AF103_HIGH_VERSION}版本的OTA任务')
                self.buildOtaTask.startOTAJob(self.AF103_PRODUCT_NAME, self.AF103_MAC, self.AF103_HIGH_VERSION)
            return True
        except:
            return False


    '''AF103 OTA的业务代码'''
    def aF103_OTA(self):
        if not self.judgeOTADirection():  # 创建升/降级OTA任务
            return False

        if not self.buildOtaTask.mainJudge():  # APP首页判断
            return False

        if not self.buildOtaTask.clickDeviceCard():  # APP首页点击设备卡片
            return False

        if not self.buildOtaTask.deviceFaceAboutSignalOrDual():  # 点击单/双食盆蒙版的DONE按钮
            return False

        if not self.buildOtaTask.otaFaceJudge():  # OTA弹窗判断
            return False

        if not self.buildOtaTask.clickOTAButton():  # 点击确认升级按钮
            return False

        if not self.buildOtaTask.otaWebJudge():  # OTA界面判断
            return False

        if not self.buildOtaTask.otaResultJudge():  # 监控OTA结果
            return False

        return True


