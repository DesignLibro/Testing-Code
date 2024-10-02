# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/4 14:11
# @File         : general_take_down_pop.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import hashlib
import json
import requests
from loguru import logger
from ..generalModule.general_reload_yaml import ReloadYaml


class TakeDownPOP(object):
    def __init__(self):
        self.published_ids = []

        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.test_environment_operation_platform_account = reload_yaml.test_environment_operation_platform_account  # test环境运营平台账号
        self.test_environment_operation_platform_passwd = reload_yaml.test_environment_operation_platform_passwd  # test环境运营平台密码
        self.test_operationPlatformLoginTokenURL = reload_yaml.test_operationPlatformLoginTokenURL  # test环境运营平台URL
        self.test_operationPlatformLoginTokenAuthority = reload_yaml.test_operationPlatformLoginTokenAuthority  # test环境运营平台authority
        self.test_operationPlatformLoginTokenOrigin = reload_yaml.test_operationPlatformLoginTokenOrigin  # test环境运营平台origin
        self.test_operationPlatformLoginTokenReferer = reload_yaml.test_operationPlatformLoginTokenReferer  # test环境运营平台referer
        self.browser_header = reload_yaml.browser_header  # 谷歌浏览器头部
        self.test_getoperationPlatformLMarketingPromotionURL = reload_yaml.test_getoperationPlatformLMarketingPromotionURL  # test环境运营平台获取运营推广URL
        self.test_takeDownPopURL = reload_yaml.test_takeDownPopURL  # test环境运营平台下架pop弹窗URL

    '''调用登录test环境运营平台接口，抓取token'''
    def operationPlatformLoginToken(self):
        self.headers1 = {
            'authority': self.test_operationPlatformLoginTokenAuthority,
            'accept': 'application/json, text/plain, */*',
            'user-agent': self.browser_header,
            'content-type': 'application/json;charset=UTF-8',
            'origin': self.test_operationPlatformLoginTokenOrigin,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.test_operationPlatformLoginTokenReferer,
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        hash_obj = hashlib.md5()
        hash_obj.update(f'{self.test_environment_operation_platform_passwd}'.encode('utf-8'))
        hash_result = hash_obj.hexdigest()
        parameter1 = {
            'email': f'{self.test_environment_operation_platform_account}',
            'password': f'{hash_result}',
        }
        send_requests = requests.post(self.test_operationPlatformLoginTokenURL, headers=self.headers1, data=json.dumps(parameter1))
        if send_requests.json()['code'] == 0:
            # logger.info('运营平台上用户的token获取成功！')
            return send_requests.json()['data']
        else:
            logger.error('运营平台上用户的token获取失败！')

    def getoperationPlatformLMarketingPromotion(self):
        self.headers2 = {
            'authority': self.test_operationPlatformLoginTokenAuthority,
            'accept': 'application/json, text/plain, */*',
            'user-agent': self.browser_header,
            'content-type': 'application/json;charset=UTF-8',
            'Cookie': f'token={self.operationPlatformLoginToken()}',
            'origin': self.test_operationPlatformLoginTokenOrigin,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.test_operationPlatformLoginTokenReferer,
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        parameter2 = {
            'pageNum': 1,
            'pageSize': 200,
        }
        send_requests = requests.post(self.test_getoperationPlatformLMarketingPromotionURL, headers=self.headers2, data=json.dumps(parameter2))
        if send_requests.json()['code'] == 0:
            # logger.info(f'获取test环境运营平台中运营推广列表成功，其中上架的pop_up弹窗id如下：')
            data = send_requests.json()

            for item in data['data']['result']:
                if item['type'] == 'POP_UP' and item['published'] == True:
                    self.published_ids.append(item['id'])
            # logger.info(self.published_ids)
            return self.published_ids
        else:
            logger.error('运营平台上运营推广列表获取失败')

    def takeDownoperationalPromotionPopup(self):
        self.headers3 = {
            'authority': self.test_operationPlatformLoginTokenAuthority,
            'accept': 'application/json, text/plain, */*',
            'user-agent': self.browser_header,
            'content-type': 'application/json;charset=UTF-8',
            'Cookie': f'token={self.operationPlatformLoginToken()}',
            'origin': self.test_operationPlatformLoginTokenOrigin,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.test_operationPlatformLoginTokenReferer,
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        for id in self.getoperationPlatformLMarketingPromotion():
            send_requests = requests.post(self.test_takeDownPopURL, headers=self.headers3, data=json.dumps({'id': id}))
            if send_requests.json()['code'] == 0:
                logger.info(f'成功下架弹窗id：{id}')
        else:
            logger.info('所有pop_up弹窗下架成功')

# TakeDownPOP().takeDownoperationalPromotionPopup()  # 调试本脚本时解除注释