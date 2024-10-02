# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/1 18:21
# @File         : general_reload_yaml.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
import time
import yaml
from loguru import logger


class ReloadYaml(object):
    def main(self):
        current_script_path = os.path.abspath(__file__)  # 获取当前脚本文件的绝对路径
        script_dir = os.path.dirname(current_script_path)  # 获取脚本所在的目录
        os.chdir(script_dir)  # 切换工作目录至脚本所在目录
        time.sleep(2)

        '''读取yaml配置文件'''
        while True:
            with open(file='../../config/config.yaml', mode='r', encoding='UTF-8') as config_file:
                data = yaml.safe_load(config_file)
                if data:
                    break
                if not data:
                    logger.error('读取配置yaml文件失败')

        self.desired_capabilities = data['desired_capabilities']  # 测试手机的固定参数
        self.appPackage = data['desired_capabilities']['appPackage']  # 测试包名
        self.width = data['width']  # 测试手机的长像素
        self.height = data['height']  # 测试手机的宽像素

        self.AF103_MAC = data['AF103_MAC']  # 测试设备的MAC
        self.AF103_NAME = data['AF103_NAME']  # 测试设备的名称
        self.AF103_MODEL = data['AF103_MODEL']  # 测试设备的型号
        self.AF103_PRODUCT_NAME = data['AF103_PRODUCT_NAME']  # AF103产品名称

        self.wifi1 = data['wifi1']  # 测试蓝牙绑定设备的wifi1
        self.passwd1 = data['passwd1']  # 测试蓝牙绑定设备的密码1
        self.mainTimeoutDuration = data['mainTimeoutDuration']  # APP登录成功后在首页的判断超时时间
        self.searchDeviceTimeoutDuration = data['searchDeviceTimeoutDuration']  # 蓝牙搜索设备超时时间
        self.bluetoothBindingDeviceTimeout = data['bluetoothBindingDeviceTimeout']  # 蓝牙绑定设备的超时时间
        self.diyDeviceName = data['diyDeviceName']  # 自定义设备名称
        self.failRetryCount = data['failRetryCount']  # 用例执行失败时的最大尝试次数

        self.user1 = data['user1']  # 测试APP账号1
        self.password1 = data['password1']  # 测试APP密码1

        self.test_environment_operation_platform_account = data['test_environment_operation_platform_account']  # test环境运营平台账号
        self.test_environment_operation_platform_passwd = data['test_environment_operation_platform_passwd']  # test环境运营平台密码
        self.test_operationPlatformLoginTokenURL = data['test_operationPlatformLoginTokenURL']  # test环境运营平台URL
        self.test_getoperationPlatformLMarketingPromotionURL = data['test_getoperationPlatformLMarketingPromotionURL']  # test环境运营平台获取运营推广URL
        self.test_takeDownPopURL = data['test_takeDownPopURL']  # test环境运营平台下架pop弹窗URL
        self.test_operationPlatformLoginTokenAuthority = data['test_operationPlatformLoginTokenAuthority']  # test环境运营平台authority
        self.test_operationPlatformLoginTokenOrigin = data['test_operationPlatformLoginTokenOrigin']  # test环境运营平台origin
        self.test_operationPlatformLoginTokenReferer = data['test_operationPlatformLoginTokenReferer']  # test环境运营平台referer
        self.browser_header = data['browser_header']  # 谷歌浏览器头部
        self.test_getOTATaskListURL = data['test_getOTATaskListURL']  # 获取ota任务列表URL
        self.test_endOTATaskListURL = data['test_endOTATaskListURL']  # 结束ota任务URL
        self.test_getDeviceInfoURL = data['test_getDeviceInfoURL']  # 获取当前设备信息
        self.AF103_HIGH_VERSION = data['AF103_HIGH_VERSION']  # 当前设备对应的最高OTA目标版本
        self.AF103_LOW_VERSION = data['AF103_LOW_VERSION']  # 当前设备对应的最低OTA目标版本
        self.test_deviceOtaSaveURL = data['test_deviceOtaSaveURL']  # 创建OTA任务URL
        self.test_startOTAJobURL = data['test_startOTAJobURL']  # 开启OTA任务URL
        self.test_selectJobItemIDURL = data['test_selectJobItemIDURL']  # 搜索指定设备的JobItemId URL
        self.test_exexuteOTAJobURL = data['test_exexuteOTAJobURL']  #

        '''文件服务器信息'''
        self.server_hostname = data['server_hostname']
        self.server_username = data['server_username']
        self.server_password = data['server_password']
        self.server_remote_path = data['server_remote_path']
        self.server_remote_path_record = data['server_remote_path_record']
        self.directory_path = data['directory_path']
        self.phone_record_path = data['phone_record_path']
        self.url_prefix = data['url_prefix']
        self.test_redis_password = data['test_redis_password']

        '''测试环境数据库信息'''
        self.test_host = data['test_host']
        self.test_port = data['test_port']
        self.test_database = data['test_database']
        self.test_user = data['test_user']
        self.test_password = data['test_password']
        self.test_charset = data['test_charset']
        self.test_redis_port = data['test_redis_port']
