"""
@brief
负责语音交互的功能

- 语音--->文字: 转交给 ASR 
- 文字--->语音: 转交给 TTS
- 与 AI 进行交互
- 通知 Brain 处理技能
"""

import modules.asr as asr
import modules.tts as tts
import modules.ai as ai
import modules.player as player
import modules.logging as logging
import modules.constants as constants
import traceback
import os

logger = logging.getLogger(__name__)

class Conversation:
    
    def __init__(self) :
        self.asr, self.ai, self.tts = None, None, None
        self.player = None
        self.brain = None
        self.tts_index = 0
        self.tts_count = 0
        self.ReInit()

    def ReInit(self) :
        """
        @brief 重新初始化
        """
        try:
            self.asr = asr.ASR()
            self.tts = tts.TTS()
            self.ai = ai.AI()
            self.player = player.Player()
            self.Brain = 0
            self.tts_index = constants.OUTPUT_SPEECH_PATH

            # player start work
            self.player.start()
        except Exception as e:
            logger.critical(f"对话初始化失败: {e}", stack_info=True)
            
    def doConverse(self, fp=constants.SP_FILE_PATH_STR) :
        """
        @brief 通过用户的语音, 知道
        :fp: 音频的地址, 一般都是在固定的地址
        """
        try: 
            query_text = self.asr.Transcribe(fp)
            logger.info(f"识别成功, 内容为 {query_text}")
        except Exception as e:
            logger.critical(f"ASR识别失败：{e}", stack_info=True)
            traceback.print_exc()

        
        try:
            self.doResponse(query_text)
        except Exception as e:
            logger.critical(f"回复失败：{e}", stack_info=True)
            traceback.print_exc()
    
    def doResponse(self, text) :
        """
        @brief 响应两种:
            1. 闲聊发出的问题
            2. 已有的技能

        :text 查询的文本
        """

        # if self.brain ....
        # else : # 闲聊
        msg = self.ai.Ask(text)
        self.doSay(msg)


    def doSay(self, text) :
        """
        @brief 根据 text 说一句话
        """
        logger.info(f"即将朗读语音：{text}")
        print(f"index = {self.tts_index}")
        fp = str(      
             os.path.join(self.tts_index, f"speech_cache{(self.tts_count)}.wav"))
        self.tts_count += 1
        logger.debug(f"tts_count :{self.tts_count}")
        
        # 检查是否成功
        if self.tts.GetSpeech(text, fp) == False:
            exit(0)
        else :
            self.player.Add(self._create_play_task(fp))
            logger.info(f"成功添加 {fp} 到播放队列")

    def _create_play_task(self, fp) :
        return player.PlayTask(0, fp)
        
