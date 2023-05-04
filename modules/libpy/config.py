"""
@brief
配置信息
"""

import os
import requests
from configobj import ConfigObj 

# about listener
input_pin = 0           # 中断引脚
input_state_pin = 0     # 录音状态引脚
input_flag = False      # 录音状态
new_speech_flag = False # 判断该录音文件是否未被处理
previous_time = 0.0     # 与 curr_time 对应，防止录音事件过多, 发生错误


class Config :
    
    has_init_ = False
    config_ = 0

    def __init__(self) :

        self.ReInit()
        self.has_init = True
    
    def ReInit(self) :
        self._check_before_init()
        self.config_ = ConfigObj('./config.ini', encoding= 'utf-8')
        

        # init informations about listener
        global input_pin
        global input_state_pin
        global input_flag
        global new_speech_flag
        global previous_time
        
        input_pin = int(self.config_['pins']['input_pin'])    
        input_state_pin = int(self.config_['pins']['input_state_pin'])  
        input_flag = False 
        new_speech_flag = False 
        previous_time = 0.0

    
    def _check_before_init(self) :

        # check configuration file "Config.ini" 
        if os.path.exists("./config.ini") == False :
            # logger
            exit(0)

        # check arecord program file
        if os.path.exists("./arecord") == False :
            # logger
            exit(0)

        # check if network is connected
        net_test = requests.get("http://www.baidu.com")
        if net_test.encoding == None :
            # logger
            exit(0)




