"""
@brief
用来录音
"""

import os
import time
import threading
import RPi.GPIO as GPIO
import libpy.logging as logging
from libpy.config import *


logger = logging.getLogger(__name__)

# 录音
def Listening() :
    global input_flag
    global new_speech_flag
    global previous_time

    input_flag = True
    logger.info("开始录音")
    
    # 通过 arecord 实现录音
    os.system("./arecord -Dplughw:CARD=Device -fcd -c1 -twav -r8000 -Vmono ./tmp/speech_cache.wav")
    
    # 录音结束后, 设置两个变量
    # 将会被 robot 对象识别
    input_flag = False
    new_speech_flag = True
    logger.info("结束录音")
    


# 在录音后, 麦克风的中断处理程序
# 这里会根据两个情况(on or off)，来判断开始录音还是结束录音
def ListenCallBack() :
    global input_flag
    global new_speech_flag
    global previous_time

    current_time = time.time()
    logger.debug(f"回调函数, prev_time = {previous_time}, curr_time = {current_time}")
    
    if current_time - previous_time > 1 : # 1秒内, handler 只反应一次
        previous_time = current_time

        if input_flag == True : # 检测是否正在录音
            logger.info("录音被中止了")
            os.system("pkill arecord")
            input_flag = False
            new_speech_flag= False
        else : # 否则没有在录音, 开启录音工作
            t1 = threading.Thread(target=Listening, args=())
            t1.daemon = False   # 关闭守护线程
            t1.start()      

# 指示灯亮表示正在录音
def SetStateLight() :
    global input_flag
    global input_state_pin

    pin_state = GPIO.input(input_state_pin)
    if pin_state == input_flag :
        pass
    else :
        GPIO.output(input_state_pin, input_flag)

    



