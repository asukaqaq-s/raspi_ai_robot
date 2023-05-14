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

GPIO.setmode(GPIO.BCM)
LIGHT_PIN = 18
FAN_PIN = 21
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

conv = conversation.Conversation()
b = brain.Brain(conv)

GPIO.output(FAN_PIN, GPIO.LOW)
time.sleep(2)
b.Query("关风扇")


try:
    while True:
        pass
finally:
    GPIO.cleanup(LIGHT_PIN)
    GPIO.cleanup(FAN_PIN)