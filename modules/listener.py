"""
@brief
创建一个线程用来录音, 假如录音成功就会设置 new_speech_flag, robot 根据这个 flag 知道需要处理
"""

import os
import time
import threading
import RPi.GPIO as GPIO
import modules.constants as constants
import modules.logging as logging
from modules.config import *

logger = logging.getLogger(__name__)


# 重载线程类
# 按键支持两种功能:
#   长按录音
#   如果超过 10s, 自动停止
class Listener(threading.Thread) :
    
    def run(self):
        
        self.listening = False
        self.previous_time = 0.0
        self.new_speech_flag = False

        while True :
            
            current_time = time.time()
            logger.debug(f"previous_time = {self.previous_time},"
                         f"new_speech_flag = {self.new_speech_flag}")
            
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH and current_time - self.previous_time > 1:

                # 假如有线程正在录音, 应该是发生了错误
                if self.listening == True :
                    logger.error("同时有两个录音线程")
                    exit(0)
                    

                # 如果此时原来的录音还没有被处理, continue 并打印警告
                if self.new_speech_flag == True:
                    logger.warning("录音文件还没有被处理")
                    time.sleep(0.01)
                    continue
                
                # 启动一个线程开始执行
                self._start_record_thread()

                # listener 模块主线程等待按键停止
                cnt = 0
                while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                    cnt += 1
                    time.sleep(0.01)
                    
                    if cnt > 1000: # 最多等待 10s, 然后退出录音
                        break
                
                # 在这里杀死录音进程
                self._stop_record()
            
                
    def _start_record_thread(self) :
        self.thread = threading.Thread(target = self._do_record)
        self.thread.start()
        
    
    def _do_record(self) :

        logger.info("开始录音")
        sp_file_path = os.path.join(constants.INPUT_SPEECH_PATH, "speech_cache.wav")

        # 通过 arecord 实现录音
        os.system(f"touch {sp_file_path}")
        os.system(f"arecord -Dplughw:CARD=Device -fcd -c1 -twav -r8000 -Vmono  {sp_file_path}")

        
    def _stop_record(self) :

        # 录音结束后, 设置两个变量
        self.listening = False
        self.new_speech_flag = True
        self.previous_time = time.time()
        logger.info("结束录音")
        os.system("pkill arecord")

    def IsNewSpeech(self) :
        return self.new_speech_flag == True
            
    def SetSpeechFlag(self):
        self.new_speech_flag = False

if __name__ == "__main__" :

    thread = Listener()
     
    
    


