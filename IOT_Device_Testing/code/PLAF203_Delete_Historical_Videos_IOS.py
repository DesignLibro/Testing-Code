# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 11:52
@File         : PLAF203_Delete_Historical_Videos_IOS.py
@Interpreter Version: python 3.12
@Description:: 1.需提前在ios手机上打开APP;
              : 2.元素大概率捕获失败，主要是进度条消失后，相关的元素无法捕获，主要是不知道什么时候能加载出视频，元素什么时候出现;
              : 3.跑脚本期间需要把捕获元素的放大镜工具退出掉;
              : 4.难解决的点：目前全屏历史视频界面的删除按钮和返回按钮，无法通过坐标和元素定位方式点击，脚本终止编写;
@TechnicalBarriers:
KnowledgePoints: 1.appium官方文档：https://www.kancloud.cn/testerhome/appium_docs_cn/2001853
'''

import time
from loguru import logger
from appium import webdriver
from appium.webdriver.common.appiumby import By


class DeleteHistoryVideo(object):
    def __init__(self, testTimes, intervalTime):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        self.desired_capabilities = {
            "platformName": "IOS",
            "platformVersion": "16.4.1",
            "deviceName": "iPhone",
            "automationName": "XCUITest",
            "bundleId": "com.designlibro.petlibro",  # 在爱思助手的“应用游戏”中右击复制标识即可
            "udid": "00008101-00190D581EBA001E",
            "webDriverAgentUrl": "http://127.0.0.1:8299/",
            "usePrebuiltWDA": False,
            "useXctestrunFile": False,
            "skipLogCapture": True,
            "fullReset": False,
            "autoLaunch": True,
            # "noReset": True,
            # "autoAcceptAlerts": True,  # 当警告弹出的时候，都会自动去点接受。包括隐私访问权限的警告（例如 定位，联系人，照片）。默认值为 false。
            # "appName": "PETLIBRO",
        }

        self.testTimes = int(testTimes)
        self.intervalTime = int(intervalTime)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_capabilities)
        self.width = self.driver.get_window_size()['width']  # 屏幕的横向分辨率
        self.height = self.driver.get_window_size()['height']  # 屏幕的纵向分辨率

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y)

    def swipeDown(self):
        x1 = int(0.7954 * self.width)
        y1 = int(0.7346 * self.height)
        y2 = int(0.7900 * self.height)
        self.swipe(x1, y1, x1, y2, 2000)

    def getDeleteHistoryPlayScreenshotSuccess(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203删除历史视频 SUCCESS.png')
        logger.info('PLAF203删除历史视频成功的APP截图保存')

    def getDeleteHistoryPlayScreenshotFail(self, count):
        self.driver.get_screenshot_as_file(
            rf'../result/{self.logFilename}--第{count}次PLAF203删除历史视频 FAIL.png')
        logger.info('PLAF203删除历史视频的APP截图保存')

    def deleteHistoryPlayHandle(self, count):
        for i in range(2):
            if 'Home, Tab 1 of 2' or 'Me, Tab 2 of 2' in self.driver.page_source:
                logger.info('step1：当前APP处于设备首页')
                break
            else:
                logger.error('step1：当前APP未处于设备首页')
                self.swipeDown()
        time.sleep(3)
        self.driver.execute_script("mobile: tap", {"x": 137 / 390 * self.width, "y": 244 / 844 * self.height})
        logger.info('step2：点击设备卡片');
        time.sleep(2)

        if 'Schedule' in self.driver.page_source:
            logger.info('step3：当前APP处于设备面板');
            time.sleep(2)
            self.driver.find_element('xpath',
                                     '//XCUIElementTypeApplication[@name="PETLIBRO"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeImage[10]').click();
            time.sleep(3)
            logger.info('step4：点击实时流窗口的“回放”按钮');
            time.sleep(2)

            self.driver.find_element('xpath',
                                     '//XCUIElementTypeApplication[@name="PETLIBRO"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeImage[3]').click()
            logger.info('step5：点击历史视频流窗口的“全屏”按钮');
            time.sleep(2)

            self.driver.find_element(By.ID, '48000000-0000-0000-B603-000000000000').click()
            # self.driver.find_element('id', '48000000-0000-0000-B603-000000000000').click()
            logger.info('step6：点击历史视频流窗口的“删除”按钮');
            time.sleep(2)

            self.driver.find_element('id', '48000000-0000-0000-B603-000000000000').click()
            logger.info('step6：点击历史视频流窗口的“删除”按钮');
            time.sleep(2)

            self.driver.find_element('id', '48000000-0000-0000-B603-000000000000').click()
            logger.info('step6：点击历史视频流窗口的“删除”按钮');
            time.sleep(2)
            #
            # self.driver.find_element('xpath', '//XCUIElementTypeApplication[@name="PETLIBRO"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[5]/XCUIElementTypeImage[4]').click()
            # logger.info('step6：点击历史视频流窗口的“删除”按钮');time.sleep(2)
            #
            # self.driver.find_element('xpath', '//XCUIElementTypeImage[@name="返回返回"]').click()
            # logger.info('step7：点击确认删除窗口的“删除”按钮');time.sleep(2)
            #
            # self.getDeleteHistoryPlayScreenshotSuccess(count)
            #
            # self.driver.find_element('xpath', '//XCUIElementTypeButton[@name="OK"]').click()
            # logger.info('step8：点击“OK”按钮');time.sleep(3)

            self.driver.execute_script("mobile: tap", {"x": 5 / 390 * self.height, "y": 75 / 844 * self.height})
            logger.info('step9：点击左上角的返回按钮');
            time.sleep(2)

            # self.driver.find_element(By.NAME, '返回返回').click()
            # logger.info('step10：点击左上角的返回按钮');time.sleep(2)
            print(self.driver.page_source)

            # self.driver.find_element('xpath', '').click()
            # logger.info('step11：点击回放界面左上角的返回按钮');time.sleep(2)
            #
            # self.driver.find_element('xpath', '').click()
            # logger.info('step12：点击实时流界面左上角的返回按钮');time.sleep(2)

    def main(self):
        logger.add(rf'../log/{self.logFilename}--PLAF203删除历史视频专项测试.log', rotation='100MB', encoding='utf-8',
                   enqueue=True)
        for count in range(1, self.testTimes + 1):
            # try:
            #     self.deleteHistoryPlayHandle(count)
            #     logger.info(f'执行第 {count} 次PLAF203删除历史视频完成')
            #     time.sleep(self.intervalTime)
            # except:
            #     logger.error(f'执行第 {count} 次PLAF203删除历史视频出现异常')
            self.deleteHistoryPlayHandle(count)
            logger.info(f'执行第 {count} 次PLAF203删除历史视频完成')
            time.sleep(self.intervalTime)
            remainingTimes = self.testTimes - count
            logger.info(f'剩余测试PLAF203删除历史视频的次数为：{remainingTimes}')
            if count == self.testTimes:
                logger.info('PLAF203删除历史视频专项测试结束！')


if __name__ == '__main__':
    # testTimes = input('请输入测试次数：---- ').strip()
    # intervalTime = input('请输入每轮测试间隔时间：(单位：S，不低于60S)---- ').strip()
    testTimes = 1000
    intervalTime = 2
    logger.info('开始执行PLAF203删除历史视频专项自动化测试...')
    # try:
    #     deleteHistoryVideo = DeleteHistoryVideo(testTimes, intervalTime)
    #     deleteHistoryVideo.main()
    # except Exception as error:
    #     logger.info('An exception happened: ' + str(error))
    deleteHistoryVideo = DeleteHistoryVideo(testTimes, intervalTime)
    deleteHistoryVideo.main()
