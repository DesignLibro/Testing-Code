# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/2 14:32
# @File         : general_launch_apk.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from loguru import logger
from appium import webdriver
from ..generalModule.general_install_apk import InstallAPK
from ..generalModule.general_reload_yaml import ReloadYaml


class LaunchAPK(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.desired_capabilities = reload_yaml.desired_capabilities  # 测试手机的固定参数

    def run(self):
        # InstallAPK(package_path=r'C:\Users\leon1\Desktop\PETLIBRO_1.3.20.apk').main()
        InstallAPK(package_path=r'/Users/dl/Desktop/apks/test_petlibro_V1.3.30_1_安卓_dev_9721c6f72.apk').main()

    def main(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        logger.info('启动APP...')
