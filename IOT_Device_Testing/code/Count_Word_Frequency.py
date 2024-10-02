# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:50
@File         : Count_Word_Frequency.py
@Interpreter Version: python 3.12
@Description:
'''

import pandas as pd
import jieba
from collections import Counter


class GetKeyWordAndShortSentence(object):
    def __init__(self):
        self.df = pd.read_excel(r'C:\Users\leon1\Desktop\问答题2统计结果.xlsx')

    def getKeyWord(self):
        text = ''.join(self.df.astype(str).sum())  # 将所有单元格中的字符串拼接成一个字符串
        words = jieba.cut(text)  # 使用 jieba 分词

        '''去除停用词'''
        stop_words = set(['我', '你', '他', '她'])
        words = [word for word in words if word not in stop_words]

        word_counts = Counter(words)  # 统计中文词语出现的次数

        '''输出出现次数最多的前 100 个中文词语'''
        wordList = []
        for word, count in word_counts.most_common(100):
            if '\u4e00' <= word <= '\u9fff' and len(word) >= 2:
                print(f"{word}----{count}")
                wordList.append(word)
        return wordList

    def getShortSentence(self):
        delimiters = ['，', '1', '：', '.', '2', '3', '4', '\n', '。', ':', '、', ' ', ',', '；', '-', '（', '）', '①', '②',
                      '③']
        '''定义分割函数'''

        def split_text(text):
            for delimiter in delimiters:
                text = text.replace(delimiter, '|')
            return text.split('|')

        '''将每个单元格的内容按照分隔符集进行分割'''
        df = self.df.applymap(lambda x: split_text(x) if isinstance(x, str) else x)
        data = df.values.tolist()

        '''拆分所有嵌套列表'''

        def flatten(data):
            result = []
            for item in data:
                if isinstance(item, list):
                    result.extend(flatten(item))
                else:
                    result.append(item)
            return result

        new_lst = [x for x in flatten(data) if not (isinstance(x, int) or x.strip() == '')]  # 去除列表中的int类型元素和空类型元素
        return new_lst

    def main(self):
        for i in self.getKeyWord():
            print(f'关键词------------ {i}')
            for j in self.getShortSentence():
                if i in j:
                    print(j)
            print('')


if __name__ == '__main__':
    getKeyWordAndShortSentence = GetKeyWordAndShortSentence()
    getKeyWordAndShortSentence.main()
