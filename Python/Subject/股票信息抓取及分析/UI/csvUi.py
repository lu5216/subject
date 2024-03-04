import os
import sys
import pandas as pd
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class CSVMain(QWidget):
    def __init__(self):
        super(CSVMain,self).__init__()
        self.resize(1480, 800)

        self.initUI()
        self.update_data()
    

    def initUI(self):
        # 读取到的csv文件
        self.table = QTableWidget()

        # 自适应宽
        self.table.resizeColumnsToContents()
        # 隔行变色设置
        self.table.setAlternatingRowColors(True)
        # 不可编辑
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 自适应窗口大小
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.table)

        self.setLayout(Vlayout)


    def update_data(self):
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
        self.setWindowTitle(f'{fileName}（只读）')           # 设置title
        self.table.setHorizontalHeaderLabels(self.df.columns)    # 设置列名





# if __name__ == "__main__":
#     QImageReader.supportedImageFormats()
#     app = QApplication(sys.argv)
#     app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
#     app.setWindowIcon(QIcon('images/1.jpg'))
#     m = CSVMain()
#     m.show()
#     sys.exit(app.exec_())