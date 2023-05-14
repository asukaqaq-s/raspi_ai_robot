"""
@brief
播放音乐、音频的类
"""

import threading
import vlc
import os
import time
import modules.logging as logging


logger = logging.getLogger(__name__)

# 播放任务类
class PlayTask :
    
    def __init__(self, play_time, url, delay = False) :
        self.play_time = play_time
        self.url = url
        self.is_delay = delay
        

class Player(threading.Thread) :
    
    def __init__(self) :
        threading.Thread.__init__(self)
        self.play_lock = threading.Lock()
        self.play_queue = [] # 播放队列
        self.media = vlc.MediaPlayer()
        

    def run(self) :

        while True:
            
            # 如果是空的, 那么就跳过
            if len(self.play_queue) == 0:
                time.sleep(1) # sleep 0.1 second to reduce cost
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
            
            logger.info(f"开始播放 {vic.url}")        
            self.play(vic)
            logger.info(f"结束播放")


    # 添加到播放队列
    def Add(self, task) :
        self.play_lock.acquire()
        self.play_queue.append(task)
        self.play_lock.release()

    # 执行播放
    def play(self, task) :
        self.media.set_mrl(task.url)
        self.media.play()

        # 当前线程等他播放完
        while self.get_state() != -1:
            time.sleep(0.5)

    # 暂停
    def pause(self):
        self.media.pause()

    # 恢复
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        logger.info("当前播放任务被暂停")
        self.media.stop()

    # 返回已播放时间
    def get_time(self) :
        return self.media.get_time()
    
    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.set_time(ms)

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；Ended
    def get_state(self):
        state = self.media.get_state()
        #print(f"{state}")
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        elif state == vlc.State.Ended:
            return -1
        else:
            return -2

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)