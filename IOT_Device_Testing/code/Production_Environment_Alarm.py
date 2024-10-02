# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:22
@File         : Production_Environment_Alarm.py
@Interpreter Version: python 3.12
@Description: 1.需要设备由亮灯为前提跑脚本
'''

import io
import time
import requests
import json
import hashlib
from PIL import Image
from loguru import logger
from appium import webdriver
from config import config_handers


class PRODServerMonitor(object):
    def __init__(self, testTimes, intervalTime):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            'platformName': 'Android',  # 固定值Android
            'platformVersion': '10',  # 系统版本号（在关于手机中查看）
            'deviceName': 'Galaxy S9',  # 手机型号
            'automationName': 'UiAutomator2',  # 固定值UiAutomator2
            'appPackage': 'com.designlibro.petlibro',
            # 在cmd窗口中敲adb shell dumpsys activity recents |find "intent={"命令获取包名和Activity名称
            'appActivity': '.MainActivity',
            'udid': '1c2bb463',  # 在cmd窗口中敲adb devices获取
            'autoLaunch': True,  # 在手机中启动appium服务，但不开启界面
            'noReset': True,  # 不要重置APP
            'fullReset': False,
            'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填写True
            'resetKeyboard': True,  # 执行完程序恢复原来的输入法
            'appium:newCommandTimeout': 360000,
            'appium:waitForSelectorTimeout': 1000,
            'appium:waitForIdleTimeout': 1000
        }
        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       self.desired_capabilities)  # 连接Appium Server，初始化自动化环境
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率
        # 在cmd窗口中获取手机屏幕分辨率的命令：adb shell dumpsys window displays，看内容：init=1440x2960 640dpi base=1080x2220 480dpi cur=1080x2220 app=1080x2076 rng=1080x1008-2076x2004

        '''飞书机器人配置'''
        self.url = 'https://open.feishu.cn/open-apis/bot/v2/hook/809136d8-6428-436e-a160-788eecf5ec72'
        self.headers = {
            'Content-Type': 'application/json',
        }

        '''运营平台参数配置'''
        self.USER = 'h_15820352975@163.com'  # 登录APP上的账号
        self.USERNEW = 'lucky.wang@designlibro.com'  # 登录运营平台上的账号
        self.PASSWDNEW = 'Wr165896'  # 登录运营平台上的密码
        self.DEVICESN = 'AF030120FBFC655R2'  # 设备sn：例如：AF030120FBFC655R2

        self.count = 1

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown(self):
        x1 = int(0.5129 * self.width)
        y1 = int(0.3030 * self.height)
        y2 = int(0.7564 * self.height)
        self.swipe(x1, y1, x1, y2, 2000)

    def feishuRobot(self, ProblemDescription):
        self.parameter = {
            'msg_type': 'text',
            'content': {
                'text': f'{ProblemDescription}'
            }
        }
        send_requests = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.parameter))
        time.sleep(3)
        if send_requests.json()['msg'] == 'success':
            logger.info('飞书机器人消息发送 SUCCESS')
        else:
            logger.info('飞书机器人消息发送 FAIL 并进行重发')
            requests.post(url=self.url, headers=self.headers, data=json.dumps(self.parameter))

    def appHandle1(self):
        for i in range(2):
            if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                logger.info('step1：当前APP处于设备首页')
                break
            else:
                logger.error('step1：当前APP未处于设备首页')
                self.swipeDown();
                time.sleep(2)

        self.driver.tap([(0.5129 * self.width, 0.3848 * self.height)], duration=1)
        logger.info('step 2: 点击"首页设备卡片"入口');
        time.sleep(3)

        if 'Air Pumping' in self.driver.page_source:
            logger.info('step 3：当前APP处于设备面板');
            time.sleep(3)

            # self.driver.find_element('xpath', '//android.widget.ImageView[@content-desc="Feed Now"]').click()
            # logger.info('step 4: 点击"Feed now"入口');time.sleep(3)
            #
            # self.driver.find_element('xpath', '//android.widget.Button[@content-desc="FEED NOW"]').click()
            # logger.info('step 5: 点击"Feed now"按钮')

            self.driver.find_element('xpath',
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
            logger.info('step 4：点击设备面板右上角的“设置”按钮');
            time.sleep(3)

            if 'DEVICE SETTINGS' in self.driver.page_source:
                logger.info('step 5：当前APP处于设置界面');
                time.sleep(3)

    def getImg(self):
        screenshot = self.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        rgb1 = image.getpixel((0.82 * self.width, 0.7729 * self.height))
        # self.driver.tap([(0.82 * self.width, 0.7729 * self.height)], duration=1)
        # print(rgb1)
        confidents1 = [
            rgb1[0] == 42,
            rgb1[1] == 42,
            rgb1[2] == 42,
        ]  # 黑灰色
        confidents2 = [
            rgb1[0] == 255,
            rgb1[1] == 255,
            rgb1[2] == 255,
        ]  # 白色
        if all(confidents1):
            logger.info('当前是开灯状态')
            return True
        elif all(confidents2):
            logger.info('当前是关灯状态')
            return False

    def appHandle2(self):
        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.ScrollView/android.widget.Switch[1]').click()
        logger.info('step 6：点击关灯按钮');
        time.sleep(8)

        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView').click()
        logger.info('step 7：点击左上角的返回按钮');
        time.sleep(8)

        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
        logger.info('step 8：点击设备面板右上角的“设置”按钮');
        time.sleep(8)

        time.sleep(self.intervalTime)
        self.getDevicesPost()

        # --------------------------------------------------------------------------------------------------------------------------------------------
        time.sleep(self.intervalTime)
        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.ScrollView/android.widget.Switch[1]').click()
        logger.info('step 9：点击开灯按钮');
        time.sleep(8)

        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView').click()
        logger.info('step 10：点击左上角的返回按钮');
        time.sleep(8)

        self.driver.find_element('xpath',
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
        logger.info('step 11：点击设备面板右上角的“设置”按钮');
        time.sleep(8)

        time.sleep(self.intervalTime)
        self.getDevicesPost()
        time.sleep(self.intervalTime)

    def operationPlatformLoginToken(self):
        self.getImg()
        self.operationPlatformLoginTokenURL = 'https://admin.us.petlibro.com/api/login/email/login'
        self.headers3 = {
            'authority': 'admin.us.petlibro.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': f'{config_handers.header1}',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://admin.us.petlibro.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://admin.us.petlibro.com',
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

    def getDevicesPost(self):
        '''
        self.TOKEN = self.operationPlatformLoginToken()  # 运营平台的账号token（7天失效）
        self.list1 = ['ATTR_SET_SERVICE', 'ATTR_PUSH_EVENT', 'APP_REFRESH_EVENT']
        self.list2 = []

        self.commandURL = 'https://admin.us.petlibro.com/api/data/command'
        self.headers1 = {
            'authority': 'admin.us.petlibro.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': f'{config_handers.header2}',
            'token': f'{self.TOKEN}',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://admin.us.petlibro.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-MODE': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://admin.us.petlibro.com',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'token={self.TOKEN}',
        }
        startTime = int(time.time() * 1000) - (2 * 60 * 1000)  # 3分钟的数据
        endTime = int(time.time() * 1000)

        self.parameter = {
            'deviceSn': 'AF020120FC342223M',
            'pageNum': 1,
            'pageSize': 200,
            'commands': self.list1,
            'startTime': f'{startTime}',
            'endTime': f'{endTime}',
        }
        send_requests = requests.post(url=self.commandURL, headers=self.headers1, data=json.dumps(self.parameter))

        print(send_requests.json())
        '''

        # try:
        # if len(send_requests.json()['data']['result'][0]['cmd']) != 0:
        #     for i in range(len(send_requests.json()['data']['result'][0]['cmd']) - 1):
        #         self.list2.append(send_requests.json()['data']['result'][i]['cmd'])
        # logger.info(self.list2)
        # if all(elem in self.list2 for elem in self.list1):
        # if 'APP_REFRESH_EVENT' in self.list2:
        logger.info(self.count)
        if self.getImg() == False and self.count % 2 != 0:
            self.info = '数据通信 SUCCESS'
            logger.info(f'{self.info}')
            # self.list2 = []
            self.count += 1
        elif self.getImg() == True and self.count % 2 == 0:
            self.info = '数据通信 SUCCESS'
            logger.info(f'{self.info}')
            # self.list2 = []
            self.count += 1
        else:
            self.info = '【重要告警】PLAF107喂食器设备，在上一次点击开/关灯按钮，重新进入设置界面，没有在1分钟内未及时更新开/关灯状态\n----设备SN：AF020120FC342223M'
            logger.error(f'{self.info}')
            # self.list2 = []
            self.feishuRobot(self.info)

        # except Exception as error:
        #     self.info = '【重要告警】PLAF107喂食器设备，在上一次点击开/关灯按钮，重新进入设置界面，没有在1分钟内未及时更新开/关灯状态\n----设备SN：AF020120FC342223M'
        #     logger.error(f'{self.info}')
        #     logger.error(error)
        #     # self.feishuRobot(self.info)

        # if len(send_requests.json()['data']['result'][0]['cmd']) != 0:
        #     for i in range(len(send_requests.json()['data']['result'][0]['cmd'])-1):
        #         self.list2.append(send_requests.json()['data']['result'][i]['cmd'])
        #     # logger.info(self.list2)
        #     # if all(elem in self.list2 for elem in self.list1):
        #     if 'ATTR_SET_SERVICE' in self.list2 and 'ATTR_PUSH_EVENT' in self.list2 and 'APP_REFRESH_EVENT'in self.list2:
        #         if self.getImg() == 'close' and self.count % 2 != 0:
        #             self.info = '数据通信 SUCCESS'
        #             logger.info(f'{self.info}')
        #             self.list2 = []
        #             self.count += 1
        #         elif self.getImg() == 'open' and self.count % 2 == 0:
        #             self.info = '数据通信 SUCCESS'
        #             logger.info(f'{self.info}')
        #             self.list2 = []
        #             self.count += 1
        #     else:
        #         self.info = '【重要告警】PLAF107喂食器设备，在上一次点击开/关灯按钮，重新进入设备设置界面，开/关灯状态1分钟内未及时更新'
        #         logger.error(f'{self.info}')
        #         self.list2 = []
        #         self.feishuRobot(self.info)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--AF107开关灯后状态未及时更新实现飞书机器人提醒.log', rotation='100MB',
                   encoding='utf-8', enqueue=True)
        time.sleep(10)
        self.appHandle1()
        while True:
            time.sleep(5)
            self.appHandle2()


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：----').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)----').strip()
    # manualFeedingMode = input('请输入喂食单位定量模式：(0 最小、1 最大、2 随机)----').strip()
    testTimes = 10000
    intervalTime = 10
    logger.info('开始执行AF107开关灯后状态未及时更新实现飞书机器人提醒...')
    prodServerMonitor = PRODServerMonitor(testTimes, intervalTime)
    prodServerMonitor.main()
