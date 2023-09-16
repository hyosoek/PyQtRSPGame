import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from random import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import time


class TotalUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.signUpFlag = 0
        self.rspGameFlag = 0
        
        self.resize(300, 200)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setStyleSheet("background-color: rgb(178, 226, 255);")
        
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralWidget)
        self.pageList = []
        for i in range(0,3):
            page = QtWidgets.QWidget()
            self.pageList.append(page)
            self.stackedWidget.addWidget(self.pageList[i])
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 301, 191))
        self.stackedWidget.setCurrentIndex(0)
        self.signInUi()
        self.signUpUi()
        self.rspGameUi()
        #위치 옮기거나, 따로 빼고 싶으면 아래의 메인윈도우.show를  UI의 상위항목으로 옮기면 된다.
        self.setCentralWidget(self.centralWidget)
        self.show()

    def signInUi(self):
        self.signInBtnList = []
        for i in range(0,2):
                btn = QtWidgets.QPushButton(self.pageList[0])
                btn.setGeometry(QtCore.QRect(40+10*i,140,100,40))
                btn.setStyleSheet("border: 2px solid gray;\n"
                        "border-radius: 10px;\n"
                        "padding-left : 5px;\n"
                        "background-color : white;")
                self.signInBtnList.append(btn)
                
        self.signInBtnList[0].setText("Sign Up")
        self.signInBtnList[1].setText("Sign In")

        self.signInLineEditList = []
        for i in range(0,2):
                lineEdit = QtWidgets.QLineEdit(self.pageList[0])
                lineEdit.setGeometry(QtCore.QRect(35,20+60*i,240,40))
                lineEdit.setStyleSheet("border: 2px solid gray;\n"
                        "border-radius: 10px;\n"
                        "padding-left : 5px;\n"
                        "background-color : white;")
                self.signInLineEditList.append(lineEdit)
        self.signInLineEditList[1].setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.signInLabelList =[]
        for i in range(0,2):
            label = QtWidgets.QLabel(self.pageList[0])
            label.setGeometry(QtCore.QRect(210, 62+60*i, 60, 16))
            label.setText("")
            label.setStyleSheet("color: red;")
            self.signInLabelList.append(label)

        noneChangedLabelList = []
        for i in range(0,2):
            label = QtWidgets.QLabel(self.pageList[0])
            label.setGeometry(QtCore.QRect(10,35+60*i, 20, 16))
            noneChangedLabelList.append(label)
        noneChangedLabelList[0].setText(" ID")
        noneChangedLabelList[1].setText("PW")


    def signUpUi(self):
        self.signUpBtnList = []
        for i in range(0,3):
            btn = QtWidgets.QPushButton(self.pageList[1])
            btn.setGeometry(QtCore.QRect(195,25+i*60,80,30))
            btn.setStyleSheet("border: 2px solid gray;\n"
                    "border-radius: 10px;\n"
                    "padding-left : 5px;\n"
                    "background-color : white;")
            self.signUpBtnList.append(btn)
        self.signUpBtnList[0].setText("IdCheck")
        self.signUpBtnList[1].setText("SignUp")
        self.signUpBtnList[2].setText("Back")

        lineEditText = ["ID","PW","PWcheck","Name","Age","PhoneNum"]  
        self.signUpLineEditList = []
        for i in range(0,6):
            lineEdit = QtWidgets.QLineEdit(self.pageList[1])
            lineEdit.setGeometry(QtCore.QRect(25, 10+i*31,140,20))
            lineEdit.setStyleSheet("border: 2px solid gray;\n"
                    "border-radius: 10px;\n"
                    "padding-left : 8px;\n"
                    "background-color : white;")
            self.signUpLineEditList.append(lineEdit)
            self.signUpLineEditList[i].setPlaceholderText(lineEditText[i])
        for i in range(0,2):  
            self.signUpLineEditList[i+1].setEchoMode(QtWidgets.QLineEdit.Password)

        self.overLapLabel = QtWidgets.QLabel(self.pageList[1])
        self.overLapLabel.setGeometry(QtCore.QRect(130,31,48,10))
        self.overLapLabel.setText("")
        

    def rspGameUi(self):
        self.rspGameBtnList = []
        self.gameImageList = ("rock.jpeg","scissors.jpeg","paper.png")
        self.userLabelList = []

        for i in range(0,3):
                gameBtn = QtWidgets.QPushButton(self.pageList[2])
                gameBtn.setGeometry(QtCore.QRect(20 + 90 * i,100,80,80))
                gameBtn.setStyleSheet("border: 2px solid gray;\n"
                        "border-radius: 10px;\n"
                        "background-color : white")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(self.gameImageList[i]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                gameBtn.setIcon(icon)
                gameBtn.setIconSize(QtCore.QSize(50, 50))
                self.rspGameBtnList.append(gameBtn)
        
        self.matchBtn = QtWidgets.QPushButton(self.pageList[2])
        self.matchBtn.setGeometry(QtCore.QRect(180,20,60,60))
        self.matchBtn.setStyleSheet("border: 2px solid gray;\n"
                "border-radius: 10px;\n"
                "background-color : white")
        self.rspGameBtnList.append(self.matchBtn)
                
        self.matchLabel = QtWidgets.QLabel(self.pageList[2]) #밖에서 건듦
        self.matchLabel.setGeometry(QtCore.QRect(190, 80, 60, 16))
        self.matchLabel.setText("Match")

        self.rspGameBackBtn = QtWidgets.QPushButton(self.pageList[2]) #밖에서 건듦
        self.rspGameBackBtn.setGeometry(QtCore.QRect(40, 15, 100, 25))
        self.rspGameBackBtn.setStyleSheet("border: 4px solid rgb(220, 220, 220);\n"
                "border-radius: 10px;\n"
                "background-color : rgb(190, 190, 190);")
        self.rspGameBackBtn.setText("Back")

        for index in range(0,4):
            userLabel = QtWidgets.QLabel(self.pageList[2])
            userLabel.setGeometry(QtCore.QRect(70, 40 + 14*index, 100, 12))
            self.userLabelList.append(userLabel)      