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

con = conversation.Conversation()
f = face.FaceReco(con)
