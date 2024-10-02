# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/8 17:45
# @File         : general_phone_record.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import subprocess
import time
from loguru import logger
from ..generalModule.general_reload_yaml import ReloadYaml


class PhoneRecord(object):
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.phone_record_path = self.reloadYaml.phone_record_path
        self.udid = self.reloadYaml.desired_capabilities['udid']  # 测试手机的固定参数

    def start_screen_recording(self, output_file_name):
        command = f'adb -s {self.udid} shell screenrecord --output-format=h264 --size=2336x1080 --bit-rate=2000000 /storage/emulated/0/DCIM/RECORD/{output_file_name}'
        subprocess.Popen(command, shell=True)  # 执行开始录屏命令
        logger.info('开启手机录屏...')

    def stop_screen_recording(self):
        process_info = subprocess.run(f'adb -s {self.udid} shell pgrep screenrecord', capture_output=True, text=True, shell=True)  # 获取正在录制屏幕的进程ID
        process_output = process_info.stdout.strip().split()
        time.sleep(2)

        process_id = process_output[0]
        subprocess.run(f'adb -s {self.udid} shell kill {process_id}', shell=True)  # 结束录制屏幕的进程
        time.sleep(3)
        command = f'adb shell ls -l {self.phone_record_path}'
        result = subprocess.check_output(command, shell=True)

        if result:
            logger.info('测试录像保存成功')
        else:
            logger.error('未发现任何手机有任何测试录像文件')

