"""

- 识别技能(命令、聊天)，返回要回复的字符串
- 进行工作
"""

from enum import Enum
import time
import RPi.GPIO as GPIO
import modules.config as config
import re
class Brain :

    def __init__(self, conversation) :
        self.conversation = conversation

    def Query(self, msg) :
        res = False
        reply = ""

        if self.isfan(msg) == True:
            reply = self.dofan(msg)
            res= True
        if self.islight(msg) == True:
            reply = self.dolight(msg)
            res= True
        if self.isclock(msg) == True:
            reply = self.doclock(msg)
            res= True
        if self.isphoto(msg) == True:
            reply = self.dophoto(msg)
            res= True
        if self.ismusic(msg) == True:
            reply = self.domusic(msg)
            res= True
        if self.isvedio(msg) == True:
            res = self.dovedio(msg)
            res= True
        
        return res

    def isfan(self, msg):
        if "风扇" in msg:
            return True        
        return False
    
    def islight(self, msg):
        if "灯" in msg:
            return True
        return False
    
    def isclock(self, msg):
        if "闹钟" in msg:
            return True
        else:
            return False

    def ismusic(self, msg):
        if "音乐" in msg:
            return True
        else:
            return False

    def isstop(self, msg):
        if "暂停" in msg:
            return True
        else:
            return False

    def isstart(self, msg):
        if "播放" in msg:
            return True
        else:
            return False

    def dofan(self, msg):
        
        t = self.get_now()
        delta = None
        type = None
        reply = ""
        
        if self.istime(msg):
            t = self.parse_time(msg)
            delta = self.parse_delta(msg)


        if self.parse_on_off(msg) == 1:
            type = constants.Skill.FAN_ON
            reply = "开风扇设置成功"
        else:
            type = constants.Skill.FAN_OFF
            reply = "关风扇设置成功"

        if delta == None:
            self.createtask(type, t)
        else:
            self.create_delta(type, t, delta)

        return reply

    def dolight(self, msg):
        
        t = self.get_now()
        delta = None
        type = None
        reply = ""
        
        if self.istime(msg):
            t = self.parse_time(msg)
            delta = self.parse_delta(msg)


        if self.parse_on_off(msg) == 1:
            type = constants.Skill.LIGHT_ON
            reply = "开灯设置成功"
        else:
            type = constants.Skill.LIGHT_OFF
            reply = "关灯设置成功"

        if delta == None:
            self.createtask(type, t)
        elif delta != None:
            self.create_delta(type, t, delta)

        return reply

    def dophoto(self, msg):
        
        t = self.get_now()
        delta = None
        type = constants.Skill.PHOTO
        reply = "拍照设置成功"
        
        if self.istime(msg):
            t = self.parse_time(msg)
            delta = self.parse_delta(msg)


        if delta == None:
            self.createtask(type, t)
        else:
            self.create_delta(type, t, delta)

        return reply
    
    def domusic(self, msg):
        
        t = self.get_now()
        delta = None
        type
        url = None
        pattern = re.compile(r'音乐播放(.*?)')
        if "播放" in msg:
            type = constants.Skill.OPEN_MUSIC
            url = re.findall(pattern, msg)   
            url = url + ".mp3"
        else:
            type = constants.Skill.SHUTDOWN_MUSIC
        reply = "音乐设置成功"
        
        if self.istime(msg):
            t = self.parse_time(msg)
            delta = self.parse_delta(msg)


        if delta == None:
            if type is constants.Skill.OPEN_MUSIC:
                self.createtask(type, t, url)
            else:
                self.createtask(type, t)
        else:
            if type is constants.Skill.OPEN_MUSIC:
                self.create_delta(type, t, delta, url)
            else:
                self.create_delta(type, t, delta, None)
        return reply
    
    def dovedio(self, msg):
        
        t = self.get_now()
        delta = None
        type = constants.Skill.VEDIO
        reply = "录像设置成功"
        
        if self.istime(msg):
            t = self.parse_time(msg)
            delta = self.parse_delta(msg)

        if delta == None:
            self.createtask(type, t)
        else:
            self.create_delta(type, t, delta)
        return reply


    # 解析开关指令
    def parse_on_off(self, msg):
        if "开" in msg:
            return 1
        if "关" in msg:
            return 0
        
    # 解析时间
    def parse_time(self, msg):

        str = ""
        parsed_dict = jio.parse_time(msg, time.time())

        if "每" in msg:
            str = parsed_dict['time']['point']['time'][0]
        else :
            str = parsed_dict['time']['point'][0]

        if str == None:
            str = datetime.datetime.now()
            str = str.strftime('%Y-%m-%d %H:%M:%S')
                    

        return str
    
    # 解析一次间隔
    def parse_delta(self, msg):
        parsed_dict = jio.parse_time(msg, time.time())
        
        if 'delta' in parsed_dict.keys():
            return parsed_dict['time']['delta']['day']
        else:
            return None

    def istime(self, msg):
        if "点" in msg or "分钟" in msg or "小时" in msg or "天" in msg or "秒" in msg:
            return True
        return False
    
    def createtask(self, type, date, url = None):
        logger.info(f"创建任务 type={type} date = {date}")
        task = scheduler.SchdTask(date, type)
        self.scheduler.Add(task)

    def create_delta(self, type, date, delta, url = None):
        logger.info(f"创建任务 type={type} date = {date} delta = {delta}")
        task = scheduler.SchdTask(date, type, period=delta*86400000)
        self.scheduler.AddPeriod(task)

    def get_now(self):
        t1 = datetime.datetime.now()
        t1 = t1.strftime('%Y-%m-%d %H:%M:%S')
        return t1

       # print(f"t1 = {t1}")
    