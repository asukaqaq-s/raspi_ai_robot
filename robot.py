import os
import time
import sys
import modules.listener as listener
import RPi.GPIO as GPIO
import modules.logging as logging
import modules.conversation as conversation
import modules.constants as constants
from modules.config import *
import modules.face as face
import modules.ui as ui
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QLabel

logger = logging.getLogger(__name__)



class Robot :
    
    def __init__(self) :
        # 状态
        self.state = constants.RobotState.DEFAULT

        # ui 类, 目前用来表示机器人状态
        self.ui = ui.UI(self)
        self.ui.start()

        # 初始化 GPIO
        self._gpio_init()
        # 初始化 listener
        self.listener = listener.Listener(self)
        self.listener.start()
        
        # 初始化 conversation
        self.conversation = conversation.Conversation()

        # 初始化 face
        self.face = face.FaceReco(self.conversation)

        
    
    
        
        
    def _gpio_init(self) :

        # 设置按钮的 GPIO
        global BUTTON_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # 设置灯的 GPIO
        global LIGHT_PIN
        GPIO.setup(LIGHT_PIN, GPIO.OUT)

        # 设置风扇的 GPIO
        global FAN_PIN
        GPIO.setup(FAN_PIN, GPIO.OUT)

        # 初始化
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
        GPIO.output(FAN_PIN, GPIO.HIGH)
        

    def Run(self) :

        # 首先进行登录请求
        try:
            self.state = constants.RobotState.LOGINING
            self.login()
        finally:
            self.face.close()
        
        self.face.close()
        global BUTTON_PIN
        
        logger.info("开始执行")
        self.conversation.doSay("机器人开始执行")
        
        try :
            self._task()
    
        finally :

            logger.info("退出执行, 回收资源")
            self.conversation.doSay("机器人退出执行")
            
            # 删除所有缓存程序
            for cache_path in ['resources/input/', 'resources/ouput/'] :
                if os.path.exists(cache_path) :
                    tmp_path = os.path.join(os.path, cache_path)
                    os.system(f"rm -rf {tmp_path}")
            
            # 释放GPIO资源
            GPIO.cleanup(BUTTON_PIN)
            GPIO.cleanup(FAN_PIN)
            GPIO.cleanup(LIGHT_PIN)
            
            
            # 释放socket

            # 释放 ui
            #sys.exit(app.exec_())
            sys.exit()
            pass

    def _task(self) :
        
        while True:        
            
            if self.listener.IsListening() == False:
                self.state = constants.RobotState.FREE

            if self.listener.IsNewSpeech() == True:
                self.state = constants.RobotState.EXECUTING
                self.conversation.doConverse()
                self.listener.SetSpeechFlag()


    def login(self) :
        """
        @brief 通过人脸识别检测是否为主任
        """
        logger.info("开始进入登录界面")
        self.conversation.doSay("欢迎使用, 在此之前你需要先登录")
        success = False    
    
        while True:
            
            if self.face.Recognize() == True:
                success = True
                self.conversation.doSay("人脸核验通过, 欢迎使用！")
            else :
                self.conversation.doSay("人脸核验不通过, 请再试一次")
                
            if success == True:
                break
    
    def get_state(self):
        return self.state
        
        

if __name__ == "__main__" :
    robot = Robot()
    robot.Run()



