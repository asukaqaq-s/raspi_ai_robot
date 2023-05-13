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
"""
print(BUTTON_PIN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

thread = listener.Listener()
thread.start()

time.sleep(100)	
"""

"""
player1 = player.Player()
player1.Add(task=player.PlayTask(0, "test1.wav"))
player1.Add(task=player.PlayTask(0, "test.wav"))
player1.run()
"""


# conv.doConverse()

asr1 = asr.ASR()
text = asr1.Transcribe("./tts_cache.wav")
print(text)