# -*- coding:utf-8 -*-

'''
@Author       : neil.fan
@Date         : 2024/09/10 14:39
@File         : PLWF305_Single_Cat_Scene_11.py
@Interpreter Version: python 3.12
@Description: 场景11：A猫饮水，水位持续30S上下波动，上下起伏5ml，波动过程中水饮水，识别RFID30次，每秒饮水0.5ml，水量平稳后继续饮水，识别RFID30次，每秒饮水0.5ml；
'''

import time
import uuid
import json
import hashlib
import os
from paho.mqtt import client as mqtt_client
from loguru import logger
from PLWF305_Drinking_Algorithm_Testing.general_funcation.general_reload_yaml import ReloadYaml


class MQTTProducer(object):
    def __init__(self):
        self.script_name_with_extension = os.path.basename(__file__)  # 获取当前脚本的完整路径
        self.script_name = os.path.splitext(self.script_name_with_extension)[0]  # 去掉文件扩展名
        self.logFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

        '''实例化ReloadYaml对象reloadYaml'''
        self.reloadYaml = ReloadYaml()
        self.reloadYaml.main()
        self.broker = self.reloadYaml.mqtt_env['demo']
        self.port = self.reloadYaml.mqtt_port
        self.keepalive = self.reloadYaml.keepalive
        self.qos = self.reloadYaml.qos

        self.WF305_USERNAME = self.reloadYaml.WF305_USERNAME
        self.WF305_PASSWD = self.reloadYaml.WF305_PASSWD
        self.WF305_SN = self.reloadYaml.WF305_SN
        self.RFID_SN_A = self.reloadYaml.RFID_SN_A
        self.RFID_SN_B = self.reloadYaml.RFID_SN_B
        self.WF305_WEIGHT_PERCENT = self.reloadYaml.WF305_WEIGHT_PERCENT

        self.topic = f'dl/PLWF305/{self.WF305_SN}/device/event/post'
        self.client_id = self.WF305_SN

        logger.add(rf'../log/{self.script_name}_{self.logFilename}.log', rotation='50MB', encoding='utf-8',
                   enqueue=True)

    def calculate_md5(self, content):
        md5_hash = hashlib.md5()
        content_bytes = content.encode('utf-8')
        md5_hash.update(content_bytes)
        md5_digest = md5_hash.hexdigest()
        return md5_digest

    def getClient_id(self):
        self.client_id_info = str(uuid.uuid4()).replace('-', '')
        return self.client_id_info

    def connect_mqtt(self):
        '''连接mqtt代理服务器'''

        def on_connect(client, userdata, flags, rc):
            '''连接回调函数'''
            if rc == 0:
                logger.info("Connected to MQTT OK!")
            else:
                logger.error(f"Failed to connect, return code {rc}")

        # 连接mqtt代理服务器，并获取连接引用
        client = mqtt_client.Client(client_id=self.client_id, clean_session=True)
        client.on_connect = on_connect
        client.username_pw_set(self.WF305_USERNAME, self.WF305_PASSWD)
        client.connect(self.broker, self.port, self.keepalive)
        client.subscribe(self.topic, self.qos)
        return client

    def publish(self, client):
        '''发布消息'''
        # while True:
        self.getClient_id()
        self.weight_percent_decrement = 0.5
        self.time_increment = 1000
        self.start_weight_percent = 2308
        self.previous_weight_percent = self.start_weight_percent

        for i in range(1, 2):
            '''定量上报1，心跳上报'''
            for a in range(1, 16):
                current_time = int(time.time() * 1000)
                self.msg4 = json.dumps(
                    {
                        "cmd": "HEARTBEAT",
                        "count": a,
                        "rssi": -46,
                        "wifiType": 1,
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "ts": current_time
                    }
                )
                result4 = client.publish(self.topic, self.msg4)
                status4 = result4[0]
                if status4 == 0:
                    logger.info(f"Send `{self.msg4}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")
                time.sleep(15)

                current_time = int(time.time() * 1000)
                self.msg1 = json.dumps(
                    {
                        "cmd": "WATER_CAP_EVENT",
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "content": [
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 1,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 2,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 3,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 4,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 5,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 6,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 7,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 8,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 9,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 10,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 11,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 12,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 13,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 14,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent,
                                "ts": current_time + self.time_increment * 15,
                                "rfid": ""
                            }
                        ],
                        "ts": current_time + self.time_increment * 15
                    }
                )

                result1 = client.publish(self.topic, self.msg1)
                status1 = result1[0]
                if status1 == 0:
                    logger.info(f"Send `{self.msg1}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")

            '''波动上报2，心跳上报'''
            for a in range(1, 3):
                current_time = int(time.time() * 1000)
                self.msg4 = json.dumps(
                    {
                        "cmd": "HEARTBEAT",
                        "count": a,
                        "rssi": -46,
                        "wifiType": 1,
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "ts": current_time
                    }
                )
                result4 = client.publish(self.topic, self.msg4)
                status4 = result4[0]
                if status4 == 0:
                    logger.info(f"Send `{self.msg4}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")
                time.sleep(15)

                '''波动上报2'''
                current_time = int(time.time() * 1000)
                self.msg1 = json.dumps(
                    {
                        "cmd": "WATER_CAP_EVENT",
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "content": [
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent + 5 - self.weight_percent_decrement * 1,
                                "ts": current_time + self.time_increment * 1,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 2,
                                "ts": current_time + self.time_increment * 2,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - 5 - self.weight_percent_decrement * 3,
                                "ts": current_time + self.time_increment * 3,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 4,
                                "ts": current_time + self.time_increment * 4,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent + 5 - self.weight_percent_decrement * 5,
                                "ts": current_time + self.time_increment * 5,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 6,
                                "ts": current_time + self.time_increment * 6,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - 5 - self.weight_percent_decrement * 7,
                                "ts": current_time + self.time_increment * 7,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 8,
                                "ts": current_time + self.time_increment * 8,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent + 5 - self.weight_percent_decrement * 9,
                                "ts": current_time + self.time_increment * 9,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 10,
                                "ts": current_time + self.time_increment * 10,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - 5 - self.weight_percent_decrement * 11,
                                "ts": current_time + self.time_increment * 11,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 12,
                                "ts": current_time + self.time_increment * 12,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent + 5 - self.weight_percent_decrement * 13,
                                "ts": current_time + self.time_increment * 13,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 14,
                                "ts": current_time + self.time_increment * 14,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": self.previous_weight_percent - self.weight_percent_decrement * 15,
                                "ts": current_time + self.time_increment * 15,
                                "rfid": f"{self.RFID_SN_A}"
                            }
                        ],
                        "ts": current_time + self.time_increment * 15
                    }
                )

                result1 = client.publish(self.topic, self.msg1)
                status1 = result1[0]
                if status1 == 0:
                    logger.info(f"Send `{self.msg1}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")

            '''减量上报，心跳上报'''
            for b in range(1, 3):
                # RFID识别15S正常上报
                current_time = int(time.time() * 1000)
                self.msg5 = json.dumps(
                    {
                        "cmd": "HEARTBEAT",
                        "count": b + 10,
                        "rssi": -46,
                        "wifiType": 1,
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "ts": current_time
                    }
                )
                result5 = client.publish(self.topic, self.msg5)
                status5 = result5[0]
                if status5 == 0:
                    logger.info(f"Send `{self.msg5}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")
                time.sleep(15)

                current_time = int(time.time() * 1000)
                self.msg2 = json.dumps(
                    {
                        "cmd": "WATER_CAP_EVENT",
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "content": [
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 1,
                                                1),
                                "ts": current_time + self.time_increment * 1,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 2,
                                                1),
                                "ts": current_time + self.time_increment * 2,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 3,
                                                1),
                                "ts": current_time + self.time_increment * 3,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 4,
                                                1),
                                "ts": current_time + self.time_increment * 4,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 5,
                                                1),
                                "ts": current_time + self.time_increment * 5,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 6,
                                                1),
                                "ts": current_time + self.time_increment * 6,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 7,
                                                1),
                                "ts": current_time + self.time_increment * 7,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 8,
                                                1),
                                "ts": current_time + self.time_increment * 8,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 9,
                                                1),
                                "ts": current_time + self.time_increment * 9,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 10,
                                                1),
                                "ts": current_time + self.time_increment * 10,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 11,
                                                1),
                                "ts": current_time + self.time_increment * 11,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 12,
                                                1),
                                "ts": current_time + self.time_increment * 12,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 13,
                                                1),
                                "ts": current_time + self.time_increment * 13,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 14,
                                                1),
                                "ts": current_time + self.time_increment * 14,
                                "rfid": f"{self.RFID_SN_A}"
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent - self.weight_percent_decrement * 15,
                                                1),
                                "ts": current_time + self.time_increment * 15,
                                "rfid": f"{self.RFID_SN_A}"
                            }
                        ],
                        "ts": current_time + self.time_increment * 15
                    }
                )

                result2 = client.publish(self.topic, self.msg2)
                status2 = result2[0]
                if status2 == 0:
                    logger.info(f"Send `{self.msg2}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")

                self.previous_weight_percent -= (15 * self.weight_percent_decrement)

            '''定量上报2，心跳上报'''
            for c in range(1, 16):
                current_time = int(time.time() * 1000)
                self.msg6 = json.dumps(
                    {
                        "cmd": "HEARTBEAT",
                        "count": c + 13,
                        "rssi": -46,
                        "wifiType": 1,
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "ts": current_time
                    }
                )
                result6 = client.publish(self.topic, self.msg6)
                status6 = result6[0]
                if status6 == 0:
                    logger.info(f"Send `{self.msg6}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")
                time.sleep(15)

                current_time = int(time.time() * 1000)
                self.weightPercent = self.previous_weight_percent
                self.msg6 = json.dumps(
                    {
                        "cmd": "WATER_CAP_EVENT",
                        "msgId": f"{self.WF305_SN}{current_time}",
                        "content": [
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 1,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 2,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 3,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 4,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 5,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 6,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 7,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 8,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 9,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 10,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 11,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 12,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 13,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 14,
                                "rfid": ""
                            },
                            {
                                "weightPercent": round((int(self.start_weight_percent / 3000 * 100)), -1),
                                "weight": round(self.previous_weight_percent, 1),
                                "ts": current_time + self.time_increment * 15,
                                "rfid": ""
                            }
                        ],
                        "ts": current_time + self.time_increment * 15
                    }
                )

                result3 = client.publish(self.topic, self.msg6)
                status3 = result3[0]
                if status3 == 0:
                    logger.info(f"Send `{self.msg6}` to topic `{self.topic}`")
                else:
                    self.remarks = f'Failed to send message to topic {self.topic}'
                    logger.info(f"Failed to send message to topic {self.topic}")
            time.sleep(120)
            self.previous_weight_percent = 2308

    def main(self):
        '''运行发布者'''
        client = self.connect_mqtt()
        client.loop_start()  # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
        self.publish(client)
        time.sleep(3)
        client.disconnect()


if __name__ == '__main__':
    mQTTProducer = MQTTProducer()
    mQTTProducer.main()
