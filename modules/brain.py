"""

- 识别技能(命令、聊天)，返回要回复的字符串
- 进行工作


"""

class Brain :

    def __init__(self) :
        pass

    def IsCommand(self) :
        return False

    def GetAnswer(self, text) :
        
        # just chat
        if self.IsCommand(self) == False :
            return "123456"