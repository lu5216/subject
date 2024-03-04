import os
import sys
import csv
import pandas as pd
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from pyecharts.charts import *
from pyecharts import options as opts
import webbrowser

from UI import connUi, databaseUi
import tushare as ts


class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()
        self.resize(1000, 600)
        self.setWindowTitle('作图')           # 设置title

        self.initUI()


    def initUI(self):
        # 添加控件
        self.table = QTableWidget()
        self.label1 = QLabel("选择数据：")
        self.choose_excle_btn = QPushButton("选择excel文件")
        self.choose_data_btn = QPushButton("选择数据库")
        self.show_btn = QPushButton("确定")
        self.label2 = QLabel("设置参数：")
        self.line_label = QLabel('请选择股票：')
        self.comboBox = QComboBox()
        self.start_label = QLabel('输入开始日期：')
        self.startDateLine = QLineEdit()      # 日期
        self.end_label = QLabel('输入结束日期：')
        self.endDateLine = QLineEdit()      # 日期
        self.label3 = QLabel("生成图像：")
        self.ok_btn = QPushButton("生成K线图")

        # 添加横线
        self.frame1 = QFrame()
        self.frame1.setFrameShape(QFrame.HLine)
        self.frame1.setFrameShadow(QFrame.Sunken)
        self.frame2 = QFrame()
        self.frame2.setFrameShape(QFrame.HLine)
        self.frame2.setFrameShadow(QFrame.Sunken)

        # 样式设置
        self.table.resizeColumnsToContents()  # 自适应宽
        self.table.setAlternatingRowColors(True)   # 隔行变色设置
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        self.table.setStyleSheet("border: 1px solid black;")  # 边框颜色
        self.choose_excle_btn.setFont(QFont("KaiTi",15))
        self.choose_data_btn.setFont(QFont("KaiTi",15))
        self.show_btn.setFont(QFont("KaiTi",15))
        self.line_label.setFont(QFont("KaiTi",15))
        self.comboBox.setFont(QFont("KaiTi",15,QFont.Bold))
        self.start_label.setFont(QFont("KaiTi",15))
        self.end_label.setFont(QFont("KaiTi",15))
        self.startDateLine.setFont(QFont("KaiTi",15))
        self.endDateLine.setFont(QFont("KaiTi",15))
        self.ok_btn.setFont(QFont("KaiTi",15,QFont.Bold))
        self.label1.setFont(QFont("KaiTi",16,QFont.Bold))
        self.label2.setFont(QFont("KaiTi",16,QFont.Bold))
        self.label3.setFont(QFont("KaiTi",16,QFont.Bold))
        self.startDateLine.setInputMask('0000-00-00;_')     # 没有输入时, 0显示为_
        self.endDateLine.setInputMask('0000-00-00;_')       # 只能输入0~9

        # 布局
        main_layout = QHBoxLayout()
        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.choose_excle_btn)
        self.VBox.addWidget(self.choose_data_btn)
        self.VBox.addWidget(self.show_btn)

        main_layout.addLayout(self.VBox)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        

        # 点击事件
        self.choose_excle_btn.clicked.connect(self.choose_excle_Click)
        self.choose_data_btn.clicked.connect(self.choose_data_Click)
        self.show_btn.clicked.connect(self.show_Click)
        self.ok_btn.clicked.connect(self.ok_Click)


    # 选择excel
    def choose_excle_Click(self):
        self.senders = self.sender().text()

        curPath=QDir.currentPath()+'/csvFile'    #获取系统当前目录
        title="打开一个文件"    #对话框标题
        filt="CSV文件(*.csv);;excel(*.xlsx *.xls)"   #文件过滤器
        fileName, flt=QFileDialog.getOpenFileName(self,title,curPath,filt)

        if (fileName == ""):
            QMessageBox.critical(self,"错误","打开文件失败")

        else:
            if flt == 'CSV文件(*.csv)':
                self.df = pd.read_csv(fileName, delimiter=',')
            elif flt == 'excel(*.xlsx *.xls)':
                self.df = pd.read_excel(fileName, delimiter=',')
            self.table.setColumnCount(len(self.df.columns))
            self.table.setRowCount(len(self.df.index))
            for i in range(len(self.df.index)):
                for j in range(len(self.df.columns)):
                    self.table.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i,j])))    # 设置标题
        self.table.setHorizontalHeaderLabels(self.df.columns)    # 设置列名


    # 选择数据库
    def choose_data_Click(self):
        self.senders = self.sender().text()
        if len(connUi.user_list)==0:
            cm = connUi.conn_Main()
            cm.show()
        else:
            self.dbui = databaseUi.DatabaseMain()
            self.dbui.show()


    # 添加数据库数据到table
    def database(self):
        # 添加到tabel控件
        self.df = databaseUi.database_data()
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i,j])))    # 设置标题
        self.table.setHorizontalHeaderLabels(self.df.columns)    # 设置列名


    # 展示
    def show_Click(self):
        StockName = []
        try:
            if self.senders == "选择数据库":
                self.database()
                for i in range(len(self.df['名称'])):
                    StockName.append(self.table.item(i,2).text())
            elif self.senders == "选择excel文件":
                for i in range(len(self.df['名称'])):
                    StockName.append(self.table.item(i,1).text())
        except Exception as e:
            print(e)
        
        # 获取股票名称
        self.comboBox.clear()
        self.comboBox.addItems(StockName)

        # 重新布局
        Glayout = QGridLayout()
        Glayout.addWidget(self.label1, 0,1,1,2)
        Glayout.addWidget(self.choose_excle_btn, 1,1,1,2)
        Glayout.addWidget(self.choose_data_btn, 1,4,1,2)
        Glayout.addWidget(self.show_btn, 2,1,1,5)
        Glayout.addWidget(self.frame1, 3,1,1,5)
        Glayout.addWidget(self.label2, 4,1,1,2)
        Glayout.addWidget(self.line_label, 5,1,1,2)
        Glayout.addWidget(self.comboBox, 5,4,1,2)
        Glayout.addWidget(self.start_label, 6,1,1,2)
        Glayout.addWidget(self.startDateLine, 6,4,1,2)
        Glayout.addWidget(self.end_label, 7,1,1,2)
        Glayout.addWidget(self.endDateLine, 7,4,1,2)
        Glayout.addWidget(self.frame2, 8,1,1,5)
        Glayout.addWidget(self.label3, 9,1,1,2)
        Glayout.addWidget(self.ok_btn, 10,1,1,5)
        self.VBox.addLayout(Glayout)
        

    # 获取
    def ok_Click(self):
        start_time = self.startDateLine.text()
        end_time = self.endDateLine.text()

        
        # 获取stock_name对应的股票代码
        stock_name = self.comboBox.currentText()    # 获取股票名称
        stock_line = self.df[(self.df['名称']==stock_name)].index.tolist()  # 获取的是列表
        stock_line = stock_line.pop()
        ticker = str(self.df['代码'][stock_line])

        # 保存
        def draw(filename):
                # 保存
                try:
                    ticker_df.sort_values(by="date",ascending=True,inplace=True)    # data升序排序
                    ticker_df.to_csv(f'CsvFile/Stock_data/{filename}.csv')
                    # 画图
                    draw_df = pd.read_csv(f'CsvFile/Stock_data/{filename}.csv')
                    x = draw_df['date'].tolist()
                    lowest = draw_df['low']
                    close = draw_df['close']
                    open = draw_df['open']
                    highest = draw_df['high']
                    y = [z for z in zip(open, close, lowest, highest)]
                    chart = Kline()
                    chart.add_xaxis(x)
                    chart.add_yaxis(f'{filename}', y)
                    chart.set_global_opts(
                        xaxis_opts=opts.AxisOpts(is_scale=True),
                        # opacity=1, 设置透明度
                        yaxis_opts=opts.AxisOpts(is_scale=True, splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))),
                        datazoom_opts=[opts.DataZoomOpts(type_='inside')],
                        title_opts=opts.TitleOpts(title=f"{filename}K线图")
                    )
                    # 保存
                    chart.render(f'htmlFile/{filename}.html')
                    # 打开html
                    reply = QMessageBox.information(None, '成功', '运行成功', QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        curPath=QDir.currentPath()    #获取系统当前目录
                        url = 'file:///'+ curPath + f'/htmlFile/{filename}.html'
                        webbrowser.open(url)
                except Exception as e:
                    QMessageBox.about(None, '空', '获取到的数据为空')
                    print(e)
                

        # 判断时间是否为空
        if start_time == '--' and end_time == '--':
            ticker_df = ts.get_hist_data(code=ticker)
            #直接保存
            draw(filename=stock_name)
        elif start_time != '--' and end_time == '--':
            ticker_df = ts.get_hist_data(code=ticker, start=start_time)
            #直接保存
            draw(filename=stock_name)
        elif start_time == '--' and end_time != '--':
            QMessageBox(self, '错误', '日期填写错误！')
        elif start_time != '--' and end_time != '--':
            ticker_df = ts.get_hist_data(code=ticker, start=start_time, end=end_time)
            #直接保存
            draw(filename=stock_name)















# if __name__ == "__main__":
#     QImageReader.supportedImageFormats()    # 解决PySide无法显示图片问题
#     app = QApplication(sys.argv)
#     app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))   #加载支持jpg的dll动态链接库
#     app.setWindowIcon(QIcon('images/1.jpg'))
#     m = Main()
#     m.show()
#     sys.exit(app.exec_())