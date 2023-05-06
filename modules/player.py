"""
播放音乐、音频的类
由于只有一个消费者(录音 listener), 一个生产者 (player), 不需要锁
"""

import threading
import queue
import os


class Player :
    
    def __init__(self) :
        """
        self.playing = False
        self.proc = None
        
        self.complete_queue = []
        self.play_lock = threading.Lock()
        self.play_queue = queue.Queue() # 播放队列
        """

    def doPlay(self) :
        # os.system('mpg123 -q -w ./tts_cache.wav ./tts_cache.mp3')
        # os.system('aplay -Dplughw:CARD=Device ./tts_cache.wav')
        os.system("mplayer ./tts_cache.wav")

if __name__ == "__main__" :
    player = Player()
    player.doPlay()