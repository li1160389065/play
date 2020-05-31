# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 475)
        MainWindow.setStyleSheet("*{\n"
"font-size:24px;\n"
"font-family:Century Gothic;\n"
"}\n"
"QWidget{\n"
"\n"
"border-radius:15px;\n"
# "background-image:url(./pictures/time.jpg);\n"
"}\n"
"\n"
"QToolButton{\n"
"background:red;\n"
"border-radius:60px;\n"
"}\n"
"QLabel{\n"
"color:black;\n"
"background:transparent;\n"
"}\n"
"QPushButton{\n"
"background:white;\n"
"border-radius:15px;\n"
"}\n"
"QPushButton:hover{\n"
"background:#333;\n"
"border-radius:15px;\n"
"background:#49ebff;\n"
"}\n"
"QLineEdit{\n"
"background:transparent;\n"
"border:none;\n"
"color:#717072;\n"
"border-bottom:1px solid #717072;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 70, 241, 311))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_6.setText("")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.pushButton_2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "员工注册"))
        self.label.setText(_translate("MainWindow", "注册"))
        self.label_6.setText(_translate("MainWindow", "密码："))
        self.label_3.setText(_translate("MainWindow", "姓名："))
        self.label_2.setText(_translate("MainWindow", "性别："))
        self.label_5.setText(_translate("MainWindow", "年龄"))
        self.label_4.setText(_translate("MainWindow", "账号："))
        self.label_7.setText(_translate("MainWindow", "手机号："))
        self.pushButton.setText(_translate("MainWindow", "注册"))
        self.pushButton_2.setText(_translate("MainWindow", "返回"))
