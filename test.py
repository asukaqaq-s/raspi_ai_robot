"""
record 5s voice

prepare:
    sudo apt-get install portaudio19-dev
    pip install pyaudio
"""

import pyaudio
import wave
import os
import sys
import RPi.GPIO as GPIO
import time
import modules.player as player
import modules.conversation as conversation
import modules.brain as brain
#import jionlp
import modules.utils as utils

# res = jio.parse_time('100天之后', time.time())
# print(res)


# res = jio.parse_time('每天8点开灯', time.time())
# print(res)


# res = jio.parse_time('每周五下午4点', time.time())
# print(res)



# -*- coding: utf-8 -*-

import itchat
import sqlite3
import os
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
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

# 创建主界面类
class Ui_Menu(QWidget):
    def __init__(self):
        super(Ui_Menu, self).__init__()
        # 创建label并设置文本内容
        self.label = QLabel('ai robot ', self)
        # 创建普通用户和管理员按键
        self.btn_ordinary = QPushButton('进入音乐模式', self)
        self.btn_admin = QPushButton('进入语音模式', self)

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        # 设置窗口大小
        self.resize(400, 400)
        # 设置label框的位置
        self.label.move(200, 200)
        
        # 设置按键框的位置和大小
        self.btn_ordinary.setGeometry(200, 250, 100, 50)
        self.btn_admin.setGeometry(200, 350, 100, 50)
        
        # 设置label样式（字体、大小、颜色等）
        self.label.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:14px;font-weight:bold;"  # 大小为70 加粗
            "font-family:Roman times;}")  # Roman times字体

        self.btn_ordinary.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:10px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        self.btn_admin.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:10px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 点击管理员按钮事件
        self.btn_admin.clicked.connect(self.slot_btn_admin)
        # 点击普通用户按钮事件
        self.btn_ordinary.clicked.connect(self.slot_btn_ordinary)

    # 点点击管理员按钮事件
    def slot_btn_admin(self):
        #self.logon = Ui_logon()
        #self.logon.show()
        #self.hide()
        pass

    # 点击普通用户按钮事件
    def slot_btn_ordinary(self):
        #self.face_reco = Ui_face_reco()
        #self.face_reco.show()
        #self.hide()
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_Menu()
    w.show()
    sys.exit(app.exec_())