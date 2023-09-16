from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import time

import py

class Example(QObject): #totalLogic의 역할인가?
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.gui = Window() #totalUi 부분
        self.worker = Worker() #rspGameLogic 부분

        self.worker_thread = QThread()  #rspGameThread 부분
        self.worker.moveToThread(self.worker_thread) #쓰레드 지정
        self.worker_thread.start() #쓰레드 함수 시작

        self._connectSignals() #버튼연동
        self.gui.show() #totalUi 부분

    def _connectSignals(self):
        self.gui.button_start.clicked.connect(self.worker.startWork)
        self.worker.sig_numbers.connect(self.gui.updateStatus)
        #self.gui.button_start.disconnect()
        # self.gui.button_cancel.clicked.connect(self.forceWorkerReset)

    # def forceWorkerReset(self):
    #     if self.worker_thread.isRunning(): 
    #         self.worker_thread.terminate()  
    #         self.worker_thread.wait()       
    #         self.worker_thread.start()
            
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.button_start = QPushButton('Start', self)
        self.button_cancel = QPushButton('Cancel', self)
        self.label_status = QLabel('status!!', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_cancel)
        layout.addWidget(self.label_status)
        self.setFixedSize(400, 200)
        #여기까진 의미 없음

#연동 부분
    @pyqtSlot(int)
    def updateStatus(self, status):
        self.label_status.setText(str(status))
        print(status)
#여기까지

class Worker(QObject):
    sig_numbers = pyqtSignal(int)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @pyqtSlot()  
    def startWork(self):
        _cnt = 0
        while True:
            _cnt += 1
            self.sig_numbers.emit(_cnt)                
            time.sleep(0.1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Example(app)
    sys.exit(app.exec_())

