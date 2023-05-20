"""
@brief
负责人脸识别的类, 调用了百度云人脸识别 api
可以直接使用 aip 库进行访问
"""

import modules.logging as logging
import base64
import time
import modules.conversation as conversation
import modules.constants as constants
from picamera import PiCamera
from aip import AipFace
from modules.config import *

logger = logging.getLogger(__name__)

class FaceReco :
    
    def __init__(self, conversation) :
        global face_api_id
        global face_api_key
        global face_secret_key

        self.conversation = conversation
        self.camera = PiCamera()
        # 创建一个客户端用以访问百度云
        self.client = AipFace(face_api_id, face_api_key, face_secret_key) 
        # 用户组
        self.group = 'raspberry_pi'
        # 图像编码方式
        self.image_type = 'BASE64'

    
    def Recognize(self):
        """
        return true if the master in photo
        """
        # 1. 拍照
        self.get_image()
        
        # 2. 转化为 base64
        img = self.transimage()

        # 3. 和百度云 post, 检测是否成功
        
        # 在百度云人脸库中寻找有没有匹配的人脸, 需要手动设置人脸库
        result = self.client.search(str(img, 'utf-8'), self.image_type, self.group)

        # 成功
        if result['error_msg'] == 'SUCCESS':
            # 获取名字
            name = result['result']['user_list'][0]['user_id']
            # 获取相似度
            score = result['result']['user_list'][0]['score']
        
            logger.info(f"人脸识别成功, 是 {name}, 相似度 {score}")
            if score > 80:
                if name == "asukaqaq":
                    return True
            else:
                # 成功, 但是不认识这个人
                name = 'Unknow'
                logger.info(f"对不起, 不认识这个人")
                return False
        
        # 如果发生了错误
        if result['error_msg'] == 'pic not has face':
            logger.info("摄像头不清楚")
            time.sleep(2)
            return False
        else:
            logger.info(f"其他原因, {result['error_msg']}")
            time.sleep(2)
            return False


    # 拍张照
    def get_image(self):
        # 摄像界面为 1024*768
        self.camera.resolution = (1024, 768)
        # 设置图像视频的饱和度
        self.camera.saturation = 80 
        # 设置帧率
        self.camera.framerate = 32

        # 打开摄像头
        time.sleep(0.1)#让相机预热
        self.camera.start_preview()
        logger.info("开始摄像, 并倒计时")
        
        # 从3倒序到1
        for i in ["三", "二", "一"]:
            self.conversation.doSay(i)
            time.sleep(1)

        # 拍照并保存
        self.camera.capture(constants.IM_FILE_PATH_STR)
        time.sleep(1)

    # 将照片格式转化为 base64
    def transimage(self):
        f = open(constants.IM_FILE_PATH_STR,'rb')
        img = base64.b64encode(f.read())
        return img

    def close(self):
        self.camera.close()

