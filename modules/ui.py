import sys
import threading
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QGroupBox
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PIL import Image
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import RPi.GPIO as GPIO
import modules.constants as constants
import modules.logging as logging
import time


logger = logging.getLogger(__name__)


class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    def __init__(self, robot):
        QObject.__init__(self)
        self.robot = robot

    # 处理业务逻辑
    def run(self):
        while True:
            # 刷新机器人状态
            
            show_str = "出错！！！"

            if self.robot.get_state() == constants.RobotState.DEFAULT:
                show_str = "初始化..."
            elif self.robot.get_state() == constants.RobotState.LOGINING:
                show_str = "登陆中..."
            elif self.robot.get_state() == constants.RobotState.FREE:
                show_str = "空闲~"
            elif self.robot.get_state() == constants.RobotState.RECORDING:
                show_str = "录音中..."
            elif self.robot.get_state() == constants.RobotState.EXECUTING:
                show_str = "执行任务~"

            #logger.info(f"ui  {show_str} 线程正在执行！！！！！！！！！")
            
            self.update_date.emit(show_str)
            time.sleep(1)
            


class Window(QDialog):
    def __init__(self, robot):
        QDialog.__init__(self)
        self.setWindowTitle('ai robot')
        self.resize(400, 100)
        self.input = QLabel(self)
        self.input.resize(400, 100)
        self.robot = robot
        self.initUI()
        

    def initUI(self):
        # 创建线程
        self.thread = QThread()

        self.backend = BackendThread(self.robot)
        # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
        self.backend.moveToThread(self.thread)

        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        logger.info(f"当前数据 {data}")
        self.input.setText(data)


# UI 子线程, 防止阻塞主线程
class UI(threading.Thread):

    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        app = QApplication(sys.argv)
        win = Window(self.robot)
        win.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())




