import os
from enum import Enum


MODULES_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

APP_PATH = os.path.normpath(
    os.path.join(MODULES_PATH, os.pardir)
)

RESOURCE_PATH = os.path.join(APP_PATH, "resources")


INPUT_SPEECH_PATH = os.path.normpath(
    os.path.join(RESOURCE_PATH, "input")
)

SP_FILE_PATH_STR = os.path.join(INPUT_SPEECH_PATH, "speech_cache.wav")

TEMP_PATH = os.path.normpath(
    os.path.join(RESOURCE_PATH, "tmp")
)

IM_FILE_PATH_STR = os.path.join(TEMP_PATH, "face.jpg")

PHOTO_FILE_PATH_STR = os.path.join(TEMP_PATH, "photo.jpg")

VEDIO_FILE_PATH_STR = os.path.join(TEMP_PATH, "vedio.h264")

CLOCK_FILE_PATH_STR = os.path.join(TEMP_PATH, "园游会-周杰伦.96.mp3")


OUTPUT_SPEECH_PATH = os.path.normpath(
    os.path.join(RESOURCE_PATH, "output")
)

if __name__ == "__main__" :
    print (f"{MODULES_PATH}\n{APP_PATH}\n{RESOURCE_PATH}\n{INPUT_SPEECH_PATH}\n{TEMP_PATH}\n{OUTPUT_SPEECH_PATH}\n")


class Dest(Enum) :
    TO_BOX = 0
    TO_WECHAT = 1



class Skill(Enum):
    DEFAULT = -1
    FAN_ON = 0
    FAN_OFF = 1
    LIGHT_ON = 2
    LIGHT_OFF = 3
    CLOCK = 4
    PHOTO = 5
    MUSIC = 6
    VEDIO = 7


    
    