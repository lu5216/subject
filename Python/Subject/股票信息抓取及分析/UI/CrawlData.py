import os
import sys
import time
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Stock import stock_pa


class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()
        self.resize(400, 300)
        self.setFixedSize(400, 300)
        self.setWindowTitle('爬取的页数')
        self.initUI()


    def initUI(self):
        self.label = QLabel("输入爬取的页数：")
        self.sb = QSpinBox()
        self.ok_btn = QPushButton('确定')
        self.exit_btn = QPushButton('取消')

        # 样式
        self.label.setFont(QFont("KaiTi",13,QFont.Bold))
        self.sb.setFont(QFont("KaiTi",20))
        self.ok_btn.setFont(QFont("KaiTi",13))
        self.exit_btn.setFont(QFont("KaiTi",13))

        self.sb.setValue(10)       # 设置初始显示的值
        self.sb.setRange(1,99)     # 设值范围

        # 布局
        Vlayout = QVBoxLayout()
        Vlayout.addStretch(1)
        Vlayout.addWidget(self.label)
        Vlayout.addStretch(1)
        Vlayout.addWidget(self.sb)
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
        page = int(self.sb.text())
        time_stamp = int(time.time())             # 时间戳
        time_local = time.localtime(time_stamp)   #转换成localtime
        dt = time.strftime("%Y%m%d-%Hh%Mm%Ss",time_local)
        stock_pa.getdata_tocsv(page=page,dt=dt)   # 爬取数据
        stock_pa.getcsv_todatabase(dt=dt)         # 存入数据库

        self.close()



