"""
@brief
播放音乐、音频的类
"""

import threading
import queue
import os
import time
import modules.logging as logging


logger = logging.getLogger(__name__)

# 播放任务类
class PlayTask :
    
    def __init__(self, play_time, file_path, delay = False) :
        self.play_time = play_time
        self.file_path = file_path
        self.is_delay = delay
        

class Player(threading.Thread) :
    
    def __init__(self) :
        threading.Thread.__init__(self)
        self.play_lock = threading.Lock()
        self.play_queue = [] # 播放队列
        

    def run(self) :

        while True:
            
            # 如果是空的, 那么就跳过
            if len(self.play_queue) == 0:
                time.sleep(0.1) # sleep 0.1 second to reduce cost
                continue

            self.play_lock.acquire()
            
            # 遍历找到一个可以播放的音频
            vic = 0
            index = 0
            for i in self.play_queue :
                if i.is_delay == False or i.play_time <= time.time() :
                    vic = i 
                    break
                index += 1
            
            # 此时删除这个音频任务
            self.play_queue.pop(index)
            self.play_lock.release()
            
            logger.info(f"开始播放 {vic.file_path}")        
            os.system(f"mplayer {vic.file_path}")
            logger.info(f"结束播放")

            # 另一种播放的思路
            # os.system('mpg123 -q -w .s_cache.wav .s_cache.mp3')
            # os.system('aplay -Dplughw:CARD=Device .s_cache.wav')
            
        
    def Add(self, task) :
        self.play_lock.acquire()
        self.play_queue.append(task)
        self.play_lock.release()
        print(len(self.play_queue))


