import os
import modules.baidu_speech as baidu_speech
import modules.constants as constants
import modules.listener as listener
import modules.player as player
import modules.tts as tts
from modules.config import *
import modules.ai as Ai
import RPi.GPIO as GPIO
import time
import modules.conversation as conversation
import modules.asr as asr
import base64
from picamera import PiCamera
from aip import AipFace
import modules.face as face
import modules.scheduler as scheduler
import modules.brain as brain
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#import jionlp as jio
#from datetime import datetime


# coding=utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import modules.utils as utils

utils.send_email_with_photo(constants.PHOTO_FILE_PATH_STR)
utils.send_email_with_vedio(constants.VEDIO_FILE_PATH_STR)