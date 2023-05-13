"""
@brief
配置信息
"""

import os
import requests
from configobj import ConfigObj 


def _check_before_init() :

    # check configuration file "config.ini" 
    if os.path.exists("./config.ini") == False :
        # logger
        exit(0)

    # check if network is connected
    net_test = requests.get("http://www.baidu.com")
    if net_test.encoding == None :
        # logger
        exit(0)



_check_before_init()
config_ = ConfigObj('./config.ini', encoding= 'utf-8')


# about listener
BUTTON_PIN = int(config_['pins']['BUTTON_PIN'])            # 中断引脚
NEW_SPEECH_FLAG = False                                    # 判断该录音文件是否未被处理

# about asr and tss
api_id = config_['baidu']['api']['api_id']
api_key = config_['baidu']['api']['api_key']
secret_key = config_['baidu']['api']['secret_key']

# about turing
TURING_KEY = config_['baidu']['api']['TURING_kEY']








