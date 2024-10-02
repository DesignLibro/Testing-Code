# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/2 14:44
# @File         : general_permission_click.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import time
from loguru import logger
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_launch_apk import LaunchAPK


class PermissionClick(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.width = reload_yaml.width  # 测试手机的长像素
        self.height = reload_yaml.height  # 测试手机的宽像素

    def runInstallAPK(self):
        '''实例化LaunchAPK对象launchAPK'''
        launchAPK = LaunchAPK()
        launchAPK.run()  # 安装apk

    def runGetDriver(self):
        '''实例化LaunchAPK对象launchAPK'''
        launchAPK = LaunchAPK()
        launchAPK.main()
        self.driver = launchAPK.driver  # driver对象代表了与设备或模拟器的连接，并提供了与应用程序进行交互的方法和属性。它可以被视为一个句柄（handle），用于操作应用程序界面的元素、执行操作和获取应用程序的状态
        return self.driver

    '''同意隐私政策'''
    def agreePrivacyPolicy(self):
        try:
            if self.driver.page_source:
                if 'AGREE AND CONTINUE' in self.driver.page_source:
                    self.driver.tap([(0.5314 * self.width, 0.8157 * self.height)], duration=1)
                    logger.info('点击同意隐私政策按钮')
                    return True
                else:
                    return True
            else:
                return True
        except:
            return False

    '''不允许petlibro app通知'''
    def notAllowAPPNotification(self):
        self.driver.tap([(0.5037 * self.width, 0.6796 * self.height)], duration=1)
        logger.info('点击不允许petlibro app通知按钮')
        return True

    '''允许petlibro app通知'''
    def allowAPPNotification(self):
        time.sleep(3)
        self.driver.tap([(0.5296 * self.width, 0.6047 * self.height)], duration=1)
        logger.info('点击允许petlibro app通知按钮')
        return True

    '''同意麦克风权限'''
    def acceptMicroPermissions(self):
        time.sleep(3)
        self.driver.tap([(0.4953 * self.width, 0.5678 * self.height)], duration=1)
        logger.info('点击允许petlibro app record audio按钮')
        return True
