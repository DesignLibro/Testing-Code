# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:32
@File         : Comparison_Of_Copywriting_For_Petlibro_APP_New.py
@Interpreter Version: python 3.12
@Description:
'''

import json
import datetime
import xlwt
from loguru import logger


class APPWordContrast(object):
    def __init__(self, des_folder, standard_word_path, current_word_path):
        self.des_folder = des_folder
        self.standard_word_path = standard_word_path
        self.current_word_path = current_word_path

        # 实际文案
        with open(self.current_word_path, 'r',
                  encoding='utf-8') as current_word_file:  # 设置为gbk，解决报错：UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa3 in position 1813: invalid start byte
            self.data = json.load(current_word_file)
        current_word_file.close()

        # 标准文案
        with open(self.standard_word_path, 'r',
                  encoding='utf-8') as standard_word_file:  # 设置为gbk，解决报错：UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa3 in position 1813: invalid start byte
            self.data1 = json.load(standard_word_file)
        standard_word_file.close()

    def get_simple_keys(self):  # 获取文案的KEY
        my_list = []
        for key, value in self.data.items():
            my_list.append(key)
            if type(value) is dict:
                for key1, value1 in self.data[key].items():
                    if type(value1) is dict:
                        for key2, value2 in value1.items():
                            my_list.append(key + '.' + key1 + '.' + key2)
                    else:
                        my_list.append(key + '.' + key1)
        else:
            for i in my_list:
                if '.' not in i:
                    my_list.remove(i)
            return my_list

    def get_simple_values(self):  # 获取实际文案
        my_list = []
        for key, value in self.data.items():
            if type(value) is dict:
                for key1, value1 in self.data[key].items():
                    if type(value1) is dict:
                        for key2, value2 in value1.items():
                            my_list.append(value2)
                    else:
                        my_list.append(value1)
        return my_list

    def get_simple_values_new(self):  # 获取标准文案
        my_list = []
        for key, value in self.data1.items():
            if type(value) is dict:
                for key1, value1 in self.data1[key].items():
                    if type(value1) is dict:
                        for key2, value2 in value1.items():
                            my_list.append(value2)
                    else:
                        my_list.append(value1)
        return my_list

    def bulidExcel(self):
        # 设置表头居中对齐的样式
        headStyle = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        headStyle.alignment = al

        # 设置表头边框样式
        borders = xlwt.Borders()
        borders.left, borders.right, borders.top, borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
        borders.left_colour, borders.right_colour, borders.top_colour, borders.bottom_colour = 0x40, 0x40, 0x40, 0x40
        headStyle.borders = borders

        # 设置表头字体
        font = xlwt.Font()
        font.name = 'Arial'  # 字体名称
        font.bold = False  # 不加粗
        font.underline = False  # 不加下划线
        font.italic = False  # 不加斜体
        font.colour_index = 1  # 纯白色字体颜色
        headStyle.font = font

        # 设置表头背景色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_blue']  # Anker标准蓝
        headStyle.pattern = pattern

        # 设置居中对齐的样式
        style = xlwt.XFStyle()
        al = xlwt.Alignment()
        # al.horz = 0x02  # 设置水平居中
        al.horz = 0x01  # 设置左对齐
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al

        # 设置边框样式
        borders = xlwt.Borders()
        borders.left, borders.right, borders.top, borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
        borders.left_colour, borders.right_colour, borders.top_colour, borders.bottom_colour = 0x40, 0x40, 0x40, 0x40
        style.borders = borders

        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('文案比对result')

        sheet.col(0).width = 8000
        sheet.col(1).width = 8000
        sheet.col(2).width = 8000
        sheet.col(3).width = 8000

        sheet.write(0, 0, 'KEY', headStyle)
        sheet.write(0, 1, '标准文案', headStyle)
        sheet.write(0, 2, '实际文案', headStyle)
        sheet.write(0, 3, '比对结果', headStyle)

        x_count, y_count, z_count, count = 1, 1, 1, 2
        for x in self.get_simple_keys():
            sheet.write(x_count, 0, x, style)
            x_count += 1

        for y in self.get_simple_values():
            sheet.write(y_count, 2, y, style)
            y_count += 1

        for z in self.get_simple_values_new():
            sheet.write(z_count, 1, z, style)
            z_count += 1

        for i in range(len(self.get_simple_keys())):
            sheet.write(count - 1, 3, xlwt.Formula(f'EXACT(b{count}, c{count})'))
            count += 1

        now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # workbook.save(self.des_folder + '\\' + '文案比对结果' + '_' + now_time + '.xlsx')
        workbook.save(self.des_folder + '\\' + 'H5 ZH' + '_新' + '.xlsx')
        logger.info('脚本执行完成！')

    def run(self):
        self.bulidExcel()


if __name__ == '__main__':
    standard_word_path = input('输入标准文案的文件绝对路径----').strip()
    current_word_path = input('输入实际文案的文件绝对路径----').strip()
    des_folder = input('输入处理后的文件保存目录----').strip()
    appWordContrast = APPWordContrast(des_folder, standard_word_path, current_word_path)
    appWordContrast.run()
