# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 12:04
@File         : Comparison_Of_Copywriting_For_Petlibro_APP.py
@Interpreter Version: python 3.12
@Description:
'''

import xlrd
import re
import os
import xlwt
from w3lib.html import remove_tags
from loguru import logger

file_dir = os.path.dirname(os.path.realpath(__file__))
logger.info(file_dir)


def read_excel(file, keystr, valuestr):
    """
    :param file: 文案Excel文件
    :param keystr: Android && IOS
    :param valuestr: 文案里语言简称
    :return: {key:value}
    """
    read_result = {}
    excelfile = xlrd.open_workbook(file, 'utf-8')  # 打开excel文件
    table_nums = excelfile.nsheets  # 获取表的数量
    for i in range(table_nums):  # 遍历表
        talbe = excelfile.sheet_by_index(i)
        col_count = talbe.ncols  # 表列总数
        a, b = [], []  # key,value
        for num in range(col_count):  # 遍历列
            col_topname = talbe.cell_value(0, num)  # 获取列头信息
            if keystr in col_topname:
                a += talbe.col_values(num)
            if valuestr in col_topname:
                b += talbe.col_values(num)

            for key, value in zip(a, b):
                read_result[key] = value  # 写入dict
    return read_result


def ios_str(file):
    """
    :param file: iOS 字符串文件
    :return: {key:value}
    """
    ios_result = {}
    f = open(file, 'r', encoding='utf-8')
    for line in f.readlines():
        key_value = re.findall(r'"(.*)" = "(.*)";', line)
        if key_value == []:
            pass
        else:
            ios_result[key_value[0][0]] = remove_tags(key_value[0][1])
    f.close()

    return ios_result


def read_xml(path):
    """
    :param path: 代码路径
    :return: {name:value}
    """
    xml_result = {}
    for i in os.listdir(path):  # 遍历代码路径
        if i[0] == '.':  # 过滤.开头文件
            pass
        else:
            f = open(path + '/' + i, 'r', encoding='utf-8')
            for line in f.readlines():  # 遍历代码文件
                # key_value = re.findall(r'<string name="(.*)">(.*)</string>', line)  # 查找对应字符串
                key_value = re.findall(r'<string name="(.*)">(.*)', line)  # 查找对应字符串
                if key_value == []:
                    pass
                else:
                    xml_result[key_value[0][0]] = remove_tags(key_value[0][1])  # 去除标签写入dict
            f.close()

    return xml_result


# 通过value查找key
def get_keys(d, value):
    for k, v in d.items():
        if v == value:
            return k


# 提取字母
def re_abc(str_value):
    abc = ''.join(re.findall(r'[A-Za-z]', str_value))
    return abc


def str_compar(execl_result, string_result, save_name):
    """
    :param execl_result: 文案dict
    :param string_result: 代码dict
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    memSheet = workbook.add_sheet('str_comparison')
    i = 1
    memSheet.write(0, 0, "count")
    memSheet.write(0, 1, "key_name")
    memSheet.write(0, 2, "文案文本")
    memSheet.write(0, 3, "代码文本")
    memSheet.write(0, 4, "对比结果")

    for key in execl_result:
        memSheet.write(i, 0, i)
        memSheet.write(i, 1, key)
        excel_str = str(execl_result[key]).strip()
        memSheet.write(i, 2, excel_str)
        if key in string_result.keys():
            string_str = str(string_result[key]).strip()
            memSheet.write(i, 3, string_str)
            if string_str == excel_str:
                memSheet.write(i, 4, "对比成功")
            elif string_str.lower() == excel_str.lower():
                memSheet.write(i, 4, "大小写对比错误！")
            elif string_str.replace('\\', '') == excel_str.replace('\\', ''):
                memSheet.write(i, 4, "去除转义字符后对比成功")
            elif string_str.replace('\\', '').lower() == excel_str.replace('\\', '').lower():
                memSheet.write(i, 4, "去除转义字符后, 大小写对比错误！")
            elif string_str.replace('\\n', '') == excel_str.replace('\\n', ''):
                memSheet.write(i, 4, "去除换行符后对比成功")
            elif string_str.replace('\\n', '').lower() == excel_str.replace('\\n', '').lower():
                memSheet.write(i, 4, "去除换行符后，大小写对比错误！")
            elif string_str.replace('\\n', '').replace('\\', '') == excel_str.replace('\\n', '').replace('\\', ''):
                memSheet.write(i, 4, "去除换行符和转义字符后对比成功")
            elif string_str.replace('\\n', '').replace('\\', '').lower() == excel_str.replace('\\n', '').replace('\\',
                                                                                                                 '').lower():
                memSheet.write(i, 4, "去除换行符和转义字符后，大小写对比错误")
            elif string_str.replace(' ', '') == excel_str.replace(' ', ''):
                memSheet.write(i, 4, "对比成功")
            elif string_str.replace(' ', '').lower() == excel_str.replace(' ', '').lower():
                memSheet.write(i, 4, "大小写对比错误")
            elif string_str.replace('.', '') == excel_str.replace('.', ''):
                memSheet.write(i, 4, "缺少.,对比错误")
            elif re_abc(string_str) == re_abc(excel_str):
                memSheet.write(i, 4, "只提取字母对比成功")
            elif string_str == '':
                memSheet.write(i, 4, "代码里搜寻失败！")
            else:
                memSheet.write(i, 4, "对比错误！")
        else:
            if excel_str in string_result.values():
                memSheet.write(i, 4, "key_name不匹配，但文案文本存在于name = " + get_keys(string_result, excel_str))
            elif key == 'Android':
                memSheet.write(i, 4, 'pass')
            else:
                memSheet.write(i, 4, "key_name不匹配且文案文本不存在")
        i += 1
    workbook.save('./' + save_name + '.xls')  # 保存路径


def language_main():
    language = input('请输入你的对比语言（例如DE）：----').strip()
    excel = input('请输入你的文件名称：----').strip()
    file_dir = input('请输入需要处理的目录路径，例如：D:\desktop：----').strip()
    file = file_dir + '\\' + excel + '.xlsx'  # 文案excel
    DE_path = file_dir + r'\Android\values-' + language  # DE代码对比路径
    result = read_excel(file, 'Android', language)  # 安卓文案DE
    xml = read_xml(DE_path)  # 安卓代码DE
    str_compar(result, xml, language + '_Android' + '_str_comparison_result')
    logger.info('文案比对成功！！！')


if __name__ == '__main__':
    language_main()
