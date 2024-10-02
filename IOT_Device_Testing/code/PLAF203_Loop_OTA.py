# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:54
@File         : PLAF203_Loop_OTA.py
@Interpreter Version: python 3.12
@Description: 当前运营平台的token失效时间为7天、APP用户的token失效时间为14天;
1.注意：两个目标固件版本在运营平台需提前上传固件包;
2.把设备绑定成功后先升级到循环OTA的其中一个目标版本，例如在1.0.69--1.0.71之间OTA压测，那就把设备先升级到1.0.69;
3.设备成功升级到1.0.69版本后，通过调https://test-admin.dl-aiot.com/api/deviceOta/save接口往运营平台插入OTA任务;
4.然后调https://test-admin.dl-aiot.com/api/deviceOta/start接口开始OTA任务;
5.调https://test-api.dl-aiot.com/device/ota/doUpgrade接口让设备执行OTA任务;
6.调https://test-admin.dl-aiot.com/api/deviceOta/end接口结束OTA任务;
7.调https://test-admin.dl-aiot.com/api/device/attributes接口获取OTA结束前后设备的固件版本号;
'''

import json
import time
import requests
import pymysql
import redis
import hashlib
from loguru import logger
from config import config_handers

class AF203OTA(object):
    def __init__(self, USER, USERNEW, PASSWDNEW, MODE, TARGETHIGH, TARGETLOW, PRODUCT, DEVICESN, testTimes,
                 intervalTime):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

        self.USER = USER
        self.USERNEW = USERNEW
        self.PASSWDNEW = PASSWDNEW
        self.TARGETHIGH = TARGETHIGH
        self.TARGETLOW = TARGETLOW
        self.PRODUCT = PRODUCT
        self.DEVICESN = DEVICESN
        self.MODE = MODE
        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)

    '''调用登录test环境运营平台接口，抓取token'''

    def operationPlatformLoginToken(self):
        self.operationPlatformLoginTokenURL = 'https://test-admin.dl-aiot.com/api/login/email/login'
        self.headers3 = {
            'authority': 'test-admin.dl-aiot.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': f'{config_handers.header1}',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://test-admin.dl-aiot.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://test-admin.dl-aiot.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        hash_obj = hashlib.md5()
        hash_obj.update(f'{self.PASSWDNEW}'.encode('utf-8'))
        hash_result = hash_obj.hexdigest()
        parameter = {
            'email': f'{self.USERNEW}',
            'password': f'{hash_result}',
        }
        send_requests = requests.post(self.operationPlatformLoginTokenURL, headers=self.headers3,
                                      data=json.dumps(parameter))
        if '200' in str(send_requests):
            logger.info('运营平台上用户的token获取成功！')
            return send_requests.json()['data']
        else:
            logger.error('运营平台上用户的token获取失败！')

    '''连接测试环境的数据库'''

    def getConnectMysql(self):
        try:
            self.connect = pymysql.connect(
                host='10.30.0.6',
                port=3306,
                database='dl_cloud',
                user='root',
                password='pKUsAjaJzcMz',
                charset='utf8'  # 注意这里不能改为utf-8
            )  # 获取Mysql连接
            self.cursor = self.connect.cursor()
            logger.info('测试环境mysql数据库连接成功！')
        except pymysql.Error as error:
            logger.error('测试环境mysql数据库连接失败！')
            logger.error(f'报错信息：{error}')

    '''搜索app账号对应的用户ID'''

    def selectUserID(self):
        sql = f'SELECT id FROM cloud_member WHERE account = "{self.USER}"'
        try:
            self.cursor.execute(sql)
            userID = self.cursor.fetchone()[0]
            return userID
        except pymysql.Error as error:
            logger.error(f'查询{self.USER}用户ID失败！')
            logger.error(f'报错信息为：{error}')

    '''获取APP账号登录后在redis中的token'''

    def getConnectRedisToken(self):
        r = redis.Redis(host='10.30.0.6', password='Dl@admin123', port=6379, db=0)
        tk = r.get(f'tk:{self.selectUserID()}')
        result = tk.decode("utf-8").strip()
        logger.info(f'获取到{self.USER}在redis中的token为：{result}')
        return result

    '''查询设备高版本号对应的版本ID'''

    def selectFirmwareHighVersionID(self):
        sql = f'SELECT id FROM cloud_device_version WHERE version = "{self.TARGETHIGH}"'
        try:
            self.cursor.execute(sql)
            firmwareHighVersionID = self.cursor.fetchone()[0]
            return firmwareHighVersionID
        except pymysql.Error as error:
            logger.error(f'查询{self.TARGETHIGH}设备版本ID失败！')
            logger.error(f'报错信息为：{error}')

    '''查询设备低版本号对应的版本ID'''

    def selectFirmwareLowVersionID(self):
        sql = f'SELECT id FROM cloud_device_version WHERE version = "{self.TARGETLOW}"'
        try:
            self.cursor.execute(sql)
            firmwareLowVersionID = self.cursor.fetchone()[0]
            return firmwareLowVersionID
        except pymysql.Error as error:
            logger.error(f'查询{self.TARGETLOW}设备版本ID失败！')
            logger.error(f'报错信息为：{error}')

    '''查询产品对应的产品ID'''

    def selectProductID(self):
        sql = f'SELECT id FROM cloud_product WHERE identifier = "{self.PRODUCT}"'
        try:
            self.cursor.execute(sql)
            productID = self.cursor.fetchone()[0]
            return productID
        except pymysql.Error as error:
            logger.error(f'查询{self.PRODUCT}产品ID失败！')
            logger.error(f'报错信息为：{error}')

    '''在通过调接口的方式在运营平台中创建OTA任务：低-->高版本'''

    def createOTAJobLOW2HIGH(self):
        realTime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.deviceOtaSaveURL = 'https://test-admin.dl-aiot.com/api/deviceOta/save'
        parameter = {
            "jobName": f"{self.TARGETLOW}--{self.TARGETHIGH}_{realTime}",
            "upgradeType": 1,  # 建议升级
            "upgradeDesc": f"{self.TARGETLOW}--{self.TARGETHIGH}_{realTime}",
            "effectiveType": 1,  # 手动生效
            "upgradeStrategy": 2,  # 2 灰度发布
            "grayProportion": 100,  # 灰度发布为100%范围
            "upgradeRemark": f"{self.TARGETLOW}--{self.TARGETHIGH}_{realTime}",
            "target": self.selectFirmwareHighVersionID(),  # 对应版本是PLAF203的高版本
            "targetProductId": self.selectProductID(),  # 对应的产品是PLAF203
            "targetVersionId": self.selectFirmwareHighVersionID(),  # 对应版本是PLAF203的高版本
        }
        send_requests = requests.post(self.deviceOtaSaveURL, headers=self.headers1, data=json.dumps(parameter))
        logger.info(f'{self.TARGETLOW} 固件版本的ID为：---- {self.selectFirmwareLowVersionID()}')
        logger.info(f'{self.TARGETHIGH} 固件版本的ID为：---- {self.selectFirmwareHighVersionID()}')
        logger.info(f'{self.PRODUCT} 产品的ID为：---- {self.selectProductID()}')
        if '200' in str(send_requests):
            logger.info(f'运营平台上OTA任务创建成功！---- {self.TARGETLOW}--{self.TARGETHIGH}_{realTime}')
            return send_requests.json()['data']
        else:
            logger.error(f'运营平台上OTA任务创建失败！---- {self.TARGETLOW}--{self.TARGETHIGH}_{realTime}')

    '''在通过调接口的方式在运营平台中创建OTA任务：高-->低版本'''

    def createOTAJobHIGH2LOW(self):
        realTime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.deviceOtaSaveURL = 'https://test-admin.dl-aiot.com/api/deviceOta/save'
        parameter = {
            "jobName": f"{self.TARGETHIGH}--{self.TARGETLOW}_{realTime}",
            "upgradeType": 1,  # 建议升级
            "upgradeDesc": f"{self.TARGETHIGH}--{self.TARGETLOW}_{realTime}",
            "effectiveType": 1,  # 手动生效
            "upgradeStrategy": 2,  # 2 灰度发布
            "grayProportion": 100,  # 灰度发布为100%范围
            "upgradeRemark": f"{self.TARGETHIGH}--{self.TARGETLOW}_{realTime}",
            "target": self.selectFirmwareLowVersionID(),  # 对应版本是PLAF203的低版本
            "targetProductId": self.selectProductID(),  # 对应的产品是PLAF203
            "targetVersionId": self.selectFirmwareLowVersionID(),  # 对应版本是PLAF203的低版本
        }
        send_requests = requests.post(self.deviceOtaSaveURL, headers=self.headers1, data=json.dumps(parameter))
        logger.info(f'{self.TARGETLOW} 固件版本的ID为：---- {self.selectFirmwareLowVersionID()}')
        logger.info(f'{self.TARGETHIGH} 固件版本的ID为：---- {self.selectFirmwareHighVersionID()}')
        logger.info(f'{self.PRODUCT} 产品的ID为：---- {self.selectProductID()}')
        if '200' in str(send_requests):
            logger.info(f'运营平台上OTA任务创建成功！---- {self.TARGETHIGH}--{self.TARGETLOW}_{realTime}')
            return send_requests.json()['data']
        else:
            logger.error(f'运营平台上OTA任务创建失败！---- {self.TARGETHIGH}--{self.TARGETLOW}_{realTime}')

    '''在运营平台上打开OTA任务'''

    def startOTAJob(self, ID):
        self.startOTAJobURL = 'https://test-admin.dl-aiot.com/api/deviceOta/start'
        parameter = {
            'id': f'{ID}'
        }
        send_requests = requests.post(self.startOTAJobURL, headers=self.headers1, data=json.dumps(parameter))
        time.sleep(2)
        if '200' in str(send_requests):
            logger.info(f'运营平台上OTA任务打开成功！---- OTA ID: {ID}')
        else:
            logger.error(f'运营平台上OTA任务打开失败！---- OTA ID: {ID}')

    '''搜索指定设备的JobItemId（OTA任务ID）'''

    def selectJobItemId(self, ID):
        self.selectJobItemIDURL = 'https://test-admin.dl-aiot.com/api/deviceOta/itemPage'
        parameter = {
            'DEVICESN': f'{self.DEVICESN}',
            'jobId': f'{ID}',
        }
        send_requests = requests.post(self.selectJobItemIDURL, headers=self.headers1, data=json.dumps(parameter))
        if '200' in str(send_requests):
            logger.info(f'获取设备的OTA任务单元成功！---- OTA任务ID：{send_requests.json()["data"]["result"][0]["id"]}')
            return send_requests.json()['data']['result'][0]['id']
        else:
            logger.error(f'获取设备的OTA任务ID失败！')

    '''设备执行OTA任务'''

    def exexuteOTAJob(self, ID):
        self.exexuteOTAJobURL = 'https://test-api.dl-aiot.com/device/ota/doUpgrade'
        parameter = {
            'deviceSn': f'{self.DEVICESN}',
            'jobItemId': f'{self.selectJobItemId(ID)}',
        }
        send_requests = requests.post(self.exexuteOTAJobURL, headers=self.headers2, data=json.dumps(parameter))
        time.sleep(2)
        if '200' in str(send_requests):
            logger.info(f'开始执行设备的OTA任务单元...')
        else:
            logger.error(f'开始执行设备的OTA任务单元失败！')

    '''关闭指定的OTA任务'''

    def endOTAJob(self, ID):
        realTime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.endOTAJobURL = 'https://test-admin.dl-aiot.com/api/deviceOta/end'
        parameter = {
            'id': f'{ID}',
            'endReason': f'OTA循环压测{realTime}',
        }
        send_requests = requests.post(self.endOTAJobURL, headers=self.headers1, data=json.dumps(parameter))
        time.sleep(2)
        if '200' in str(send_requests):
            logger.info(f'结束设备的OTA任务成功！---- {ID}')
        else:
            logger.error(f'结束执行设备的OTA任务单元失败！---- {ID}')

    '''获取设备的当前固件版本'''

    def getFirmwareVersion(self):
        self.getFirmwareVersionURL = 'https://test-admin.dl-aiot.com/api/device/attributes'
        parameter = {
            'id': f'{self.DEVICESN}',
        }
        send_requests = requests.post(self.getFirmwareVersionURL, headers=self.headers1, data=json.dumps(parameter))
        if '200' in str(send_requests):
            logger.info(f'获取设备的当前固件版本号成功！---- version: {send_requests.json()["data"]["softwareVersion"]}')
        else:
            logger.error(f'获取设备的OTA任务ID失败！')

    '''主程序'''

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203 OTA压测.log', rotation='100MB', encoding='utf-8', enqueue=True)
        self.getConnectMysql()
        self.TOKEN = self.operationPlatformLoginToken()  # 运营平台的账号token（7天失效）
        self.TOKEN1 = self.getConnectRedisToken()  # APP用户token(14天失效)

        self.headers1 = {
            'authority': 'test-admin.dl-aiot.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': f'{config_handers.header1}',
            'token': f'{self.TOKEN}',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://test-admin.dl-aiot.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://test-admin.dl-aiot.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'token={self.TOKEN}',
        }

        self.headers2 = {
            'language': 'EN',
            'source': 'IOS',
            'token': f'{self.TOKEN1}',
            'version': '0.2.14',
            'content-type': 'application/json;charset=UTF-8',
        }

        if self.MODE == '1':
            logger.info('已确认选择为：低->高 OTA模式')
            for count in range(1, self.testTimes + 1):
                if count % 2 != 0:
                    ID = self.createOTAJobLOW2HIGH()
                else:
                    ID = self.createOTAJobHIGH2LOW()
                try:
                    self.getFirmwareVersion()
                    self.startOTAJob(ID);
                    time.sleep(5)
                    self.selectJobItemId(ID);
                    time.sleep(3)
                    self.exexuteOTAJob(ID)
                    time.sleep(self.intervalTime)
                    self.endOTAJob(ID);
                    time.sleep(3)
                    self.getFirmwareVersion()
                except:
                    logger.error(f'执行第 {count} 次PLAF 203 OTA出现异常')
                remainingTimes = self.testTimes - count
                logger.info(f'剩余测试PLAF203 OTA的次数为：{remainingTimes}')
                if count == self.testTimes:
                    logger.info(f'PLAF203 OTA专项自动化测试结束！')

        else:
            logger.info('已确认选择为：高->低 OTA模式')
            for count in range(1, self.testTimes + 1):
                if count % 2 != 0:
                    ID = self.createOTAJobHIGH2LOW()
                else:
                    ID = self.createOTAJobLOW2HIGH()
                try:
                    self.getFirmwareVersion()
                    self.startOTAJob(ID);
                    time.sleep(5)
                    self.selectJobItemId(ID);
                    time.sleep(3)
                    self.exexuteOTAJob(ID)
                    time.sleep(self.intervalTime)
                    self.endOTAJob(ID);
                    time.sleep(3)
                    self.getFirmwareVersion()
                except:
                    logger.error(f'执行第 {count} 次PLAF 203OTA出现异常')
                remainingTimes = self.testTimes - count
                logger.info(f'剩余测试PLAF203 OTA的次数为：{remainingTimes}')
                if count == self.testTimes:
                    logger.info(f'PLAF203 OTA专项自动化测试结束！')


# USER = input('请输入登录APP上的账号：例如：h_15820352975@163.com ---- ').strip()
# USERNEW = input('请输入登录运营平台上的账号：例如：lucky.wang@designlibro.com ---- ').strip()
# PASSWDNEW = input('请输入登录运营平台上的密码：例如：Wr165896 ---- ').strip()
# MODE = input('请输入首次测试模式：1为：低->高   2为：高->低 ---- ').strip()
# TARGETHIGH = input('请输入两个目标版本中的高版本号：例如：1.0.71 ---- ').strip()
# TARGETLOW = input('请输入两个目标版本中的低版本号：例如：1.0.69 ---- ').strip()
# PRODUCT = input('请输入产品代号：例如：PLAF203 ---- ').strip()
# DEVICESN = input('请输入设备sn：例如：AF030120FBFC655R2 ---- ').strip()
# testTimes = input('请输入测试次数：---- ').strip()
# intervalTime = input('请输入每轮测试间隔时间：(单位：S，PLAF203不低于200S) ---- ').strip()

USER = 'h_15820352975@163.com'  # 登录APP上的账号
USERNEW = 'lucky.wang@designlibro.com'  # 登录运营平台上的账号
PASSWDNEW = 'Wr165896'  # 登录运营平台上的密码
MODE = '2'  # 首次测试模式：1为：低->高   2为：高->低
TARGETHIGH = '1.0.72'  # 两个目标版本中的高版本号：例如：1.0.71
TARGETLOW = '1.0.71'  # 两个目标版本中的低版本号：例如：1.0.69
PRODUCT = 'PLAF203'  # 产品代号：例如：PLAF203
DEVICESN = 'AF030120FBFC655R2'  # 设备sn：例如：AF030120FBFC655R2
testTimes = '100000'  # 测试次数
intervalTime = '600'  # 每轮测试间隔时间：(单位：S，PLAF203不低于200S)

logger.info('开始执行PLAF203循环OTA专项自动化测试...')
aF203OTA = AF203OTA(USER, USERNEW, PASSWDNEW, MODE, TARGETHIGH, TARGETLOW, PRODUCT, DEVICESN, testTimes, intervalTime)
aF203OTA.main()
