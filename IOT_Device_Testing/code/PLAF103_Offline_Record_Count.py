# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:41
@File         : PLAF103_Offline_Record_Count.py
@Interpreter Version: python 3.12
@Description: 1. 2022/12/13  修改离线日志关键字为：mqtt:addr =
'''

import time
import re
from loguru import logger
from pathlib import Path


class OfflineVisualization(object):
    def __init__(self, mode, src_folder, folderSearchMode, des_folder):
        self.mode = mode  # 单/多个log文件处理
        self.folderSearchMode = folderSearchMode  # log目录的查找模式：当前、递归
        self.src_folder = src_folder  # 处理目录/文件路径
        self.des_folder = des_folder  # 存储目录
        self.newLogFileName = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())  # 合并后的log文件名
        self.newLogPath = rf'{self.des_folder}\{self.newLogFileName}合并.log'  # 合并后的log目录
        self.keyWord = 'mqtt:addr = '
        self.count_key = 0
        self.keyTimeList, self.offlineList = [], []

    def getFiles(self):
        if self.folderSearchMode == '1':  # 当前目录
            filesList = Path(self.src_folder).glob('*.log')
        elif self.folderSearchMode == '2':  # 递归目录
            filesList = Path(self.src_folder).rglob('*.log')
        else:
            return None
        return filesList

    def mergeFiles(self):
        newLogFile = open(self.newLogPath, mode='ab')
        for file in self.getFiles():
            with open(rf'{str(file)}', mode='rb') as f:
                data = f.read()
                newLogFile.write(data)
                newLogFile.write(b'\n')
        else:
            f.close()
            newLogFile.close()
            logger.info('log内容合并完成！')

    def logFiles(self):
        if self.mode == '1':  # 1.多log文件处理
            self.mergeFiles()
            log = open(self.newLogPath, mode='r', encoding='latin1')
        elif self.mode == '2':  # 2.单log文件处理
            log = open(self.src_folder, mode='r', encoding='latin1')
        return log

    def includeKeyWordLog(self):
        for line in self.logFiles().readlines():
            if line.count(self.keyWord) > 0:  # 关键字1
                self.count_key += line.count(self.keyWord)
                keyLogTime = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}:\d{3})', line)
                if keyLogTime:
                    keyLogTime = str(keyLogTime.group())
                    self.keyTimeList.append(keyLogTime)
        if self.count_key:
            logger.info(f'出现关键字：{self.keyWord} 的次数为：{self.count_key}')
            f = open(rf'{self.des_folder}\离线序号与测试时间对应表.txt', mode='w')
            for x, y in zip(range(1, len(self.keyTimeList) + 1), self.keyTimeList):
                text = f'第{x}次----恢复离线的时间为：{y}'
                f.write(text)
                f.write('\n')
            else:
                f.close()
                logger.info('测试时间写入文件并保存成功！')
        else:
            logger.info('log中不存在离线记录！')

    def main(self):
        self.includeKeyWordLog()


if __name__ == '__main__':
    logger.info('''
        1. 该工具可以处理单个log文件，处理多个log文件时，会将所有的log内容拼接在一起；
        2. 可以只查询当前的log文件目录，也可以实现递归查询；
        3. 在log文件中查找指定关键字，获取当前的时间戳、离线次数；
        ''')
    logger.info('-' * 155)
    time.sleep(0.5)

    while True:
        mode = input('请选择处理方式：1.多log文件处理  2.单log文件处理----').strip()
        if mode == '1' or mode == '2':
            mode = mode
        else:
            logger.info('该处理方式不存在，请重新输入！')
            continue

        if mode == '2':
            logger.info('如果是单log文件处理，下面输入该log文件绝对路径！')
        time.sleep(0.5)

        src_folder = input(r'请输入要处理的log目录路径/文件路径：----').strip()
        if not Path(src_folder).exists():
            logger.info('该log目录路径/文件路径不存在，请重新输入！')
            continue

        folderSearchMode = input('请输入log文件目录的查找模式：1.当前目录  2.递归目录----').strip()
        folderSearchMode = folderSearchMode if folderSearchMode == '1' or folderSearchMode == '2' else logger.info(
            '该目录查找模式不存在！')

        des_folder = input('请输入处理后的文件保存路径：例：D:\desktop----').strip()
        if not Path(des_folder).exists():
            logger.info('该存储文件路径不存在，正在创建...')
            Path(des_folder).mkdir()

        try:
            offlineVisualization = OfflineVisualization(mode, src_folder, folderSearchMode, des_folder)
            offlineVisualization.main()
        except Exception as error:
            logger.info('An exception happened: \n' + str(error))
            logger.info('执行报错，重新执行脚本...')
