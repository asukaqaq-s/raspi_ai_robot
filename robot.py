import os
import time
import modules.listener as listener
import RPi.GPIO as GPIO
import modules.libpy.logging as logging
import modules.asr as asr
import modules.tts as tts

from modules.libpy.config import *


logger = logging.getLogger(__name__)

class Robot :
    
    config_ = 0
    has_init_ = False

    def Init(self) :
        self.config_ = Config()
        self._gpio_init()
        self.has_init_ = True
        
        # 
        self.asr = asr.BaiduASR()

        pass

    def _gpio_init(self) :

        # 设置按钮的 GPIO
        # add_event_detect: sets up an event detection for falling edge events on pin input_pin. 
        # When a falling edge is detected, the function listener.ListenCallBack will be called. 
        # The bouncetime parameter specifies the length of time in milliseconds to ignore subsequent 
        # events after the first event is detected, in order to debounce the input.

        global input_pin
        global input_state_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(input_state_pin, GPIO.OUT)
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=listener.ListenCallBack, bouncetime = 20)

    def Run(self) :
        
        global input_pin
        global input_state_pin

        if self.has_init_ == False :
            logger.warning("你要先初始化robot")
            exit(0)
        
        logger.info("开始执行")
        try :
            self._task()
    
        finally :
            logger.info("退出执行, 回收资源")

            # 删除所有缓存程序
            # expanduser
            for cache_path in ['modules/speech_cache.wav', 'modules/tts_cache.wav', 'modules/tts_cache.mp3'] :
                if os.path.exists(cache_path) :
                    os.remove(cache_path)
            
            # 释放GPIO资源
            GPIO.cleanup(input_pin)
            GPIO.cleanup(input_state_pin)

            # 释放socket

    def _task(self) :
        global new_speech_flag
        global input_flag
        """
        @brief
            如果有新的录音文件, 调用 transformer
            transformer 负责转化语音为文字, 然后让 brain 获取语义
            将序列化后的语义文件返回给 robot, 判断要做命令还是要聊天
            最后如果任务需要生成语音, 先将文字数据反序列化, 传递给 transformer 生成语音
        """

        while True :
            
            # 设置指示灯状态
            # 让 robot 主线程处理亮灯更方便
            listener.SetStateLight(input_flag)

            # 如果新录了一个音
            if new_speech_flag == True :
                # 1. do speechtotext
                
                
                # 2. 语义解析, 是否有命令, 返回要回复的字符串
                
                
                # 3. do texttospeech
                
                
                # 4. 最后播放音频
                
                

            time.sleep(0.05)

        
        

        
        

if __name__ == "__main__" :

    robot = Robot()
    robot.Init()
    robot.Run()

