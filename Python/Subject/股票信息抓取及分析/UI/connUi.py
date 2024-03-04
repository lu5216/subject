import os
import sys
import pymysql
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import UI.databaseUi as databaseUi

global user_list
user_list = []

class conn_Main(QWidget):
    def __init__(self):
        super(conn_Main,self).__init__()
        self.resize(400, 300)
        self.setFixedSize(400, 300)
        self.setWindowTitle('连接数据库')

        self.initUI()
    

    def initUI(self):
        self.label1 = QLabel("用户：")
        self.lineEdit1 = QLineEdit()
        self.label2 = QLabel("密码：")
        self.lineEdit2 = QLineEdit()
        self.text_btn = QPushButton('测试')
        self.ok_btn = QPushButton('确定')
        self.exit_btn = QPushButton('取消')

        # 样式
        self.lineEdit2.setEchoMode(QLineEdit.Password)    # 密码模式
        self.label1.setFont(QFont("KaiTi",13,QFont.Bold))
        self.label2.setFont(QFont("KaiTi",13,QFont.Bold))
        self.lineEdit1.setFont(QFont("KaiTi",13,QFont.Bold))
        self.lineEdit2.setFont(QFont("KaiTi",13,QFont.Bold))
        self.text_btn.setFont(QFont("KaiTi",13))
        self.ok_btn.setFont(QFont("KaiTi",13))
        self.exit_btn.setFont(QFont("KaiTi",13))

        # 布局
        Vlayout = QVBoxLayout()
        Hlayout1 = QHBoxLayout()
        Hlayout1.addWidget(self.label1)
        Hlayout1.addWidget(self.lineEdit1)
        Hlayout2 = QHBoxLayout()
        Hlayout2.addWidget(self.label2)
        Hlayout2.addWidget(self.lineEdit2)
        Hlayout3 = QHBoxLayout()
        Hlayout3.addStretch(1)
        Hlayout3.addWidget(self.text_btn)
        Hlayout3.addStretch(1)
        Hlayout3.addWidget(self.ok_btn)
        Hlayout3.addStretch(1)
        Hlayout3.addWidget(self.exit_btn)
        Vlayout.addLayout(Hlayout1)
        Vlayout.addLayout(Hlayout2)
        Vlayout.addLayout(Hlayout3)
        

        self.setLayout(Vlayout)

        # 点击事件
        self.text_btn.clicked.connect(self.text_click)
        self.ok_btn.clicked.connect(lambda:self.ok_click())
        self.exit_btn.clicked.connect(self.close)


    def text_click(self):
        user = self.lineEdit1.text()
        password = self.lineEdit2.text()
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user=user, password=password, charset='utf8')
            QMessageBox.about(self, '连接成功', f'数据库连接成功！！！\n用户 = {user}\n密码 = ******\n')
            user_list.append(user)
            user_list.append(password)
            conn.close()
        except:
            QMessageBox.critical(self, '连接失败', '用户、密码或架构错误，请重新输入！！！')
        

    def ok_click(self):
        user = self.lineEdit1.text()
        password = self.lineEdit2.text()
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user=user, password=password, charset='utf8')
            if len(user_list) == 0:         # 判断是否为空
                user_list.append(user)
                user_list.append(password)
            conn.close()
            # 进入数据库操作页面
            self.databasemain = databaseUi.DatabaseMain()
            self.databasemain.show()
            self.close()
        except:
            QMessageBox.critical(self, '连接失败', '用户、密码或架构错误，请重新输入！！！')



def conn_database():
    return user_list
