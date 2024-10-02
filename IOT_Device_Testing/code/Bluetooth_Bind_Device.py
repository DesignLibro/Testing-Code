# -*- coding:utf-8 -*-

'''
@Author       : rik.mei
@Date         : 2024/10/3 11:14
@File         : Bluetooth_Bind_Device.py
@Interpreter Version: python 3.12
@Description:
'''

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import logging, datetime, sys, configparser
from time import sleep
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def find_tx(tx, t=20):
    try:
        for i in range(t):
            if tx.exists():
                tx.click();break
            else:
                sleep(0.5)
    except:
        pass


def connect_dev(ssid, pwd, device_name, app):
    # 初始化环境
    log = logging.getLogger('airtest')
    log.setLevel(logging.INFO)
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    dev = connect_device('Android://')

    # 启动 自研APP
    logger.info('重新启动APP')
    stop_app(app)
    start_app(app)

    # 判断APP是否启动成功
    for i in range(80):
        sleep(2)
        if poco("Home, Tab 1 of 2").exists():
            logger.info('断言检查APP处于主页,继续 ... ')
            sleep(1)
            break
        else:
            sleep(1)
        if i == 20:
            logger.info('断言检查未发现APP处于主页,请检查环境配置。')
            sys.exit()

    # 添加设备
    # poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View")[1].child("android.view.View").child("android.widget.ImageView")[1].click()
    # poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").offspring("android.widget.ScrollView")[1].child("android.widget.ImageView")[1].click()
    logger.info('开始添加设备')
    touch([940, 185])

    # 扫描发现设备
    logger.info('开始扫描发现设备,请稍后 ...')
    for i in range(600):
        ex = poco(device_name).exists()
        if ex:
            if device_name == poco(device_name).attr('name'):
                logger.info('扫描设备成功，开始配网添加 ... ')
                poco(device_name).click()
                break
        else:
            sleep(0.5)
        if i >= 300:
            logger.info('设备扫描失败，请检查并复位设备 ... ')
            sys.exit()

    # 配置目标WiFi信息
    logger.info('开始配置目标WiFi信息 ... ')
    for i in range(5):
        ex = poco("NEXT").exists()
        if ex:
            text('pass');
            touch([868, 845])  # 定位输入框
            # tx = poco("android.widget.FrameLayout").offspring("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.widget.EditText")[0]
            # find_tx(tx)
            tx = \
                poco("android.widget.FrameLayout").offspring("android.widget.FrameLayout").child(
                    "android.view.View").child(
                    "android.view.View").child("android.view.View").child("android.view.View").child(
                    "android.view.View").child("android.view.View").child("android.view.View").child(
                    "android.widget.EditText")[0].child("android.widget.ImageView")[0]
            find_tx(tx, 4)

            # touch([868, 845]);touch([868, 845])
            text(ssid);
            sleep(0.5)
            # os.system('adb shell input text ' + pwd)
            text(pwd);
            sleep(1)
            tx = poco('NEXT');
            find_tx(tx)
            break
        else:
            sleep(0.5)

    # 设备配网连接过程中
    logger.info('设备配网连接过程中,请稍后 ... ')
    for i in range(150):
        ex = poco('GET STARTED').exists()
        if ex:
            logger.info('设备连接成功')
            poco('GET STARTED').click()
            break
        elif poco("FAILED TO ADD THE DEVICE").exists():
            logger.info('设备连接失败')
            stop_app(app)

            break
        else:
            sleep(0.5)

    # 设备连接成功，准备解绑
    for i in range(10):
        ex = poco("Home, Tab 1 of 2").exists()
        if ex:
            logger.info('已返回APP主页，刷新设备列表')
            poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child(
                "android.view.View").child("android.view.View").child("android.view.View").swipe([0, 0.5])
            sleep(2)
            logger.info('进入设备卡片')
            touch([300, 900]);
            sleep(2)

            try:
                sleep(1)
                poco("CANCEL").click();
                sleep(1)
            except:
                pass
            # try:
            #     for i in range(4):
            #         ex2 = poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View").exists()
            #         if ex2:
            #             logger.info('识别到校准弹窗')
            #             touch([500,1350]);sleep(1)
            #             logger.info('退出校准页面')
            #             touch([100,140]);sleep(1)
            #             break
            #         else: sleep(1)
            # except: logger.info('未识别到其它弹窗')
            logger.info('进入设备设置页面')
            tx = poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child(
                "android.view.View").child("android.view.View").child("android.widget.ImageView")[1]
            find_tx(tx);
            sleep(2.5)
            # touch([970,145]);sleep(2.5)
            logger.info('定位解绑按钮')
            poco("android.widget.FrameLayout").child("android.view.View").child("android.view.View").child(
                "android.view.View").child("android.view.View").child("android.view.View").swipe([0, -1.5])
            sleep(1)
            logger.info('开始解绑，请等待设备复位 <预计30s> ... ')
            poco('UNBIND DEVICE').click()
            sleep(1)
            poco('YES').click()
            sleep(30)
            break


if __name__ == '__main__':
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - [%(filename)s] [line:%(lineno)d] - %(levelname)s: %(message)s')
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = rf'..\log\{timestamp}蓝牙配网.log'
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 创建一个StreamHandler，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 创建一个Logger，用于记录日志
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.INFO)

    # 将FileHandler和StreamHandler添加到Logger中
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 创建一个配置解析器对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read(r'..\config\config.ini', encoding='utf-8')

    ssid_2g4 = config.get('test_info', 'ssid_2g4')
    pwd_2g4 = config.get('test_info', 'pwd_2g4')
    ssid_5g = config.get('test_info', 'ssid_5g')
    pwd_5g = config.get('test_info', 'pwd_5g')
    ssid_2g_and_5g = config.get('test_info', 'ssid_2g_and_5g')
    pwd_2g_and_5g = config.get('test_info', 'pwd_2g_and_5g')

    dev_mac = config.get('test_info', 'dev_mac')
    dev_model = config.get('test_info', 'dev_model')
    app_name = config.get('test_info', 'app_name')
    test_times = config.get('test_info', 'test_times')

    logger.info('\n======================= 蓝牙连接测试开始 ========================\n')

    if dev_model == 'AF107':
        dev_name = 'Space Feeder\nMAC:' + dev_mac
        logger.info('本次运行的机型为 AF107')
    elif dev_model == 'AF203':
        # dev_name = 'PLAF203 Camera Feeder\nMAC:'+dev_mac
        dev_name = 'Granary Camera Feeder\nMAC:' + dev_mac
        logger.info('本次运行的机型为 AF203')

    for i in range(10000):
        times = '============  【2.4G】当前循环测试次数: ' + str(i + 1)
        logger.info(times)
        connect_dev(ssid_2g4, pwd_2g4, dev_name, app_name)

    # for i in range(10):
    #     times = '============  【5G】当前循环测试次数: ' + str(i)
    #     logger.info(times)
    #     connect_dev(ssid_5g,pwd_5g,dev_name,app_name)

    # for i in range(50):
    #     times = '============  【二合一】当前循环测试次数: ' + str(i)
    #     logger.info(times)
    #     connect_dev(ssid_2g_and_5g,pwd_2g_and_5g,dev_name,app_name)

    logger.info('\n======================= 蓝牙连接测试结束 ========================\n')
