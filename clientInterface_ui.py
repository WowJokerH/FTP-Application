# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clientInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QSplitter,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTreeView, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.hostname = QLineEdit(self.centralwidget)
        self.hostname.setObjectName(u"hostname")

        self.horizontalLayout.addWidget(self.hostname)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.username = QLineEdit(self.centralwidget)
        self.username.setObjectName(u"username")

        self.horizontalLayout.addWidget(self.username)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout.addWidget(self.password)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.port = QLineEdit(self.centralwidget)
        self.port.setObjectName(u"port")
        self.port.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.port)

        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")

        self.horizontalLayout.addWidget(self.loginButton)

        self.logoutButton = QPushButton(self.centralwidget)
        self.logoutButton.setObjectName(u"logoutButton")

        self.horizontalLayout.addWidget(self.logoutButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.statusWindow = QTableWidget(self.centralwidget)
        self.statusWindow.setObjectName(u"statusWindow")
        self.statusWindow.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout.addWidget(self.statusWindow)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.localPath = QComboBox(self.layoutWidget)
        self.localPath.setObjectName(u"localPath")
        self.localPath.setEditable(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localPath.sizePolicy().hasHeightForWidth())
        self.localPath.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.localPath)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.localdir = QTreeView(self.layoutWidget)
        self.localdir.setObjectName(u"localdir")

        self.verticalLayout_2.addWidget(self.localdir)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.layoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.remotePath = QLineEdit(self.layoutWidget_2)
        self.remotePath.setObjectName(u"remotePath")
        self.remotePath.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.remotePath)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.remoteSplitter = QSplitter(self.layoutWidget_2)
        self.remoteSplitter.setObjectName(u"remoteSplitter")
        self.remoteSplitter.setOrientation(Qt.Vertical)
        self.remoteTree = QTreeWidget(self.remoteSplitter)
        self.remoteTree.setObjectName(u"remoteTree")
        self.remoteTree.setHeaderHidden(True)
        self.remoteSplitter.addWidget(self.remoteTree)
        self.remotedir = QTableWidget(self.remoteSplitter)
        self.remotedir.setObjectName(u"remotedir")
        self.remoteSplitter.addWidget(self.remotedir)

        self.verticalLayout_3.addWidget(self.remoteSplitter)

        self.splitter.addWidget(self.layoutWidget_2)

        self.verticalLayout.addWidget(self.splitter)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(16777215, 150))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.status = QLabel(self.centralwidget)
        self.status.setObjectName(u"status")

        self.horizontalLayout_2.addWidget(self.status)

        self.progressLabel = QLabel(self.centralwidget)
        self.progressLabel.setObjectName(u"progressLabel")

        self.horizontalLayout_2.addWidget(self.progressLabel)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_2.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FTP Client", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u673a(H):", None))
        self.hostname.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d(U):", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801(W):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3(P):", None))
        self.port.setText(QCoreApplication.translate("MainWindow", u"21", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u8fde\u63a5(Q)", None))
        self.logoutButton.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5730\u7ad9\u70b9:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8fdc\u7a0b\u7ad9\u70b9:", None))
        ___qtreewidgetitem = self.remoteTree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Remote Site", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u961f\u5217\u7684\u6587\u4ef6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u4f20\u8f93\u5931\u8d25", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u6210\u529f\u7684\u4f20\u8f93", None))
        self.status.setText(QCoreApplication.translate("MainWindow", u"\u5c31\u7eea", None))
        self.progressLabel.setText("")
    # retranslateUi

