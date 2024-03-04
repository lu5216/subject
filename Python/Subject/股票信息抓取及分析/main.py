import os
import sys
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
sys.path.append(".\\")
from Stock import ChooseStock
from UI import connUi, csvUi, CrawlData, databaseUi


class main(QWidget):
    def __init__(self):
        super(main,self).__init__()

        self.setWindowTitle('股票信息挖掘与分析')
        self.resize(600, 400)
        self.move(700, 300)

        self.initUI()

    def initUI(self):
        # 图片
        self.Imglabel = QLabel()
        # 按钮
        self.crawlDataButton = QPushButton(QIcon("images/1.jpg"), '爬取数据')
        self.csvButton = QPushButton('查看CSV')
        self.dataButton = QPushButton('数据库操作')
        self.chooseStockButton = QPushButton('选择股票代码')


        # 样式设计
        self.Imglabel.setAlignment(Qt.AlignCenter)
        self.Imglabel.setScaledContents(True)
        self.Imglabel.setToolTip("股票信息挖掘与分析")
        self.Imglabel.setPixmap(QPixmap("images/index.png"))
        self.crawlDataButton.setFont(QFont("KaiTi",15,QFont.Bold))
        self.csvButton.setFont(QFont("KaiTi",15,QFont.Bold))
        self.dataButton.setFont(QFont("KaiTi",15,QFont.Bold))
        self.chooseStockButton.setFont(QFont("KaiTi",15,QFont.Bold))

        # 布局
        Hbox = QHBoxLayout()    # 水平布局
        Hbox.addWidget(self.csvButton)
        Hbox.addWidget(self.dataButton)
        
        Vbox = QVBoxLayout()    # 垂直布局
        Vbox.addWidget(self.Imglabel)
        Vbox.addWidget(self.crawlDataButton)
        Vbox.addLayout(Hbox)
        Vbox.addWidget(self.chooseStockButton)

        self.setLayout(Vbox)

        # 信号绑定
        self.crawlDataButton.clicked.connect(self.CrawlDataClick)
        self.csvButton.clicked.connect(self.CSVClick)
        self.dataButton.clicked.connect(self.DataClick)
        self.chooseStockButton.clicked.connect(self.ChooseStockClick)


    def CrawlDataClick(self):
        self.cd = CrawlData.Main()
        self.cd.show()


    def CSVClick(self):
        self.csvmain = csvUi.CSVMain()
        self.csvmain.show()


    def DataClick(self):
        if len(connUi.user_list)==0:
            connmain = connUi.conn_Main()
            connmain.show()
        else:
            self.dbui = databaseUi.DatabaseMain()
            self.dbui.show()


    def ChooseStockClick(self):
        self.cs = ChooseStock.Main()
        self.cs.show()
        


if __name__ == "__main__":
    QImageReader.supportedImageFormats()    # 解决PySide无法显示图片问题
    app = QApplication(sys.argv)
    app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))   #加载支持jpg的dll动态链接库
    app.setWindowIcon(QIcon('images/1.jpg'))
    m = main()
    m.show()
    sys.exit(app.exec_())
        

