import os
import sys
import pymysql
import pandas as pd
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from sqlalchemy import create_engine, types

import UI.connUi as connUi
from UI.Database import choose_database, choose_table

class DatabaseMain(QWidget):
    def __init__(self):
        super(DatabaseMain,self).__init__()
        self.resize(1200, 700)
        self.setWindowTitle('数据库操作')

        self.initUI()
    

    def initUI(self):
        self.label1 = QLabel('数据库操作')
        self.label2 = QLabel('数据导入')
        self.dataTable = QTableWidget()
        self.comboBox = QComboBox()
        self.lineEdit = QLineEdit()
        self.choose_database_Btn = QPushButton('选择架构')
        self.choose_table_Btn = QPushButton('选择表')
        self.add_data_Btn = QPushButton('添加数据')
        self.delete_data_Btn = QPushButton('删除数据')
        self.upload_data_Btn = QPushButton('上传数据')
        self.inquire_Btn = QPushButton('查询')
        self.empty_Btn = QPushButton('清空')
        self.empty_database_Btn = QPushButton('清空数据库')
        self.create_form_Btn = QPushButton('生成表格')

        # 样式设计
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("color:blue")
        self.label1.setFont(QFont("KaiTi",15,QFont.Bold))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("color:blue")
        self.label2.setFont(QFont("KaiTi",15,QFont.Bold))
        self.choose_database_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.choose_table_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.add_data_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.delete_data_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.upload_data_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.comboBox.setFont(QFont("KaiTi",12,QFont.Bold))
        self.inquire_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.lineEdit.setFont(QFont("KaiTi",12,QFont.Bold))
        self.empty_Btn.setFont(QFont("KaiTi",12,QFont.Bold))
        self.empty_database_Btn.setFont(QFont("KaiTi",14,QFont.Bold))
        self.create_form_Btn.setFont(QFont("KaiTi",12,QFont.Bold))

        # 自适应宽
        self.dataTable.resizeColumnsToContents()
        # 隔行变色设置
        self.dataTable.setAlternatingRowColors(True)
        # 自适应窗口大小
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 布局
        VLayout1 = QVBoxLayout()
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.label1)
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.choose_database_Btn)
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.choose_table_Btn)
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.add_data_Btn)
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.delete_data_Btn)
        VLayout1.addStretch(1)
        VLayout1.addWidget(self.upload_data_Btn)

        VLayout2 = QVBoxLayout()
        VLayout2.addWidget(self.label2)
        VLayout2.addWidget(self.dataTable)
        HLayout1 = QHBoxLayout()
        HLayout1.addWidget(self.comboBox)
        HLayout1.addWidget(self.lineEdit)
        HLayout1.addWidget(self.inquire_Btn)
        HLayout1.addWidget(self.empty_Btn)
        HLayout2 = QHBoxLayout()
        HLayout2.addWidget(self.empty_database_Btn)
        HLayout2.addWidget(self.create_form_Btn)
        VLayout2.addLayout(HLayout1)
        VLayout2.addLayout(HLayout2)

        HLayout = QHBoxLayout()
        HLayout.addLayout(VLayout1)
        HLayout.addLayout(VLayout2)

        self.setLayout(HLayout)

        # 信号绑定
        self.choose_database_Btn.clicked.connect(self.choose_database_Click)
        self.choose_table_Btn.clicked.connect(self.choose_table_Click)
        self.add_data_Btn.clicked.connect(self.add_data_Click)
        self.delete_data_Btn.clicked.connect(self.delete_data_Click)
        self.create_form_Btn.clicked.connect(self.create_form_Click)
        self.upload_data_Btn.clicked.connect(self.upload_data_Click)
        self.inquire_Btn.clicked.connect(self.inquire_Click)
        self.empty_Btn.clicked.connect(self.empty_Click)
        self.empty_database_Btn.clicked.connect(self.empty_database_Click)


    # 选择架构
    def choose_database_Click(self):
        self.cd = choose_database.Main()
        self.cd.show()


    # 选择表
    def choose_table_Click(self):
        self.ct = choose_table.Main()
        self.ct.show()


    # 添加行
    def add_data_Click(self):
        # 获取总行数
        rowCount = self.dataTable.rowCount()
        # 设置行数
        self.dataTable.setRowCount(rowCount+1)


    # 删除行
    def delete_data_Click(self):
        # 获取总行数
        rowCount = self.dataTable.rowCount()
        # 设置行数
        self.dataTable.setRowCount(rowCount-1)


    # 修改数据
    def upload_data_Click(self):
        user_list =  connUi.conn_database()         # 获取user,password
        framework = choose_database.choose_text()   # 获取database
        form = choose_table.choose_text()           # 获取表名
        conn = pymysql.connect(host='localhost', port=3306, user=user_list[0], password=user_list[1], db=framework)
        cur = conn.cursor()
        # sql语句
        sql = f"SELECT * FROM `{form}`"
        cur.execute(sql)
        cur.close()
        conn.close()
        # 获取dataTable里面的内容
        row = self.dataTable.rowCount()
        col = self.dataTable.columnCount()
        data_dt = {}    # 保存为csv文件
        dtypes = {}     # 写入数据库
        for i in range(len(self.table)):
            data_dt[f'{self.table[i]}'] = []
            dtypes[f'{self.table[i]}'] = types.VARCHAR(20)
        # data.append(table)      # 将表头添加到data
        for r in range(row):
            for c in range(col):
                text_item = self.dataTable.item(r, c)
                text = text_item.text()
                data_dt[f'{self.table[c]}'].append(text)
        # 存储到临时csv文件
        df = pd.DataFrame(data_dt)
        df.to_csv('csvFile\\upload.csv', index=False)
        # 读取数据
        df = pd.read_csv('csvFile\\upload.csv')
        try:
            sql = f'{form}'
            con = create_engine(f'mysql+pymysql://{user_list[0]}:{user_list[1]}@localhost:3306/{framework}?charset=utf8')
            df.to_sql(sql, con=con, index=False, if_exists='replace', dtype=dtypes)
            QMessageBox.about(self, '上传成功', f'表格 {form} 更新成功！！！')
        except:
            QMessageBox.about(self, '上传失败', f'表格 {form} 更新失败！！！')
        

    # 查询按钮
    def inquire_Click(self):
        # 下拉框获得用户选中的文本信息
        str1 = self.comboBox.currentText()
        # 输入框获得用户输入的文本信息
        str2 = self.lineEdit.text()
        # 获取表格
        user_list =  connUi.conn_database()         # 获取user,password
        framework = choose_database.choose_text()   # 获取database
        form = choose_table.choose_text()           # 获取表名
        conn = pymysql.connect(host='localhost', port=3306, user=user_list[0], password=user_list[1], db=framework)
        cur = conn.cursor()
        sql = f"SELECT * FROM `{form}`"
        cur.execute(sql)
        data = cur.fetchall()
        df = pd.DataFrame(data)
        df.columns = self.table     # 设置df的列头为数据库列头
        # 查询
        if str2 == "":
            count = -1      # 判断查询到的列是第几列
            count_table = []
            for j in df:
                count += 1
                if str1 == j:
                    break
            # 查询成功
            if count != -1:
                count_table.append(self.table[count])    # 列名
                self.dataTable.setColumnCount(1)         # 设置表格列数
                self.dataTable.setHorizontalHeaderLabels(count_table)    # 设置列名
                # 将查询的结果填入
                for n in range(len(df[f'{str1}'])):
                    self.dataTable.item(n,0).setText(str(df.iloc[n, count]))
        else:
            flag = 0            # 判断查询是否成功
            count_list = []     # 存储所有匹配到的值
            # 根据所选列，查询所有匹配的选项
            for i in range(0, len(df[f'{str1}'])):
                if str2 == df[f'{str1}'][i]:
                    flag = 1
                    count_list.append(i)
            if flag==0:
                QMessageBox.about(self, '查询失败', f"查询失败，在'{str1}'找不到['{str2}']")
            else:
                self.dataTable.setRowCount(len(count_list))     # 设置表格行数
                # 将查询的结果填入
                for cl in range(len(count_list)):
                    for n in range(len(df[f'{str1}'])):
                        self.dataTable.item(cl,n).setText(str(df.iloc[count_list[cl], n]))


    # 清空查询
    def empty_Click(self):
        self.lineEdit.clear()


    # 清空datatable
    def empty_database_Click(self):
        self.dataTable.clear()


    # 生成表格
    def create_form_Click(self):
        self.database()
        self.comboBox.clear()               # 清空残余选项
        self.lineEdit.clear()               # 清空输入框
        self.comboBox.addItems(self.table)  # 添加选线
        framework = choose_database.choose_text()   # 获取database
        self.choose_database_Btn.setText(f"库：{framework}")
        form = choose_table.choose_text()    # 获取表名
        self.choose_table_Btn.setText(f"表：{form}")


    # 将数据信息添加到datatable
    def database(self):
        try:
            user_list =  connUi.conn_database()         # 获取user,password
            framework = choose_database.choose_text()   # 获取database
            form = choose_table.choose_text()           # 获取表名
        except:
            QMessageBox.about(self, '空表', '请选择架构和表！！！')
            return
        conn = pymysql.connect(host='localhost', port=3306, user=user_list[0], password=user_list[1], db=framework)
        cur = conn.cursor()
        # sql语句
        sql = f"SELECT * FROM `{form}`"
        cur.execute(sql)
        # 为空表时
        if cur is not None:
            # 获取查询到的数据，是以字典的形式存储的，读取使用data[i][j]下标定位
            data = cur.fetchall()
            try:
                what_i_want = data[0]   # 当查询结果为空时，这里会报错
            except:
                QMessageBox.about(self, '空表', f'表格 {form} 为空表！！！')
        
        # 显示到界面表格上
        df = pd.DataFrame(data)
        self.dataTable.setColumnCount(len(df.columns))
        self.dataTable.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.dataTable.setItem(i,j,QTableWidgetItem(str(df.iloc[i,j])))   # 设置内容

        # 获取表头
        des = cur.description
        self.table = [t[0] for t in des]
        self.dataTable.setHorizontalHeaderLabels(self.table)    # 设置列名
        # 给df添加列名
        df.columns = self.table

        # 获取数据
        global database_df
        database_df = pd.DataFrame(df)

        cur.close()
        conn.close()


def database_data():
    return database_df
