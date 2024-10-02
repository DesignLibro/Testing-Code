# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/10 15:16
# @File         : general_record_to_computer_upload_server.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
import subprocess
import time

from loguru import logger
from fabric import Connection
from lucky_code.designlibro_codes.main_codes.generalModule.general_reload_yaml import ReloadYaml
from feishu_send_message import send_feishu_text_Message


class GeneralRecordToComputer(object):
    def __init__(self):
        '''实例化对象ReloadYaml为reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.server_hostname = self.reloadYaml.server_hostname
        self.server_username = self.reloadYaml.server_username
        self.server_password = self.reloadYaml.server_password
        self.server_remote_path_record = self.reloadYaml.server_remote_path_record
        self.directory_path = self.reloadYaml.directory_path
        self.phone_record_path = self.reloadYaml.phone_record_path
        self.url_prefix = self.reloadYaml.url_prefix

    '''从手机中下载录像文件到电脑，并删除源文件'''
    def downloadRecord(self):
        subprocess.run(['adb', 'pull', self.phone_record_path, self.directory_path])  # 使用 adb 命令执行文件传输操作
        time.sleep(2)

        if os.path.exists(self.directory_path):
            logger.info('手机录像文件下载成功')

            subprocess.run(['adb', 'shell', 'rm', '-rf', self.phone_record_path])  # 使用 adb 命令删除手机上的文件及目录
            time.sleep(2)
            subprocess.run(['adb', 'shell', 'mkdir', self.phone_record_path])  # 使用 adb 命令再次创建空目录
            logger.info('手机录像文件从手机删除成功')
        else:
            logger.info('手机录像文件下载失败')

    '''获取电脑中以record_开头，.mp4为后缀的文件绝对路径'''
    def getRecordList(self, directory):
        self.record_mp4_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('record_') and file.endswith('.mp4'):
                    file_path = os.path.join(root, file)
                    self.record_mp4_files.append(file_path)
        return self.record_mp4_files

    def uploadRecord(self):
        self.downloadRecord()
        try:
            # 建立SSH连接
            with Connection(host=self.server_hostname, user=self.server_username, connect_kwargs={"password": self.server_password}) as conn:
                logger.info('SSH连接成功')
            for record in self.getRecordList(self.directory_path):
                conn.put(local=record, remote=self.server_remote_path_record)  # 执行SCP上传
                logger.info('手机录像上传服务器成功')
                os.remove(record)
                logger.info('录像文件从本地删除成功')
                recordLink = record.split("\\")[-1]
                send_feishu_text_Message(f'手机录像上传服务器成功，访问地址为 -- {self.url_prefix + recordLink}，需在浏览器上另存为该视频文件，在电脑本地查看')
        except Exception as e:
            logger.error(str(e))


# GeneralRecordToComputer().uploadRecord()  # 调试本脚本时打开注释
