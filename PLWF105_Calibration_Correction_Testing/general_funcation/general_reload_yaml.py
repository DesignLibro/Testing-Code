# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/1 15:48
@File         : general_reload_yaml.py
@Interpreter Version: python 3.12
@Description:
'''


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
            with open(file='../config/config.yaml', mode='r', encoding='UTF-8') as config_file:
                data = yaml.safe_load(config_file)
                if data:
                    break
                if not data:
                    logger.error('读取配置yaml文件失败')

        self.mqtt_env = data['mqtt_environment']  # demo mqtt模拟环境url，可修改为test
        self.mqtt_port = data['mqtt_port']  # mqtt端口号
        self.keepalive = data['keepalive']  # 与代理通信之间允许的最长时间段（以秒为单位）
        self.qos = data['qos']
        self.WF105_USERNAME = data['WF105_USERNAME']
        self.WF105_PASSWD = data['WF105_PASSWD']

        self.WF105_SN = data['WF105_SN']
        self.WF105_WEIGHT_PERCENT = data['WF105_WEIGHT_PERCENT']


