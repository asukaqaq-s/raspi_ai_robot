import os

APP_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)

TEMP_PATH = os.path.join(APP_PATH, "temp")