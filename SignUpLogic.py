from enum import auto
import sys
from PyQt5 import QtGui, QtWidgets
from sympy import Si
from TotalUi import *
from DataBase import *
from SignInLogic import*
from PyQt5.QtCore import Qt


class SignUpLogic:
    def __init__(self,Ui):
        self.ui = Ui
        self.db = DataBase() #지역변수
        self.isIdExist = False
        self.ui.signUpBtnList[0].clicked.connect(lambda event: self.idOverLapCheck(event)) #ok
        self.ui.signUpBtnList[1].clicked.connect(lambda event: self.trySignUp(event)) #ok
        self.ui.signUpBtnList[2].clicked.connect(lambda event: self.showSignIn(event)) #ok
        for i in range(0,3):
            self.ui.signUpBtnList[i].enterEvent = lambda event ,index = i : self.btnColorChange1(event, index)
            self.ui.signUpBtnList[i].leaveEvent = lambda event ,index = i : self.btnColorChange2(event, index)
        
    def idOverLapCheck(self,event):
        tempData = self.db.dataRead("user","id",self.ui.signUpLineEditList[0].text())
        if len(tempData) == 0 and self.ui.signUpLineEditList[0].text() != "":
            self.ui.overLapLabel.setText("Enable!")
            self.ui.overLapLabel.setStyleSheet("color: green;")
            self.isIdExist = True
        else :
            self.ui.overLapLabel.setText("disable!")
            self.ui.overLapLabel.setStyleSheet("color: red;")  
            self.isIdExist = False

    def trySignUp(self,event):
        tempList = []
        temp = False
        for i in range(0,6):
             tempList.append(self.ui.signUpLineEditList[i].text())
        for i in range(0,6):
            if len(tempList[i]) == 0:
                temp = True
        if temp == True: #하나라도 비어있으면
            self.blankWarn()
        else:
            if self.isIdExist == False:
                self.overLapWarn()
            else:
                if self.ui.signUpLineEditList[1].text() != self.ui.signUpLineEditList[2].text():
                    self.oddPwWarn()
                else:
                    try: 
                        int(self.ui.signUpLineEditList[4].text())
                        try:
                            int(self.ui.signUpLineEditList[5].text())
                            self.signUpSuccessMessage()
                        except:
                            self.phNumIntWarn()
                    except:
                        self.ageIntWarn()
#텍스트 중복코드임 매개변수로 처리합니다. 
    def blankWarn(self):
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        mb.setText("모든 칸을 채워주세요")
        mb.show()

    def overLapWarn(self):
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setText("아이디 중복확인을 해주세요")
        mb.show()
    
    def oddPwWarn(self):
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setText("비밀번호 2차입력을 확인해주세요")
        mb.show()

    def ageIntWarn(self):
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setText("나이는 숫자만 가능합니다.")
        mb.show()  

    def phNumIntWarn(self):
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setText("전화번호는 숫자만 입력해주세요")
        mb.show()  

    def signUpSuccessMessage(self): 
        mb = QtWidgets.QMessageBox(self.ui.pageList[0])
        mb.setText("가입하신 것을 환영합니다!")
        mb.show()
        self.signUpSequence()
        
    def signUpSequence(self): #데이터 중복체크 후 데이터입력 가능
        lineEditDataList = []
        for i in range(0,6):
            lineEditDataList.append(self.ui.signUpLineEditList[i].text())
        del lineEditDataList[2]

        userColumn = ("id","pw","name","age","phonenumber")
        self.db.dataCreate("user",userColumn,lineEditDataList)

        temp = self.db.dataRead("user","id",lineEditDataList[0])
        winrateColumn = ("usercode","win","draw","lose")
        winrateBasicSet = (temp[0][5],0,0,0)
        self.db.dataCreate("winrate",winrateColumn,winrateBasicSet)
        
        for i in range(0,6):
            self.ui.signUpLineEditList[i].setText("")
        self.ui.overLapLabel.setText("")
        self.showSignIn(auto)
        
    def showSignIn(self,event): #로그인화면에서 로그인 누르면 가위바위보로
        self.ui.stackedWidget.setCurrentIndex(0)
        for i in range(0,3):
            self.ui.signUpBtnList[i].disconnect()
        # del self.overLapFlag
        # del self.db
        # del self.ui
        

    # 버튼 디자인이벤트
    def btnColorChange1(self,event,index):
        styleSheet = self.ui.signUpBtnList[index].styleSheet()
        styleSheet += "border: 2px solid white;"
        self.ui.signUpBtnList[index].setStyleSheet(styleSheet)

    def btnColorChange2(self,event,index):
        styleSheet = self.ui.signUpBtnList[index].styleSheet()
        styleSheet += "border: 2px solid gray;"
        self.ui.signUpBtnList[index].setStyleSheet(styleSheet)