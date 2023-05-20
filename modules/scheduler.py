"""
@brief
任务池, 多线程负责调度
"""
import threading
from enum import Enum
import os
import time
import modules.logging as logging
import modules.constants as constants
import modules.config as config
import RPi.GPIO as GPIO
import modules.player as player
import modules.utils as utils
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


logger = logging.getLogger(__name__)
    


# 播放任务类
class SchdTask :
    
    def __init__(self, date, type, url = None, period = None) :
        self.date = date
        self.type = type
        self.url = url
        self.period = period
        self.task_id = -1   
        self.time = self.date_to_time()

    def date_to_time(self):
        # 先转换为时间数组
        timeArray = time.strptime(self.date, "%Y-%m-%d %H:%M:%S")
 
        # 转换为时间戳
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    
    def add_period_time(self):
        delta = 0
        if self.period != None:
            delta = self.period
        self.time += delta

    
 
    

class Scheduler(threading.Thread) :
    
    def __init__(self, conversation) :
        threading.Thread.__init__(self)
        self.conversation = conversation
        self.player = conversation.player
        self.task_list = []
        self.task_lock = threading.Lock()

    def run(self):
        
        while True:
        
            # 如果是空的, 那么就跳过
            if len(self.task_list) == 0:
                time.sleep(1) # sleep 0.1 second to reduce cost
                continue

            self.task_lock.acquire()
            # 遍历找到一个可以播放的音频
            vic = -1
            index = 0
            for i in self.task_list :
                if i.time <= time.time() :
                    vic = i
                    break
                index += 1
            
            if vic != -1: # 成功找到了一个
                # 此时删除这个音频任务
                self.task_list.pop(index)
                # 执行任务
                self.do_task(vic)

                # 添加一个新任务到队列中
                if vic.period != None:
                    vic.add_period_time()
                    self.task_list.append(vic)

            self.task_lock.release()
            


    # 添加到播放队列
    def Add(self, task) :
        self.task_lock.acquire()
        self.task_list.append(task)
        self.task_lock.release()
        
    
    def AddPeriod(self, task):
        self.task_lock.acquire()
        self.task_list.append(task)
        self.task_lock.release()

    def Delete(self, task_id):
        #self.remove_job(task_id)
        pass



    def do_task(self, task):
        logger.info(f"开始执行 {task.type} task_id = {task.task_id} task_date = {task.date} task_period = {task.period}")
        if task.type == constants.Skill.FAN_ON:
            self.do_fan_on(task)
        if task.type == constants.Skill.FAN_OFF:
            self.do_fan_off(task)
        if task.type == constants.Skill.LIGHT_ON:
            self.do_light_on(task)
        if task.type == constants.Skill.LIGHT_OFF:
            self.do_light_off(task)
        if task.type == constants.Skill.CLOCK:
            self.do_clock(task)
        if task.type == constants.Skill.PHOTO:
            self.do_photo(task)
        if task.type == constants.Skill.MUSIC:
            self.do_music(task)
        if task.type == constants.Skill.VEDIO:
            self.do_vedio(task)

        logger.info(f"结束执行 {task.type} task_id = {task.task_id} task_date = {task.date} task_period = {task.period}")


    def do_fan_on(self, task) :
        GPIO.output(config.FAN_PIN, GPIO.LOW)

    def do_fan_off(self, task) :
        GPIO.output(config.FAN_PIN, GPIO.HIGH)

    def do_light_on(self, task):
        GPIO.output(config.LIGHT_PIN, GPIO.LOW)

    def do_light_off(self, task):
        GPIO.output(config.LIGHT_PIN, GPIO.HIGH)

    def do_clock(self, task):
        point = self.get_time_point(task.date)
        self.player.Add(player.PlayTask(point, url=constants.CLOCK_FILE_PATH_STR))
        
    def do_photo(self):
        utils.get_photo()
        utils.send_email_with_photo(constants.PHOTO_FILE_PATH_STR)
    
    def do_music(self):
        pass

    def do_vedio(self):
        fp = utils.get_vedio()
        utils.send_email_with_vedio(constants.VEDIO_FILE_PATH_STR)    

    def get_time_point(self, date):
        str = date.strftime('%Y-%m-%d %H:%M:%S')
        point = time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S"))
        return point



