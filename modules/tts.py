"""
调用了百度的语音 api
要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
填入 config.ini 中

发送请求在 baiduspeech 里面实现，这里只是检查参数和返回值
"""

from modules.config import *
import modules.logging as logging
import modules.baidu_speech as baidu_speech
import json

logging = logging.getLogger(__name__)

class TTS :

    def __init__(self) :
        self.speech = baidu_speech.BaiduSpeech()

    def GetSpeech(self, msg, fp) :
        """
        msg: 目标文本的字符串
        fp: 存储路径
        return: 是否成功
        """

        result_page = self.speech.TTS(msg)
        tts_result_headers = result_page.headers

        # 如果语音合成失败
        if tts_result_headers['Content-Type'] == 'application/json' :
            tts_result_error_dict = result_page.json()
			
            logging.warning(f"合成错误！错误码为：{tts_result_error_dict['err_no']}")
            return False

        elif tts_result_headers['Content-Type'] == 'audio/mp3' :
			# 获取合成文件的二进制数据
            tts_mp3_data = result_page.content
            with open(fp, 'wb')  as tts_mp3_file :
                tts_mp3_file.write(tts_mp3_data)

			# 合成成功，则返回合成文件的路径
            return True

        else :
            logging.error("tss error!!!")
            return False
