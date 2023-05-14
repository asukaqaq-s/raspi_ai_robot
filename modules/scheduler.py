"""
@brief
任务池, 多线程负责调度
"""
import threading
from enum import Enum


class Skill(Enum):
    default = -1
    fan = 0
    light = 1
    clock = 2
    music = 3

class SchdTask:
    
    def __init__(self):
        self.skill = Skill.default
        self.work_time = 0 # 工作的时间
        self.uri = None
        
        
        
        

class Scheduler(threading.Thread):
    
    def __init__(self):
        self.free = 1
        self.task = None

class SchdPool:
    pass