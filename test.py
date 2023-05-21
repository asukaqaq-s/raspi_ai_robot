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


