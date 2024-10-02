# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/2/4 15:12
# @File         : AF103_buleboothBindDevice_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_blu_bind_device import BluBindDevice
from ..generalModule.general_build_ota_task import BuildOtaTask
from ..generalModule.general_reload_yaml import ReloadYaml


# class AF103_buleboothBindDevice(General_module):
#     '''继承父类的初始化函数，才能完成后续的父类属性调用'''
#     def __init__(self):
#         super().__init__()  # 调用父类General_module的初始化函数

class AF103_buleboothBindDevice(object):
    def __init__(self):
        '''实例化BluBindDevice对象bluBindDevice'''
        self.bluBindDevice = BluBindDevice()

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.AF103_PRODUCT_NAME = self.reloadYaml.AF103_PRODUCT_NAME

        '''实例化BuildOtaTask对象buildOtaTask'''
        self.buildOtaTask = BuildOtaTask()
        self.buildOtaTask.endOtaTask(self.AF103_PRODUCT_NAME)  # 在运营平台中下架所有的AF103 OTA任务

    '''AF103蓝牙绑定的业务代码'''
    def aF103_buleboothBindDevice(self):
        if not self.bluBindDevice.mainJudge():  # APP首页判断  if not true:
            return False

        if not self.bluBindDevice.clickAddDeviceButton():  # 点击添加设备按钮
            return False

        if not self.bluBindDevice.acceptLocationPermissions():  # 同意授权location权限
            return False

        if not self.bluBindDevice.acceptAPPFindDevicePermissions():  # 同意授权APP发现设备的权限
            return False

        if not self.bluBindDevice.bluetoothDeviceSearchInterfaceJudge():  # 蓝牙搜索设备界面判断
            return False

        if not self.bluBindDevice.bluetoothDeviceSearch():  # 蓝牙搜索设备
            return False

        if not self.bluBindDevice.clickMAC():  # 点击MAC卡片
            return False

        if not self.bluBindDevice.WIFIFaceJudge():  # WIFI信息编辑界面判断
            return False

        if not self.bluBindDevice.inputWIFIInfoAndNext():  # 输入WIFI信息并点击下一步
            return False

        if not self.bluBindDevice.bluetoothDeviceBindingInterfaceJudge():  # 蓝牙绑定设备界面判断
            return False

        if not self.bluBindDevice.bluetoothDeviceBindingResultJudge():  # 蓝牙绑定设备结果判断
            return False

        if not self.bluBindDevice.renameDevice():  # 对设备进行重命名
            return False

        if not self.bluBindDevice.selectSingalOrDual():  # 选择单/双盆
            return False

        if not self.bluBindDevice.skipAF103AlexaDashFace():  # 跳过Alexa Dash页面
            return False

        if not self.bluBindDevice.mainDeviceJudge():  # 首页设备判断
            return False
        return True
