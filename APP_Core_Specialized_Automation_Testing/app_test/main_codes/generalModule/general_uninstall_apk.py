# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/2 19:27
# @File         : general_uninstall_apk.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import subprocess
from loguru import logger
from ..generalModule.general_reload_yaml import ReloadYaml


class UninstallAPK(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.appPackage = reload_yaml.appPackage
        self.udid = reload_yaml.desired_capabilities['udid']

    def mian(self):
        # 检查应用程序是否已安装，若有则卸载
        check_cmd = f'adb -s {self.udid} shell pm list packages {self.appPackage}'
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        if self.appPackage in result.stdout:
            # 卸载应用程序
            uninstall_cmd = f'adb -s {self.udid} uninstall {self.appPackage}'
            subprocess.run(uninstall_cmd, shell=True)
            logger.info(f'已卸载应用程序包名: {self.appPackage}')
        else:
            logger.info(f'当前测试手机未存在指定程序包名{self.appPackage}')

# UninstallAPK().mian()  # 调试本脚本时解除注释
