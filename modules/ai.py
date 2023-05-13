"""
@brief
这里使用了百度的 turing robot, 通过 socket 与百度官网通信
- 传入问题给百度
- 获得响应报文中的字符串, 作为ai答复
"""

import requests
import json
import uuid
from modules.config import *
import modules.logging as logging


logger = logging.getLogger(__name__)


class AI:
    
    def __init__(self) :
        global TURING_KEY
        self.turing_key = TURING_KEY
        self.turing_api_url = "http://openapi.turingapi.com/openapi/api/v2"
        self.my_mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    
    def Ask(self, question) :
        """
        question: str, 要询问的问题
        return: str, ai的回复
        """

        try:
            body = {
                "perception": {"inputText": {"text": question}},
                "userInfo": {"apiKey": self.turing_key, "userId": self.my_mac},
            }

            r = requests.post(self.turing_api_url, json=body)
            reponse = json.loads(r.text) # 响应报文
            result = ""

            # 这里是参考 api 文档, 将 answer 拼接成一个字符串            
            if "results" in reponse:
                for res in reponse["results"]:
                    result += "\n".join(res["values"].values())
            else:
                result = "图灵机器人服务异常"
            
            logger.info(f"turing 回答：{result}")
            return result

        except Exception:

            logger.critical(
                "Tuling robot failed to response for %r", question, exc_info=True
            )
            return "抱歉, 图灵机器人服务回答失败"



        
        
        
    