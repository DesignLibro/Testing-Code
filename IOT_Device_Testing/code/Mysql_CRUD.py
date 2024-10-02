# -*- coding:utf-8 -*-

'''
@Author       : lucky.wang
@Date         : 2024/10/3 14:48
@File         : Mysql_CRUD.py
@Interpreter Version: python 3.12
@Description:
'''

import MySQLdb
from loguru import logger


class MQTTMysqlCRUD(object):
    def __init__(self):
        self.getConnect()

    def getConnect(self):
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

    def closeConnect(self):
        try:
            if self.connect:
                self.connect.close()  # 断开连接
        except MySQLdb.Error as error:
            logger.info(f'Error {error.args[0], error.args[1]}')

    def insertOne(self):
        try:
            sql = "INSERT INTO `mqtt_test` (`msgId`, `create_time`) VALUES ('刘', '2022-11-11 11:11:11');"
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

    def deletetOne(self):
        try:
            sql = "DELETE FROM `mqtt_test` WHERE msgId = '刘';"
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


if __name__ == '__main__':
    mQTTMysqlCRUD = MQTTMysqlCRUD()
    # mQTTMysqlCRUD.insertOne()
    mQTTMysqlCRUD.deletetOne()
