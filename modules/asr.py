"""
调用了百度的语音识别 api
要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
填入 config.ini 中

为了方便可拓展性, 其实应该有一个基类 abstractASR，其他的 asr 都继承他
但是本项目 is just a toy, 所以没那么复杂

发送请求在 baiduspeech 里面实现，这里只是检查参数和返回值
"""


from modules.config import *
import modules.logging as logging
import modules.baidu_speech as baidu_speech
import json

logging = logging.getLogger(__name__)

class ASR :
    
    def __init__(self) :
        self.speech = baidu_speech.BaiduSpeech()

    def Transcribe(self, file_path) :
        """
        file_path: 文件路径
        return: 语音识别结果, str
        """

        result_page = self.speech.ASR(file_path)
        dict_result = result_page.json()

        err_no = dict_result['err_no']
        if err_no == 0 : # 识别成功
            return "".join(dict_result["result"])
        else :
            logging.warning(f"识别结果错误, 错误码 {err_no}")
            return None

