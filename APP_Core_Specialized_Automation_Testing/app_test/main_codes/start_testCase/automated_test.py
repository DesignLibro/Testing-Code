# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/2/4 16:12
# @File         : automated_test.py
# @Mark         : 
# @TechnicalBarriers: 
# @KnowledgePoints:   


import pytest
import time
import os
from loguru import logger
from feishu_send_message import send_feishu_text_Message
from ..tastCase.APP_login_CLASS_A_Android import APPLogin
from ..tastCase.AF103_buleboothBindDevice_CLASS_A_Android import AF103_buleboothBindDevice
from ..tastCase.AF103_addAndApplyFeedCall_CLASS_A_Android import AF103_addAndApplyFeedCall
from ..tastCase.AF103_manualFeed_CLASS_A_Android import AF103_manualFeed
from ..tastCase.AF103_scheduleFeed_CLASS_A_Android import AF103_scheduleFeed
from ..tastCase.AF103_unbindDevice_CLASS_A_Android import AF103_unbindDevice
from ..tastCase.AF103_ota_CLASS_A_Android import AF103_OTA

# AF103 -----------------------------------------------------------------------------------------------------------------

def test_app_login(log_test):
    # send_feishu_text_Message('开始执行新APP包自动化测试，麻烦在此期间保持当前后台环境')
    logger.info(f'开始执行APP账号密码登录测试...')
    # assert APPLogin().main() == True, 'APP账号密码登录用例执行失败'
    if APPLogin().main() == True:
        logger.info('APP账号密码登录用例执行成功')
    else:
        send_feishu_text_Message('APP账号密码登录用例执行失败，后续用例无法执行')
        logger.error('APP账号密码登录用例执行失败，后续用例无法执行')
        pytest.fail('APP账号密码登录用例执行失败，后续用例无法执行')


def test_AF103_buleboothBindDevice(log_test):
    logger.info(f'开始执行AF103产品蓝牙绑定测试...')
    # assert AF103_buleboothBindDevice().aF103_buleboothBindDevice() == True, 'AF103蓝牙绑定设备用例执行失败'
    if AF103_buleboothBindDevice().aF103_buleboothBindDevice() == True:
        logger.info('AF103蓝牙绑定设备用例执行成功')
    else:
        send_feishu_text_Message('AF103蓝牙绑定设备用例执行失败，后续用例无法执行')
        logger.error('AF103蓝牙绑定设备用例执行失败，后续用例无法执行')
        pytest.fail('AF103蓝牙绑定设备用例执行失败，后续用例无法执行')


def test_AF103_addAndApplyFeedCall(log_test):
    logger.info(f'开始执行AF103产品添加与应用喂食录音测试...')
    # assert AF103_addAndApplyFeedCall().aF103_addAndApplyFeedCall() == True, 'AF103添加与应用喂食录音用例执行失败'
    if AF103_addAndApplyFeedCall().aF103_addAndApplyFeedCall() == True:
        logger.info('AF103添加与应用喂食录音用例执行成功')
    else:
        send_feishu_text_Message('AF103添加与应用喂食录音用例执行失败，后续用例无法执行')
        logger.error('AF103添加与应用喂食录音用例执行失败，后续用例无法执行')
        pytest.fail('AF103添加与应用喂食录音用例执行失败，后续用例无法执行')


def test_AF103_manualFeed(log_test):
    logger.info(f'开始执行AF103手动喂食测试...')
    # assert AF103_manualFeed().aF103_manualFeed() == True, 'AF103手动喂食用例执行失败'
    if AF103_manualFeed().aF103_manualFeed() == True:
        logger.info('AF103手动喂食用例执行成功')
    else:
        send_feishu_text_Message('AF103手动喂食用例执行失败，后续用例无法执行')
        logger.error('AF103手动喂食用例执行失败，后续用例无法执行')
        pytest.fail('AF103手动喂食用例执行失败，后续用例无法执行')


def test_AF103_scheduleFeed(log_test):
    logger.info(f'开始执行AF103计划喂食测试...')
    # assert AF103_scheduleFeed().aF103_scheduleFeed() == True, 'AF103计划喂食用例执行失败'
    if AF103_scheduleFeed().aF103_scheduleFeed() == True:
        logger.info('AF103计划喂食用例执行成功')
    else:
        send_feishu_text_Message('AF103计划喂食用例执行失败，后续用例无法执行')
        logger.error('AF103计划喂食用例执行失败，后续用例无法执行')
        pytest.fail('AF103计划喂食用例执行失败，后续用例无法执行')


def test_AF103_ota(log_test):
    logger.info(f'开始执行AF103 ota测试...')
    # assert AF103_OTA().aF103_OTA() == True, 'AF103 ota用例执行失败'
    if AF103_OTA().aF103_OTA() == True:
        logger.info('AF103 ota用例执行成功')
    else:
        send_feishu_text_Message('AF103 ota用例执行失败，后续用例无法执行')
        logger.error('AF103 ota用例执行失败，后续用例无法执行')
        pytest.fail('AF103 ota用例执行失败，后续用例无法执行')


def test_AF103_unbindDevice(log_test):
    logger.info(f'开始执行AF103解绑设备测试...')
    # assert AF103_unbindDevice().aF103_unbindDevice() == True, 'AF103解绑设备用例执行失败'
    if AF103_unbindDevice().aF103_unbindDevice() == True:
        logger.info('AF103解绑设备用例执行成功')
    else:
        send_feishu_text_Message('AF103解绑设备用例执行失败，后续用例无法执行')
        logger.error('AF103解绑设备用例执行失败，后续用例无法执行')
        pytest.fail('AF103解绑设备用例执行失败，后续用例无法执行')





    # send_feishu_text_Message('新包自动化测试完成')

# AF107 -----------------------------------------------------------------------------------------------------------------

'''
def install_apk(apk_path_name):
    General_module(apk_path_name)
''' # 与robert联调时将此代码打开


@pytest.fixture(scope='function', autouse=True)
def log_test(request):
    current_script_path = os.path.abspath(__file__)  # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(current_script_path)  # 获取脚本所在的目录
    os.chdir(script_dir)  # 切换工作目录至脚本所在目录

    log_filename = rf"../report/{request.node.name}_{time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())}.log"
    logger.add(log_filename, encoding='utf-8')
    request.node.extra = logger  # 将日志内容添加到extra属性中


if __name__ == '__main__':
    pytest_plugins = ['pytest_html']
    pytest.main(['automated_test.py', '-v'])
