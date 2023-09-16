import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from TotalUi import*
from DataBase import *
from SignUpLogic import*
from RspGameLogic import*

class SignInLogic:
    def __init__(self):
        self.ui = TotalUi()
        self.db = DataBase()
        for i in range(0,2):
            self.ui.signInBtnList[i].enterEvent = lambda event ,index = i : self.btnColorChange1(event, index)
            self.ui.signInBtnList[i].leaveEvent = lambda event ,index = i : self.btnColorChange2(event, index)
        self.ui.signInBtnList[0].clicked.connect(lambda event: self.showSignUp(event))
        self.ui.signInBtnList[1].clicked.connect(lambda event: self.signInSeq(event))
    
    def signInSeq(self,event):
        lineEditDataArr = []
        blankTest = False
        for i in range(0,2):
            lineEditDataArr.append(self.ui.signInLineEditList[i].text()) #2개 밖에 안되서 아래 빈칸체크 if에서 조건으로 달아줌
            if self.ui.signInLineEditList[i].text() == "":
                blankTest = True
        if blankTest == True:
            mb = QtWidgets.QMessageBox(self.ui.pageList[0])
            mb.setText("정보를 입력해주세요")
            mb.show()
        else:
            userdata = self.db.dataRead("user","id",lineEditDataArr[0])
            if len(userdata) > 0: #아이디 존재 확인
                if str(userdata[0][1]) == str(lineEditDataArr[1]):#비번 확인
                    for i in range(0,2):
                            self.ui.signInLineEditList[i].setText("")
                            self.ui.signInLabelList[i].setText("")
                    self.showRspGame(userdata[0][5])
                    
                else:
                    self.ui.signInLabelList[0].setText("")
                    self.ui.signInLabelList[1].setText("wrong!")
            else:
                self.ui.signInLabelList[1].setText("")
                self.ui.signInLabelList[0].setText("wrong!")

    def showRspGame(self,usercode): #가위바위보, 회원가입에서에서 빽 누르면 로그인으로
        self.ui.stackedWidget.setCurrentIndex(2)
        rspGameLogic = RspGameLogic(self.ui,usercode)
        
    def showSignUp(self,event):
        self.ui.stackedWidget.setCurrentIndex(1)
        signUpLogic = SignUpLogic(self.ui)
    

    #버튼 디자인이벤트
    def btnColorChange1(self,event,index):
        styleSheet = self.ui.signInBtnList[index].styleSheet()
        styleSheet += "border: 2px solid white;"
        self.ui.signInBtnList[index].setStyleSheet(styleSheet)

    def btnColorChange2(self,event,index):
        styleSheet = self.ui.signInBtnList[index].styleSheet()
        styleSheet += "border: 2px solid gray;"
        self.ui.signInBtnList[index].setStyleSheet(styleSheet)