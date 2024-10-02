# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/7 10:46
# @File         : generate_report.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
from datetime import datetime
from loguru import logger
from fabric import Connection
from feishu_send_message import send_feishu_text_Message
from lucky_code.designlibro_codes.main_codes.generalModule.general_reload_yaml import ReloadYaml
from lucky_code.designlibro_codes.main_codes.generalModule.general_record_to_computer_upload_server import GeneralRecordToComputer


class GenerateReport(object):
    def __init__(self):
        '''实例化对象ReloadYaml为reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.server_hostname = self.reloadYaml.server_hostname
        self.server_username = self.reloadYaml.server_username
        self.server_password = self.reloadYaml.server_password
        self.server_remote_path = self.reloadYaml.server_remote_path

    def getReportFileName(self):
        # report_dir = r'C:\Users\leon1\PycharmProjects\appautoarichiverscript\lucky_code\designlibro_codes\main_codes\report'  # windows电脑中report目录路径
        report_dir = r'/Users/dl/Robert/script/lucky_code/designlibro_codes/main_codes/report'  # mac电脑中report目录路径
        files = os.listdir(report_dir)  # 获取 report 目录下的所有文件

        # 过滤出以 "Automation_Test_Report_" 开头且以 ".html" 结尾的文件
        html_files = [file for file in files if file.startswith("Automation_Test_Report_") and file.endswith(".html")]

        # 按文件名中的时间戳进行排序
        sorted_files = sorted(html_files, key=lambda x: datetime.strptime(x.replace("Automation_Test_Report_", "").replace(".html", ""), "%Y-%m-%d_%H-%M-%S"), reverse=True)  # 适用于 'YYYY-MM-DD_HH-MM-SS' 格式

        # 获取最新的 HTML 文件
        if sorted_files:
            self.newest_html_file = sorted_files[0]
            logger.info(f'最新时间的 HTML 文件是:{self.newest_html_file}')
            return self.newest_html_file
        else:
            logger.info('report 目录中没有 HTML 文件')
            return None

    def send_report_to_feishu(self):
        local_file_path = rf'../report/{self.getReportFileName()}'  # 本地源文件路径
        try:
            # 建立SSH连接
            with Connection(host=self.server_hostname, user=self.server_username, connect_kwargs={"password": self.server_password}) as conn:
                logger.info('SSH连接成功')

                conn.put(local=local_file_path, remote=self.server_remote_path)  # 执行SCP上传

                logger.info(f'{local_file_path} Html报告上传服务器成功')
                send_feishu_text_Message(
                    f'新包自动化测试已完成，详见在线测试报告：{"https://source.dl-aiot.com/test/" + self.newest_html_file}')
                # GeneralRecordToComputer().uploadRecord()
        except Exception as e:
            logger.error(str(e))


if __name__ == '__main__':
    GenerateReport().send_report_to_feishu()
