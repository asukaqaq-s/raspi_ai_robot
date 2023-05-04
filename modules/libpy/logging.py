import logging
import os
import constants

from logging.handlers import RotatingFileHandler

PAGE = 4096

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR


def getLogger(name):
    """
    作用同标准模块 logging.getLogger(name)

    :returns: logger
    """
    format = "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - line %(lineno)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format)
    logging.basicConfig(format=format)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # FileHandler
    file_handler = RotatingFileHandler(
        os.path.join(constants.TEMP_PATH, "robot.log"),
        maxBytes=1024 * 1024,
        backupCount=5,
    )
    file_handler.setLevel(level=logging.NOTSET)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

