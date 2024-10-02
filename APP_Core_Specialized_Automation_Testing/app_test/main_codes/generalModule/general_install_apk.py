# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/1 17:36
# @File         : general_install_apk.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
import time
import subprocess
from loguru import logger
from ..generalModule.general_uninstall_apk import UninstallAPK
from feishu_send_message import send_feishu_text_Message
from ..generalModule.general_reload_yaml import ReloadYaml


class InstallAPK(object):
    def __init__(self, package_path):
        self.package_path = package_path

        '''实例化UninstallAPK对象uninstallAPK'''
        uninstallAPK = UninstallAPK()
        uninstallAPK.mian()

        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.udid = reload_yaml.desired_capabilities['udid']  # 测试手机的固定参数

    def main(self):
        while True:
            try:
                logger.info('正在安装Android APK...')
                process = subprocess.run(['adb', '-s', f'{self.udid}', 'install', '-r', self.package_path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

                '''检查安装结果'''
                if process.returncode == 0:
                    logger.info(f'{self.package_path} 安装成功')
                    break
                else:
                    logger.error(f'{self.package_path} 安装失败')
                    logger.error(process.stdout.decode())
                    logger.error(process.stderr.decode())
            except Exception as error:
                send_feishu_text_Message(f'安装APK包{self.package_path} 时发生错误：{error}，重试安装...')
                logger.error(f'安装APK包{self.package_path} 时发生错误：{error}，重试安装...')

# InstallAPK(package_path=r'C:\Users\leon1\Desktop\PETLIBRO_1.3.10.apk').main()  # 调试本脚本时解除注释
