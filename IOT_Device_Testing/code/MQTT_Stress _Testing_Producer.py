# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 12:02
@File         : MQTT_Stress _Testing_Producer.py
@Interpreter Version: python 3.12
@Description:
'''

import time
import json
import MySQLdb
from paho.mqtt import client as mqtt_client
from loguru import logger


class MQTTProducer(object):
    def __init__(self):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        logger.add(rf'../log/{self.logFilename}MQTT压测生产者.log', rotation='50MB', encoding='utf-8', enqueue=True)
        self.broker = 'sit-svc.dl-aiot.com'  # mqtt代理服务器地址
        # # self.broker = '72.31.17.240'  # mqtt代理服务器地址
        # self.broker = '54.160.131.73'  # mqtt代理服务器地址
        self.port = 1883
        self.keepalive = 60  # 与代理通信之间允许的最长时间段（以秒为单位）
        self.topic = "dl/PLAF203/AF030120FBF9B937Z/device/event/post"  # 消息主题
        self.qos = 1
        self.username = 'BL1032DZXTPXN4AM'
        self.passwd = 'EB3R5MS83PYJTUNOPAJSZXM26BXY6NWD'
        self.getConnect()
        self.remarks = ''

    def getConnect(self):  # 连接数据库
        try:
            self.connect = MySQLdb.connect(
                host='10.18.0.8',
                user='dladmin',
                passwd='ZT1qdl@PET',
                db='dl_cloud',
                charset='utf8'
            )  # 获取Mysql连接
        except MySQLdb.Error as error:
            logger.info(f'Error {error.args[0], error.args[1]}')

    def closeConnect(self):  # 关闭数据库连接
        try:
            if self.connect:
                self.connect.close()  # 断开连接
        except MySQLdb.Error as error:
            logger.info(f'Error {error.args[0], error.args[1]}')

    def getTime(self):
        self.client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 客户端id不能重复
        return self.client_id

    def connect_mqtt(self):  # 连接MQTT
        '''连接mqtt代理服务器'''

        def on_connect(client, userdata, flags, rc):
            '''连接回调函数'''
            # 响应状态码为0表示连接成功
            if rc == 0:
                logger.info("Connected to MQTT OK!")
            else:
                logger.info(f"Failed to connect, return code {rc}")

        self.getTime()
        # 连接mqtt代理服务器，并获取连接引用
        client = mqtt_client.Client(self.client_id, clean_session=False)
        client.on_connect = on_connect
        client.username_pw_set(self.username, self.passwd)
        client.connect(self.broker, self.port, self.keepalive)
        client.subscribe(self.topic, self.qos)
        return client

    def publish(self, client):
        '''发布消息'''
        while True:
            self.getTime()
            current_milli_time = lambda: int(round(time.time() * 1000))
            '''每隔20秒发布一次信息'''
            time.sleep(1)
            self.msg = json.dumps({
                "cmd": "GRAIN_OUTPUT_EVENT",
                "ts": current_milli_time(),
                "msgId": f"{self.client_id}",
                # "finished": False,
                "type": 2,
                "expectGrainNum": 1,
                "actualGrainNum": 0,
                "execTime": current_milli_time(),
                "execStep": "GRAIN_START"
            })
            self.insertOne()
            result = client.publish(self.topic, self.msg)
            status = result[0]
            if status == 0:
                logger.info(f"Send `{self.msg}` to topic `{self.topic}`")
            else:
                self.remarks = f'Failed to send message to topic {self.topic}'
                self.updateOne()
                logger.info(f"Failed to send message to topic {self.topic}")

    def insertOne(self):  # 插入单条数据
        try:
            sql = f"INSERT INTO `mqtt_test` (`msgId`, `create_time`, `remarks`) VALUES ('{self.client_id}', '{self.getTime()}', '{self.remarks}');"
            cursor = self.connect.cursor()  # 游标
            try:
                result = cursor.execute(sql)
                self.connect.commit()  # 提交事务
                logger.info(f'插入{result}条数据！{sql}')  # 或者说打印受影响的行数
            except MySQLdb.Error as error:
                logger.info(f'Error {error.args[0], error.args[1]}')
        except MySQLdb.Error as error:
            logger.info(error)
            self.connect.rollback()  # 回滚事务

    def updateOne(self):  # 更新单条数据
        try:
            sql = f"UPDATE `mqtt_test` SET remarks='{self.remarks}' WHERE msgId='{self.client_id}';"
            cursor = self.connect.cursor()  # 游标
            try:
                result = cursor.execute(sql)
                self.connect.commit()  # 提交事务
                logger.info(f'更新{result}条数据！{sql}')  # 或者说打印受影响的行数
            except MySQLdb.Error as error:
                logger.info(f'Error {error.args[0], error.args[1]}')
        except MySQLdb.Error as error:
            logger.info(error)
            self.connect.rollback()  # 回滚事务

    def main(self):
        '''运行发布者'''
        client = self.connect_mqtt()
        client.loop_start()  # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
        # client.loop_forever()
        self.publish(client)
        self.closeConnect()
        client.disconnect()


if __name__ == '__main__':
    mQTTProducer = MQTTProducer()
    mQTTProducer.main()
