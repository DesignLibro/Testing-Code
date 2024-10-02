# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 12:00
@File         : Button_Pressure_Test.py
@Interpreter Version: python 3.12
@Description:
'''

import time
import RPi.GPIO as GPIO
import random
import os
import argparse
from loguru import logger


def power_timer(gpio_port, test_times, timer, power_status, down_timer):
    logger.info('定时掉电(定时按键)测试开始...')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_port, GPIO.OUT)
    count = 0
    for i in range(test_times):
        # logger.info(f'设备上电前状态：{GPIO.input(gpio_port)}')
        GPIO.output(gpio_port, power_status[0])
        logger.info(f'等待 {timer} 秒开始掉电，当前状态：{GPIO.input(gpio_port)}')
        time.sleep(timer)
        GPIO.output(gpio_port, power_status[1])
        logger.info(f'掉电完成，等待{down_timer}秒后重新上电')
        time.sleep(down_timer)
        count += 1
        logger.info(f'剩余测试次数为：{test_times - count}')
    GPIO.cleanup()


def power_increment(gpio_port, test_times, start_time, increment, end_time, power_status, down_timer):
    logger.info('增量掉电(增时按键)测试开始...')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_port, GPIO.OUT)
    s_time = start_time
    count = 0
    for i in range(test_times):
        # logger.info(f'设备上电前状态：{GPIO.input(gpio_port)}')
        GPIO.output(gpio_port, power_status[0])  # 上电
        logger.info(f'等待 {s_time} 秒开始掉电，当前状态：{GPIO.input(gpio_port)}')
        time.sleep(s_time)  # 上电多久开始掉电
        GPIO.output(gpio_port, power_status[1])  # 掉电
        logger.info(f'掉电完成，等待{down_timer}秒后重新上电')
        time.sleep(down_timer)
        s_time += increment
        if s_time >= end_time:
            s_time = start_time
        count += 1
        logger.info(f'剩余测试次数为：{test_times - count}')
    GPIO.cleanup()


def power_random(gpio_port, test_times, start_time, end_time, power_status, down_timer):
    logger.info('随机掉电(随机按键)测试开始')
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式
    GPIO.setup(gpio_port, GPIO.OUT)  # 设置GPIO口为输出模式
    count = 0
    for i in range(test_times):
        # logger.info(f'设备上电前状态：{GPIO.input(gpio_port)}')
        GPIO.output(gpio_port, power_status[0])
        s_time = random.randint(start_time, end_time) + random.random()
        logger.info(f'等待 {s_time} 秒开始掉电，当前状态：{GPIO.input(gpio_port)}')
        time.sleep(s_time)
        GPIO.output(gpio_port, power_status[1])
        logger.info(f'掉电完成，等待{down_timer}秒后重新上电')
        time.sleep(down_timer)
        count += 1
        logger.info(f'剩余测试次数为：{test_times - count}')
    GPIO.cleanup()


if __name__ == '__main__':
    logger.warning('每次测试完后需要注意电磁铁的状态，只有当电磁铁为不弹出时才能结束测试，切记！！！')
    logger.warning('以下参数只有日志路径可以不输入，其它参数都要输入，切记！！！\n')
    logger.info('按键专项测试开始...')

    gpio_port = int(input("请输入对应掉电的GPIO口（默认为4）:---- ").strip())
    test_mode = int(input("请选择测试类型对应数字（1：定时掉电，2：增量掉电，3：随机掉电）：---- ").strip())
    test_times = int(input("请输入测试次数：---- ").strip())
    log_flag = input("输入日志保存路径，不输入默认脚本本地log文件夹路径（可以不输入）：---- ").strip()
    high_flag = int(input("输入继电器高低电平模式（1：高电平上电，2：低电平上电），默认为1：---- ").strip())
    down_timer = int(input("请输入上电间隔时间：---- ").strip())
    # if down_timer is not None and down_timer != 5:
    #     down_timer = down_timer
    # else:
    #     down_timer = 5

    time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    logs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')
    if len(log_flag) >= 1:
        log_file = f'{log_flag}/pown_down_{time_stamp}.log'
    else:
        log_file = os.path.join(logs_path, f'pown_down_{time_stamp}.log')
    logger.add(log_file, encoding='utf-8')
    if high_flag > 1 and high_flag == 2:
        power_status = [GPIO.LOW, GPIO.HIGH]
    else:
        power_status = [GPIO.HIGH, GPIO.LOW]

    if test_mode == 1:
        timer = int(input("定时掉电-请输入定时掉电时间（单位秒）：----"))
        logger.info(
            f'配置：定时掉电，GPIO口：{gpio_port}，测试次数：{test_times}，日志路径：{log_file}, 定时掉电时间：{timer}, 上电间隔时间：{down_timer}')
        power_timer(gpio_port, test_times, timer, power_status, down_timer)
    elif test_mode == 2:
        start_time = float(input("增量掉电-请输入第一次掉电时间（单位秒）：----"))
        increment = float(input("增量掉电-请输入每次掉电递增时间间隔（单位秒）：----"))
        end_time = float(input("增量掉电-请输入掉电时间最长上限（单位秒）：----"))
        logger.info(
            f'配置：增量掉电，GPIO口：{gpio_port}，测试次数：{test_times}，日志路径：{log_file}, 第一次掉电：{start_time}, 递增间隔：{increment}，最长上限：{end_time}')
        power_increment(gpio_port, test_times, start_time, increment, end_time, power_status, down_timer)
    elif test_mode == 3:
        start_time = int(input("随机掉电-请输入随机掉电时间区间的最小值（单位秒）：----"))
        end_time = int(input("随机掉电-请输入随机掉电时间区间的最大值（单位秒）：----"))
        logger.info(
            f'配置：随机掉电，GPIO口：{gpio_port}，测试次数：{test_times}，日志路径：{log_file}, 最小值时间：{start_time}, 最大值时间：{end_time}')
        power_random(gpio_port, test_times, start_time, end_time, power_status, down_timer)
    else:
        logger.error('请选择正常测试类型！！！')
    logger.info(f'测试结束，日志路径：{log_file}')
