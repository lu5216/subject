import os
import sys
import pymysql
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from UI import connUi
from UI.Database import choose_database

class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()
        self.resize(400, 300)
        self.setFixedSize(400, 300)
        self.setWindowTitle('选择数据库')

        self.show_database()
        self.initUI()


    def show_database(self):
        user_list =  connUi.conn_database()         # 获取user,password
        framework = choose_database.choose_text()        # 获取database
        conn = pymysql.connect(host='127.0.0.1', port=3306, user=user_list[0], password=user_list[1], database=framework, charset='utf8')
        self.items = []
        try:
            with conn.cursor() as cursor:
                sql = '''SHOW TABLES'''
                cursor.execute(sql)
                table = cursor.fetchall()
            # table是元组嵌套元组
            for i in range(len(table)):
                for j in range(len(table[i])):
                    self.items.append(table[i][j])
        finally:
            cursor.close()
            conn.commit()
            conn.close()


    def initUI(self):
        self.label = QLabel("请选择表：")
        self.combo = QComboBox()
        self.ok_btn = QPushButton('确定')
        self.exit_btn = QPushButton('取消')

        # 样式
        self.label.setFont(QFont("KaiTi",13,QFont.Bold))
        self.combo.setFont(QFont("KaiTi",20))
        self.ok_btn.setFont(QFont("KaiTi",13))
        self.exit_btn.setFont(QFont("KaiTi",13))

        self.combo.addItems(self.items)

        # 布局
        Vlayout = QVBoxLayout()
        Vlayout.addStretch(1)
        Vlayout.addWidget(self.label)
        Vlayout.addStretch(1)
        Vlayout.addWidget(self.combo)
        Hlayout4 = QHBoxLayout()
        Hlayout4.addStretch(1)
        Hlayout4.addWidget(self.ok_btn)
        Hlayout4.addStretch(1)
        Hlayout4.addWidget(self.exit_btn)
        Vlayout.addStretch(1)
        Vlayout.addLayout(Hlayout4)
        
        self.setLayout(Vlayout)

        # 点击事件
        self.ok_btn.clicked.connect(self.ok_click)
        self.exit_btn.clicked.connect(self.close)


    def ok_click(self):
        global form
        form = self.combo.currentText()
        self.close()


def choose_text():
    return form
