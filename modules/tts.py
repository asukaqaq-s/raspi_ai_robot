"""
调用了百度的语音 api
要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
填入 config.ini 中

发送请求在 baiduspeech 里面实现，这里只是检查参数和返回值
"""

from libpy.config import *
import libpy.logging as logging
import baidu_speech
import json

logger = logging.getLogger(__name__)

class BaiduTSS :

    def __init__(self) :
        self.speech = baidu_speech.BaiduSpeech()

    def GetSpeech(self, target_text) :
        """
        target_text: 目标文本的字符串
        return: 存储路径
        """

        result_page = self.speech.TTS(target_text)
        tts_result_headers = result_page.headers

        # 如果语音合成失败
        if tts_result_headers['Content-Type'] == 'application/json' :
            tts_result_error_dict = result_page.json()
			
            logger.warning(f"合成错误！错误码为：{tts_result_error_dict['err_no']}")
            return None

        elif tts_result_headers['Content-Type'] == 'audio/mp3' :
			# 获取合成文件的二进制数据
            tts_mp3_data = result_page.content
            with open('./tts_cache.mp3', 'wb')  as tts_mp3_file :
                tts_mp3_file.write(tts_mp3_data)

			# 合成成功，则返回合成文件的路径
            return './tts_cache.mp3'

        else :
            logger.error("tss error!!!")
            exit(0)
