# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqtgraph.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(525, 40, 101, 192))
        self.listWidget.setObjectName("bandwidths")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 10, 83, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.graphicsView = QtWidgets.QWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 40, 501, 391))
        self.graphicsView.setObjectName("graphicsView")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(530, 240, 91, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(530, 280, 91, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(410, 10, 111, 25))
        self.comboBox.setObjectName("comboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 637, 22))
        self.menubar.setObjectName("menubar")
        self.menuEEG_Filters = QtWidgets.QMenu(self.menubar)
        self.menuEEG_Filters.setObjectName("menuEEG_Filters")
        self.menufilter = QtWidgets.QMenu(self.menubar)
        self.menufilter.setObjectName("menufilter")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuEEG_Filters.menuAction())
        self.menubar.addAction(self.menufilter.menuAction())

        self.retranslateUi(MainWindow)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EEG-Filters"))
        self.pushButton.setText(_translate("MainWindow", "open file"))
        self.pushButton_2.setText(_translate("MainWindow", "filter"))
        self.menuEEG_Filters.setTitle(_translate("MainWindow", "EEG-Filters"))
        self.menufilter.setTitle(_translate("MainWindow", "filter"))
