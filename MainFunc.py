import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from random import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from SignInLogic import *
from RspGameLogic import *
from TotalUi import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signIn = SignInLogic()
    sys.exit(app.exec_())



    