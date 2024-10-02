# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/3/13 14:27
# @File         : general_build_ota_task.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import hashlib
import json
import requests
import pymysql
import redis
import time
import os
from loguru import logger
from ..generalModule.general_take_down_pop import TakeDownPOP
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_permission_click import PermissionClick
from ..generalModule.general_phone_record import PhoneRecord
from feishu_send_message import send_feishu_text_Message


class BuildOtaTask(object):
    def __init__(self):
        self.ota_task_ids = []

        '''实例化ReloadYaml对象reload_yaml'''
        reload_yaml = ReloadYaml()
        reload_yaml.main()
        self.width = reload_yaml.width  # 测试手机的长像素
        self.height = reload_yaml.height  # 测试手机的宽像素
        self.mainTimeoutDuration = reload_yaml.mainTimeoutDuration  # APP登录成功后在首页的判断超时时间

        self.test_environment_operation_platform_account = reload_yaml.test_environment_operation_platform_account  # test环境运营平台账号
        self.test_environment_operation_platform_passwd = reload_yaml.test_environment_operation_platform_passwd  # test环境运营平台密码
        self.test_operationPlatformLoginTokenURL = reload_yaml.test_operationPlatformLoginTokenURL  # test环境运营平台URL
        self.test_operationPlatformLoginTokenAuthority = reload_yaml.test_operationPlatformLoginTokenAuthority  # test环境运营平台authority
        self.test_operationPlatformLoginTokenOrigin = reload_yaml.test_operationPlatformLoginTokenOrigin  # test环境运营平台origin
        self.test_operationPlatformLoginTokenReferer = reload_yaml.test_operationPlatformLoginTokenReferer  # test环境运营平台referer
        self.browser_header = reload_yaml.browser_header  # 谷歌浏览器头部
        self.test_getOTATaskListURL = reload_yaml.test_getOTATaskListURL  # 获取ota任务列表URL
        self.test_endOTATaskListURL = reload_yaml.test_endOTATaskListURL  # 结束ota任务URL
        self.test_startOTAJobURL = reload_yaml.test_startOTAJobURL  # 开启OTA任务URL
        self.test_getDeviceInfoURL = reload_yaml.test_getDeviceInfoURL  # 获取当前设备信息URL
        self.deviceOtaSaveURL = reload_yaml.test_deviceOtaSaveURL  # 创建OTA任务URL
        self.test_selectJobItemIDURL = reload_yaml.test_selectJobItemIDURL  # 搜索指定设备的JobItemId URL
        self.test_exexuteOTAJobURL = reload_yaml.test_exexuteOTAJobURL  # 设备执行OTA任务

        self.AF103_HIGH_VERSION = reload_yaml.AF103_HIGH_VERSION  # 当前设备对应的最高OTA目标版本
        self.AF103_LOW_VERSION = reload_yaml.AF103_LOW_VERSION  # 当前设备对应的最低OTA目标版本

        self.bluetoothBindingDeviceTimeout = reload_yaml.bluetoothBindingDeviceTimeout
        self.AF103_MAC = reload_yaml.AF103_MAC

        '''测试环境数据库信息'''
        self.test_host = reload_yaml.test_host
        self.test_port = reload_yaml.test_port
        self.test_database = reload_yaml.test_database
        self.test_user = reload_yaml.test_user
        self.test_password = reload_yaml.test_password
        self.test_charset = reload_yaml.test_charset

        self.user1 = reload_yaml.user1
        self.server_password = reload_yaml.server_password
        self.test_redis_port = reload_yaml.test_redis_port
        self.test_redis_password = reload_yaml.test_redis_password

        '''连接测试环境的数据库'''
        try:
            self.connect = pymysql.connect(
                host=self.test_host,
                port=self.test_port,
                database=self.test_database,
                user=self.test_user,
                password=self.test_password,
                charset=self.test_charset  # 注意这里不能改为utf-8
            )  # 获取Mysql连接
            self.cursor = self.connect.cursor()
            logger.info('测试环境mysql数据库连接成功！')
        except pymysql.Error as error:
            logger.error('测试环境mysql数据库连接失败！')
            logger.error(f'报错信息：{error}')

    def run(self):
        '''实例化PermissionClick对象permissionClick'''
        self.permissionClick = PermissionClick()
        self.driver = self.permissionClick.runGetDriver()

        '''实例化TakeDownPOP对象takeDownPOP'''
        self.takeDownPOP = TakeDownPOP()
        self.takeDownPOP.takeDownoperationalPromotionPopup()

        '''获取当前脚本文件'''
        self.file_path = os.path.abspath(__file__)  # 获取当前脚本的文件名（包括路径）
        self.file_name = os.path.basename(self.file_path)  # 获取文件名和扩展名
        self.file_name_without_extension = os.path.splitext(self.file_name)[0]

        '''实例化PhoneRecord对象phoneRecord'''
        self.recordName = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        self.output_file_name = f'record_{self.file_name_without_extension}_{self.recordName}.mp4'
        self.phoneRecord = PhoneRecord(self.output_file_name)
        # self.phoneRecord.start_screen_recording(self.output_file_name)

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
        send_requests = requests.post(self.test_operationPlatformLoginTokenURL, headers=self.headers1,
                                      data=json.dumps(parameter1))
        if send_requests.json()['code'] == 0:
            # logger.info('运营平台上用户的token获取成功！')
            return send_requests.json()['data']
        else:
            logger.error('运营平台上用户的token获取失败！')

    '''查询产品对应的产品ID'''
    def selectProductID(self, PRODUCT):
        sql = f'SELECT id FROM cloud_product WHERE identifier = "{PRODUCT}"'
        try:
            self.cursor.execute(sql)
            self.productID = self.cursor.fetchone()[0]
            return self.productID
        except pymysql.Error as error:
            logger.error(f'查询{PRODUCT}产品ID失败！')
            logger.error(f'报错信息为：{error}')

    '''获取指定设备类型下“进行中”的OTA任务列表'''
    def getRunningOTATaskList(self, PRODUCT):
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
            'jobState': 2,  # 进行中的状态
            'pageNum': 1,
            'pageSize': 200,
        }
        send_requests = requests.post(self.test_getOTATaskListURL, headers=self.headers2, data=json.dumps(parameter2))
        if send_requests.json()['code'] == 0:
            data = send_requests.json()
            for item in data['data']['result']:
                if item['targetProductId'] == self.selectProductID(PRODUCT) and item['state'] == 2:
                    self.ota_task_ids.append(item['id'])
            return self.ota_task_ids
        else:
            logger.error('运营平台上OTA任务列表获取失败')

    '''将指定设备类型下“进行中”的ota任务都结束'''
    def endOtaTask(self, PRODUCT):
        try:
            for id in self.getRunningOTATaskList(PRODUCT):
                send_requests = requests.post(self.test_endOTATaskListURL, headers=self.headers2, data=json.dumps({'id': f'{id}', 'endReason': 'lucky_test'}))
                if send_requests.json()['code'] == 0:
                    logger.info(f'结束ota任务id：{id}')
                    time.sleep(2)
            else:
                logger.info(f'所有{PRODUCT}的进行中OTA任务都已结束')
        except Exception as error:
            logger.info(f'所有{PRODUCT}的进行中OTA任务都已结束')
            logger.error(error)

    '''搜索app账号对应的用户ID'''
    def selectUserID(self):
        sql = f'SELECT id FROM cloud_member WHERE account = "{self.user1}"'
        try:
            self.cursor.execute(sql)
            self.userID = self.cursor.fetchone()[0]
            return self.userID
        except pymysql.Error as error:
            logger.error(f'查询{self.user1}用户ID失败！')
            logger.error(f'报错信息为：{error}')

    '''获取APP账号登录后在redis中的token'''
    def getConnectRedisToken(self):
        r = redis.Redis(host=self.test_host, password=self.test_redis_password, port=6379, db=0)
        tk = r.get(f'tk:{self.selectUserID()}')
        result = tk.decode("utf-8").strip()
        logger.info(f'获取到{self.user1}账号在redis中的token为：{result}')
        return result

    '''根据设备MAC地址查询SN'''
    def getCurrentDeviceSN(self, MAC):
        logger.info(MAC)
        sql = f'SELECT device_sn FROM cloud_device WHERE mac = "{MAC}"'
        try:
            self.cursor.execute(sql)
            self.deviceSN = self.cursor.fetchone()[0]
            return self.deviceSN
        except pymysql.Error as error:
            logger.error(f'查询{MAC}设备的SN失败！')
            logger.error(f'报错信息为：{error}')

    '''获取当前设备的固件版本号'''
    def getCurretntDeviceVersion(self, MAC):
        parameter4 = {
            'id': self.getCurrentDeviceSN(MAC=MAC),
        }
        send_requests = requests.post(self.test_getDeviceInfoURL, headers=self.headers2, data=json.dumps(parameter4))
        if send_requests.json()['code'] == 0:
            data = send_requests.json()
            self.VERSION = data['data']['softwareVersion']
            return data['data']['softwareVersion']
        else:
            logger.error(f'获取{MAC}设备的SN失败')

    '''查询设备版本号对应的版本ID'''
    def selectFirmwareVersionID(self, PRODUCT, VERSION):
        sql = f'SELECT id FROM cloud_device_version WHERE version = "{VERSION}" AND product_id = {self.selectProductID(PRODUCT=PRODUCT)}'
        try:
            self.cursor.execute(sql)
            firmwareHighVersionID = self.cursor.fetchone()[0]
            return firmwareHighVersionID
        except pymysql.Error as error:
            logger.error(f'查询{VERSION}设备版本ID失败！')
            logger.error(f'报错信息为：{error}')

    '''在通过调接口的方式在运营平台中创建OTA任务'''
    def createOTAJob(self, PRODUCT, MAC, VERSION):
        realTime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        _parameter5 = {
                "deviceSns": self.getCurrentDeviceSN(MAC=MAC),
                "jobName": f"{self.VERSION}--{VERSION}_{realTime}",
                "upgradeType": 1,  # 建议升级
                "upgradeDesc": f"{self.VERSION}--{VERSION}_{realTime}",
                "effectiveType": 1,  # 手动生效
                "upgradeStrategy": 1,  # 1 指定SN升级
                "grayProportion": 1,  # 指定SN升级(灰度 1)
                "upgradeRemark": f"{self.VERSION}--{VERSION}_{realTime}",
                "target": self.selectFirmwareVersionID(PRODUCT=PRODUCT, VERSION=VERSION),
                "targetProductId": self.selectProductID(PRODUCT=PRODUCT),
                "targetVersionId": self.selectFirmwareVersionID(PRODUCT=PRODUCT, VERSION=VERSION),
        }
        send_requests = requests.post(self.deviceOtaSaveURL, headers=self.headers2, data=json.dumps(_parameter5))
        # logger.info(f'{self.VERSION} 固件版本的ID为：---- {self.selectFirmwareVersionID(PRODUCT, VERSION)}')
        # logger.info(f'{self.selectFirmwareVersionID(PRODUCT, VERSION)} 固件版本的ID为：---- {self.selectFirmwareVersionID(PRODUCT, VERSION)}')
        # logger.info(f'{PRODUCT} 产品的ID为：---- {self.selectProductID(PRODUCT)}')
        if send_requests.json()['code'] == 0:
            logger.info(f'运营平台上OTA任务创建成功！---- {self.VERSION}--{VERSION}_{realTime}')
            self.ID = send_requests.json()['data']
            return self.ID
        else:
            logger.error(send_requests.json())
            logger.error(f'运营平台上OTA任务创建失败！---- {self.VERSION}--{VERSION}_{realTime}')

    '''在运营平台上打开OTA任务'''
    def startOTAJob(self, PRODUCT, MAC, VERSION):
        try:
            self.getCurrentDeviceSN(MAC=MAC)
            _parameter6 = {
                'id': f'{self.createOTAJob(PRODUCT=PRODUCT, MAC=MAC, VERSION=VERSION)}'
            }
            send_requests = requests.post(self.test_startOTAJobURL, headers=self.headers2, data=json.dumps(_parameter6))
            time.sleep(2)
            if send_requests.json()['code'] == 0:
                logger.info(f'运营平台上OTA任务打开成功！')
                return True
            else:
                logger.error(f'运营平台上OTA任务打开失败！')
                return False
        except:
            return False

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    '''控制手机屏幕上滑'''
    def swipeUp(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.1498 * self.height)
        y2 = int(0.9855 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    '''控制手机屏幕下滑'''
    def swipeDown(self):
        x1 = int(0.7130 * self.width)
        y1 = int(0.9855 * self.height)
        y2 = int(0.1498 * self.height)
        self.swipe(x1, y1, x1, y2, 20000)

    '''APP首页判断'''
    def mainJudge(self):
        self.run()
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Device' in self.driver.page_source and 'Me' in self.driver.page_source:
                    logger.info('step1：当前APP处于设备首页')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step1：当前APP未处于设备首页，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step1：当前APP未处于设备首页，后续用例无法执行')
            return False

    '''APP首页点击设备卡片'''
    def clickDeviceCard(self):
        self.driver.tap([(0.5018 * self.width, 0.4457 * self.height)], duration=1)
        logger.info('点击首页设备卡片')
        time.sleep(2)
        return True

    '''设备面板判断'''
    def deviceFaceJudge(self):  # 适用103、
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Meal Call' in self.driver.page_source:
                    logger.info('step2：跳转到设备面板')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step2：当前未处于设备面板，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step2：当前未处于设备面板，后续用例无法执行')

    '''点击单/双食盆蒙版的DONE按钮'''
    def deviceFaceAboutSignalOrDual(self):
        time.sleep(5)
        self.driver.tap([(0.0777 * self.width, 0.5037 * self.height)], duration=1)
        time.sleep(2)
        logger.info('点击单/双食盆蒙版的DONE按钮')
        return True

    '''OTA弹窗判断'''
    def otaFaceJudge(self):  # 适用103、
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'Newest Version' in self.driver.page_source:
                    logger.info('step3：出现OTA弹框')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step3：当前未出现OTA弹窗，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step3：当前未出现OTA弹窗，后续用例无法执行')

    '''点击确认升级按钮'''
    def clickOTAButton(self):
        self.driver.tap([(0.5314 * self.width, 0.6730 * self.height)], duration=1)
        logger.info('step4：点击确认升级按钮')
        time.sleep(4)
        return True

    '''OTA界面判断'''
    def otaWebJudge(self):
        for i in range(self.mainTimeoutDuration):
            if self.driver.page_source:
                if 'FIRMWARE UPDATE' in self.driver.page_source:
                    logger.info('step5：当前处于OTA进度界面')
                    time.sleep(2)
                    return True
                else:
                    time.sleep(1)
                    self.swipeUp()
        else:
            logger.error('step5：当前未出于ota进度界面，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('step5：当前未出于ota进度界面，后续用例无法执行')

    '''监控OTA结果'''
    def otaResultJudge(self):
        for i in range(self.bluetoothBindingDeviceTimeout):
            if self.driver.page_source:
                if 'UPDATE SUCCESSFUL' in self.driver.page_source:
                    logger.info(f'Finally：设备{self.AF103_MAC}OTA 成功')
                    return True
                elif 'Fail' in self.driver.page_source or 'FAIL' in self.driver.page_source:
                    logger.error(f'Finally：设备{self.AF103_MAC}OTA 失败，后续用例无法执行')
                    time.sleep(2)
                else:
                    time.sleep(1)
            else:
                time.sleep(1)
        else:
            logger.error(f'Finally：设备{self.AF103_MAC}OTA 失败，后续用例无法执行')
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message(f'Finally：设备{self.AF103_MAC}OTA 失败，后续用例无法执行')
            return False
