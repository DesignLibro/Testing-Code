# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2022/12/6 10:21
# @File         : MQTT_Stress _Testing_Consumer.py
# @Mark        :


import time
import MySQLdb
from paho.mqtt import client as mqtt_client
from loguru import logger


class MQTTConsumer(object):
    def __init__(self):
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        logger.add(rf'../log/{self.logFilename}MQTT压测消费者.log', rotation='50MB', encoding='utf-8', enqueue=True)
        self.broker = 'demo-svc.dl-aiot.com'  # mqtt代理服务器地址
        # self.broker = '72.31.17.240'  # mqtt代理服务器地址
        # self.broker = '54.160.131.73'  # mqtt代理服务器地址
        self.port = 1883
        self.keepalive = 60  # 与代理通信之间允许的最长时间段（以秒为单位）
        self.topic = "dl/PLWF305/WF0201358B7617578/device/service/sub"  # 消息主题
        self.qos = 1
        self.username = 'zhangtao'
        self.passwd = 'zhangtao'
        self.getConnect()
        self.json_text = ''

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

    def connect_mqtt(self):
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
        client = mqtt_client.Client(client_id=self.client_id, clean_session=True)
        client.on_connect = on_connect
        client.username_pw_set(self.username, self.passwd)
        client.connect(self.broker, self.port, self.keepalive)
        client.subscribe(self.topic, self.qos)
        return client

    def subscribe(self, client: mqtt_client):
        '''订阅主题并接收消息'''

        def on_message(client, userdata, msg):
            '''订阅消息回调函数'''
            logger.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            # self.deletetOne()
            self.json_text = eval(msg.payload.decode())['msgId']
            self.deletetOne()

        # 订阅指定消息主题
        client.subscribe(self.topic)
        client.on_message = on_message

    def deletetOne(self):
        try:
            sql = f"DELETE FROM `mqtt_test` WHERE msgId = '{self.json_text}';"
            cursor = self.connect.cursor()  # 游标
            try:
                result = cursor.execute(sql)
                self.connect.commit()  # 提交事务
                logger.info(f'删除{result}条数据！{sql}')  # 或者说打印受影响的行数
            except MySQLdb.Error as error:
                logger.info(f'Error {error.args[0], error.args[1]}')
        except MySQLdb.Error as error:
            logger.info(error)
            self.connect.rollback()  # 回滚事务

    def main(self):
        '''运行订阅者'''
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()
        self.closeConnect()
        client.disconnect()


if __name__ == '__main__':
    mQTTConsumer = MQTTConsumer()
    mQTTConsumer.main()
