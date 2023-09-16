import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from random import *
import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from DataBase import *
from TotalUi import *
from SignInLogic import *

class RspGameLogic(QObject,threading.Thread):
    imageSignal = pyqtSignal()
    labelSignal = pyqtSignal(int)
    userDataSignal = pyqtSignal()

    def __init__(self,Ui,usercode):
        super().__init__()
        self.ui = Ui
        self.usercode = usercode #현재게임중인 유저의 코드
        self.state = None #가위바위보 상태를 저장해줄 상태
        self.holdingFlag = False #게임버튼 누르면 잠시 멈추게 해줄 상태
        self.finishFlag = False #쓰레딩 종료를 위한 상태
        self.db = DataBase()

        self.ui.rspGameBackBtn.clicked.connect(lambda event: self.showSignIn(event))
        self.ui.rspGameBackBtn.enterEvent = lambda event : self.btnColorChange1(event)
        self.ui.rspGameBackBtn.leaveEvent = lambda event : self.btnColorChange2(event)
        for i in range(0,3):
            self.ui.rspGameBtnList[i].clicked.connect(lambda event, index = i: self.rspGameSequence(event,index))
        self.imageSignal.connect(self.updateGui)
        self.labelSignal.connect(self.updateMatch)
        self.userDataSignal.connect(self.userDataLabelShow)
        self.start()

#시그널 발생 함수
    def renewMatchImage(self):
        self.imageSignal.emit()
    
    def renewMatchLabel(self,whichBtn):
        self.labelSignal.emit(whichBtn)

    def renewUserLabel(self):
        self.userDataSignal.emit()


    def run(self):
        self.renewUserLabel()
        while True:
            if self.holdingFlag == False:
                self.renewMatchImage()
                time.sleep(0.1)
            elif self.holdingFlag == True:
                self.renewMatchLabel(self.state)
                self.renewUserLabel()
                time.sleep(2)
                self.holdingFlag = False
            if self.finishFlag == True:
                break
            
    def rspGameSequence(self,event,whichBtn):
        self.state = whichBtn
        self.holdingFlag = True

    def updateGui(self):
        self.enemyState = randint(0,2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.ui.gameImageList[self.enemyState]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.matchBtn.setIcon(icon)
        self.ui.matchBtn.setIconSize(QtCore.QSize(50, 50))

    def userDataLabelShow(self):
        winRateData = self.db.dataRead("winrate","usercode",self.usercode)
        userData = self.db.dataRead("user","usercode",self.usercode)
        self.ui.userLabelList[0].setText(userData[0][0] + " 님")
        labelList = ("win : ","draw : ","lose : ")
        for i in range(0,3):
            self.ui.userLabelList[i+1].setText(labelList[i]+str(winRateData[0][i+1]))
        
    def updateMatch(self,whichBtn):
        self.updateGui()
        matchState = self.enemyState 
        if matchState == 0:
            if whichBtn == 0:
                self.whenDraw()
            elif whichBtn == 1:
                self.whenLose()
            elif whichBtn == 2:
                self.whenWin()
        elif matchState == 1:
            if whichBtn == 0:
                self.whenWin()
            elif whichBtn == 1:
                self.whenDraw()
            elif whichBtn == 2:
                self.whenLose()
        elif matchState == 2:
            if whichBtn == 0:
                self.whenLose()
            elif whichBtn == 1:
                self.whenWin()
            elif whichBtn == 2:
                self.whenDraw()

    def whenWin(self):
        self.ui.matchLabel.setText("Win!")
        tempdata = self.db.dataRead("winrate","usercode",self.usercode)
        winData = tempdata[0][1] + 1
        self.db.dataUpdate("winrate","win",winData,self.usercode)

    def whenDraw(self):
        self.ui.matchLabel.setText("Draw~")
        tempdata = self.db.dataRead("winrate","usercode",self.usercode)
        drawData = tempdata[0][2] + 1
        self.db.dataUpdate("winrate","draw",drawData,self.usercode)

    def whenLose(self):
        self.ui.matchLabel.setText("Lose..")
        tempdata = self.db.dataRead("winrate","usercode",self.usercode)
        loseDate = tempdata[0][3] + 1
        self.db.dataUpdate("winrate","lose",loseDate,self.usercode)

    def showSignIn(self,event): #가위바위보, 회원가입에서에서 빽 누르면 로그인으로
        self.ui.stackedWidget.setCurrentIndex(0)
        self.finishFlag = True #쓰레드 정지
        self.ui.rspGameBackBtn.disconnect()
        for i in range(0,3):
            self.ui.rspGameBtnList[i].disconnect()
        self.imageSignal.disconnect()
        self.labelSignal.disconnect()
        self.userDataSignal.disconnect()
        # del self.finishFlag
        # del self.db
        # del self.enemyState
        # del self.finishFlag
        # del self.holdingFlag
        # del self.imageSignal
        # del self.labelSignal
        # del self.name
        # del self.state
        # del self.ui
        # del self.usercode
        # del self.userDataSignal
        # del self.staticMetaObject
        

    #버튼 디자인이벤트
    def btnColorChange1(self,event):
        styleSheet = self.ui.rspGameBackBtn.styleSheet()
        styleSheet += "border: 2px solid rgb(220, 220, 220);"
        self.ui.rspGameBackBtn.setStyleSheet(styleSheet)

    def btnColorChange2(self,event):
        styleSheet = self.ui.rspGameBackBtn.styleSheet()
        styleSheet += "border: 2px solid gray;"
        self.ui.rspGameBackBtn.setStyleSheet(styleSheet)