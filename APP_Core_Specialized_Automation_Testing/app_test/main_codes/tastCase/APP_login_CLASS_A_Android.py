# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/2 20:52
# @File         : APP_login_CLASS_A_Android.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


from ..generalModule.general_login import Login


class APPLogin(object):
    def __init__(self):
        '''实例化Login对象login'''
        self.login = Login()

    def main(self):
        if not self.login.login():
            return False
        return True
