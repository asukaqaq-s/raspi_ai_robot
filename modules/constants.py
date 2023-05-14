import os

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

OUTPUT_SPEECH_PATH = os.path.normpath(
    os.path.join(RESOURCE_PATH, "output")
)

if __name__ == "__main__" :
    print (f"{MODULES_PATH}\n{APP_PATH}\n{RESOURCE_PATH}\n{INPUT_SPEECH_PATH}\n{TEMP_PATH}\n{OUTPUT_SPEECH_PATH}\n")


