"""

"""

import os
import json
import requests
import uuid
import base64
from modules import logging
from modules.config import *

logging = logging.getLogger(__name__)

class BaiduSpeech(object) :
    
    def __init__(self) :
        super(self.__class__, self).__init__()

        # 语音识别的 api 地址
        self.asr_api_url = "http://vop.baidu.com/server_api"
        # 语音合成的 api 地址
        self.tts_api_url = "http://tsn.baidu.com/text2audio"
        # 获取 access token
        self.access_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.my_mac = uuid.UUID(int = uuid.getnode()).hex[-12:]

        # api 访问的表单数据
        global api_key
        global secret_key

        self.api_key, self.secret_key = api_key, secret_key
        self.access_token = self.FetchToken()

        self.cnt = 0
        

        
    def FetchToken(self) :
        try :
            body = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key,
            }

            access_page = requests.post(
                self.access_url,
                headers={"Content-Type": "application/json; charset=UTF-8"}, 
                data = body,
            )
            access_dict = access_page.json()
            access_token = access_dict["access_token"]

            return access_token
        except :
            logging.error("获取 access token 异常")
            exit(0)

    def ASR(self, file_path): 
        """
        file_path: 录音文件的本地地址
        return: 返回识别结果, page 
        """
        # 以二进制形式打开音频文件, which stored by .wav
        with open(file_path, "rb") as speech_file :
            speech_data = speech_file.read()

        # sent over a network connection or stored in a file
        # by converting it to a UTF-8 formatted string, we can easily manipulate and transmit the data.
        speech_data_length = len(speech_data)
        speech_b64_data = base64.b64encode(speech_data).decode('utf-8')
        dict_data = {
            'format' : 'wav',
            'rate' : 8000, # 采样率
            'channel' : 1,
            'cuid' : self.my_mac,
            'token' : self.access_token,
            'lan' : 'zh', # language
            'speech' : speech_b64_data,
            'len' : speech_data_length
        }

        json_data = json.dumps(dict_data).encode('utf-8')
        json_data_length = len(json_data)

        # request header
        post_headers = {
            'Content-Type' : 'application/json',
            'Content-length' : str(json_data_length)
        }

        logging.info("正在发送录音数据到网络")
        
        try :
            result_page = requests.post(
                self.asr_api_url, 
                headers=post_headers, 
                data=json_data,timeout=3
            )
        
        except requests.exceptions.Timeout :
            logging.error("数据 post 超时")
            return None

        logging.info("数据发送成功")
        return result_page


    def TTS(self, target_text) :
        """
        target_text: 要转化的字符串
        return: 返回合成结果 page
        """

        if target_text == None:
            return None
        
        logging.info("开始语音合成")
        # 构造请求表单
        tts_form = {
            'tex' : target_text ,
            'lan' : 'zh' ,  #语言选择
            'tok' : self.access_token,
            'ctp' : 1 , #客户端类型选择
            'cuid' : self.my_mac ,
            #以下为选填的项目
            'spq' : 3 , #语速
            'pit' : 4 , #语调
            'vol' : 5 , #音量
            'per' : 0   #发音人选择,0~4
		}

        # 发送请求给 baidu_tts
        try :
            tts_result_page = requests.post(self.tts_api_url, data=tts_form, timeout=2)
        except requests.exceptions.Timeout :
            logging.error("语音合成 post 超时")
            return None
        
        return tts_result_page



if __name__ == "__main__" :
    speech = BaiduSpeech() 

    