import os
import time
import modules.listener as listener
import RPi.GPIO as GPIO
import modules.logging as logging
import modules.conversation as conversation
from modules.config import *

logger = logging.getLogger(__name__)

class Robot :
    
    def __init__(self) :
        self._gpio_init()
        # 初始化 listener
        self.listener = listener.Listener()
        self.listener.start()
        
        # 初始化 conversation
        self.conversation = conversation.Conversation()
        
        
    def _gpio_init(self) :

        # 设置按钮的 GPIO
        global BUTTON_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        

    def Run(self) :
        
        global BUTTON_PIN
        
        logger.info("开始执行")
        self.conversation.doSay("机器人开始执行")
        
        try :
            self._task()
    
        finally :

            logger.info("退出执行, 回收资源")
            self.conversation.doSay("机器人退出执行")
            
            # 删除所有缓存程序
            for cache_path in ['resources/input/', 'resources/ouput/', 'resources/tmp/'] :
                if os.path.exists(cache_path) :
                    tmp_path = os.path.join(os.path, cache_path)
                    os.system(f"rm -rf {tmp_path}")
            
            # 释放GPIO资源
            GPIO.cleanup(BUTTON_PIN)

            # 释放socket
            pass

    def _task(self) :
        
        while True:        

            if self.listener.IsNewSpeech() == True:
                self.conversation.doConverse()
                self.listener.SetSpeechFlag()

        

if __name__ == "__main__" :

    robot = Robot()
    robot.Run()



