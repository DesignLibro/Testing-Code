# -*- coding:utf-8 -*-
import time

# @Author       : baolong.wang
# @Date         : 2024/3/2 15:02
# @File         : general_login.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import os
from loguru import logger
from ..generalModule.general_permission_click import PermissionClick
from ..generalModule.general_reload_yaml import ReloadYaml
from ..generalModule.general_take_down_pop import TakeDownPOP
from ..generalModule.general_phone_record import PhoneRecord
from feishu_send_message import send_feishu_text_Message


class Login(object):
    def __init__(self):
        '''实例化ReloadYaml对象reload_yaml'''
        self.reload_yaml = ReloadYaml()
        self.reload_yaml.main()
        self.user1 = self.reload_yaml.user1  # 测试APP账号1
        self.password1 = self.reload_yaml.password1  # 测试APP密码1
        self.mainTimeoutDuration = self.reload_yaml.mainTimeoutDuration  # APP登录成功后在首页的判断超时时间
        self.width = self.reload_yaml.width  # 测试手机的长像素
        self.height = self.reload_yaml.height  # 测试手机的宽像素

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

    def run(self):
        '''实例化PermissionClick对象permissionClick'''
        self.permissionClick = PermissionClick()
        self.permissionClick.runInstallAPK()
        self.driver = self.permissionClick.runGetDriver()

        time.sleep(2)
        self.permissionClick.agreePrivacyPolicy()
        time.sleep(2)
        self.permissionClick.allowAPPNotification()
        time.sleep(2)

    '''取消邀评弹窗'''
    def cancelInvitationPopup(self):
        for i in range(self.mainTimeoutDuration - 15):
            if 'ENJOYING PETLIBRO' in self.driver.page_source:
                self.driver.tap([(0.5064 * self.width, 0.7413 * self.height)], duration=1)
                logger.info('点击取消邀评弹窗')
                time.sleep(3)
                break
            else:
                time.sleep(1)

    '''出现登录失效弹框时点击OK按钮'''
    def loginExpired(self):
        for i in range(self.mainTimeoutDuration - 15):
            if self.driver.page_source:
                if 'LOGIN HAS EXPIRED' in self.driver.page_source:
                    self.driver.tap([(0.5018 * self.width, 0.6047 * self.height)], duration=1)
                    logger.info('出现登录失效弹框时点击OK按钮')
                    time.sleep(5)
                    break
                else:
                    time.sleep(1)

    '''点击登录按钮'''
    def login(self):
        # self.phoneRecord.start_screen_recording(self.output_file_name)
        self.run()  # 获取操作句柄
        time.sleep(2)
        self.loginExpired()
        try:
            self.driver.tap([(0.5083 * self.width, 0.9331 * self.height)], duration=1)
            logger.info('step1：点击登录按钮')
            time.sleep(2)

            self.driver.tap([(0.8990 * self.width, 0.2956 * self.height)], duration=1)
            logger.info('step2：点击国家与地区按钮')
            time.sleep(2)

            self.driver.tap([(0.3944 * self.width, 0.3554 * self.height)], duration=1)
            logger.info('step3：点击American Samoa按钮')
            time.sleep(4)

            '''
            self.driver.tap([(0.9629 * self.width, 0.3774 * self.height)], duration=1)
            logger.info('step3：点击C字母按钮')
            time.sleep(2)

            self.driver.tap([(0.4787 * self.width, 0.6244 * self.height)], duration=1)
            logger.info('step4：点击China')
            time.sleep(2)
            '''

            self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').click()
            logger.info('step4：点击用户账号输入栏')
            time.sleep(1)

            self.driver.tap([(0.9055 * self.width, 0.3947 * self.height)], duration=1)
            time.sleep(1)

            self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[1]').send_keys(self.user1)
            logger.info(f'step5：输入用户账号-- {self.user1}')
            time.sleep(1)

            self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').click()
            logger.info('step6：点击用户密码输入栏')
            time.sleep(1)
            self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]').send_keys(self.password1)
            logger.info(f'step7：输入用户密码-- {self.password1}')
            time.sleep(1)

            self.driver.tap([(0.0851 * self.width, 0.6024 * self.height)], duration=1)
            logger.info('step8：点击勾选协议按钮')
            time.sleep(2)

            self.driver.tap([(0.5175 * self.width, 0.6950 * self.height)], duration=1)
            logger.info('step9：点击登录按钮')
            time.sleep(2)

            for i in range(self.mainTimeoutDuration-15):
                if 'FACE ID' in self.driver.page_source or 'face id' in self.driver.page_source:
                    self.driver.tap([(0.5037 * self.width, 0.7670 * self.height)], duration=1)
                    logger.info('step10：点击禁用生物ID登录按钮')
                    break
                else:
                    time.sleep(1)

            '''调用运营平台下架邀评弹窗'''
            self.cancelInvitationPopup()  # 取消邀评弹窗

            # try:
            #     self.driver.find_element('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
            #     logger.info('点击取消POP_UP弹窗')
            #     time.sleep(2)
            # except:
            #     pass

            '''APP首页判断'''
            for i in range(self.mainTimeoutDuration):
                if self.driver.page_source:
                    if 'Device' in self.driver.page_source and 'Me' in self.driver.page_source:
                        logger.info('step11：当前APP处于设备首页')
                        logger.info(f'Finally：APP登录{self.user1}账号用例执行成功')
                        # self.phoneRecord.stop_screen_recording()
                        return True
                    else:
                        time.sleep(1)
            else:
                logger.error('Finally：登录失败，后续用例无法执行')
                # self.phoneRecord.stop_screen_recording()
                send_feishu_text_Message('Finally：当登录失败，后续用例无法执行')
                return False
        except:
            # self.phoneRecord.stop_screen_recording()
            send_feishu_text_Message('Finally：当前APP未处于设备首页，后续用例无法执行')
            return False

# Login().login()  # 调试本脚本时解除注释