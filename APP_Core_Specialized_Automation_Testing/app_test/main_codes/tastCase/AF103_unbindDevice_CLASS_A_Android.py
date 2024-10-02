# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/5 16:38
# @File         : AF103_unbindDevice_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_login import Login
from ..generalModule.general_unbind_device import UnbindDevice
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml


class AF103_unbindDevice(object):
    def __init__(self):
        '''实例化Login对象login'''
        self.login = Login()

        '''实例化UnbindDevice对象unbindDevice'''
        self.unbindDevice = UnbindDevice()

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''AF103解绑设备的业务代码'''
    def aF103_unbindDevice(self):
        if not self.unbindDevice.mainJudge():  # APP首页判断
            return False

        if not self.unbindDevice.longPressDeviceCard():  # APP首页长按解绑设备卡片
            return False

        if not self.unbindDevice.unbindDeviceJudge():  # 解绑设备验证
            return False
        return True
