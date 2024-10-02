# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:35
@File         : Multi_Language_APP_Copywriting_JSON.py
@Interpreter Version: python 3.12
@Description:
'''

import pandas as pd
import json
from loguru import logger


class InsertWords(object):
    def __init__(self):
        self.df = pd.read_excel(r'C:\Users\leon1\Desktop\0906H5.xlsx')

    def generateJson(self):
        '''将左列以 . 分隔，形成多层字典嵌套'''
        result = {}
        for index, row in self.df.iterrows():
            keys = row['KEY'].split('.')
            value = row['DE']

            '''循环处理每个键'''
            current_dict = result
            for key in keys[:-1]:
                if key not in current_dict:  # 如果当前键不存在于当前字典中，则创建一个新的字典作为该键的值
                    current_dict[key] = {}
                current_dict = current_dict[key]  # 将当前字典更新为该键的值
            current_dict[keys[-1]] = value  # 最后一个键对应的值为右列的值

        with open(r'C:\Users\leon1\Desktop\0906最新H5文案json\H5_DE.json', 'w',
                  encoding='UTF-8') as f:  # 将字典转换为 JSON 格式，并写入文件中
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info('脚本执行完成！')


if __name__ == '__main__':
    insertWords = InsertWords()
    insertWords.generateJson()
