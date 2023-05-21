"""
@brief
一些用到的函数, 主要是用在 phase 3,4 里面
"""

from picamera import PiCamera
import modules.logging as logging
import time
import os
import modules.constants as constants
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import vlc
logger = logging.getLogger(__name__)
take_photo_cnt = 0
take_vedio_cnt = 0

# def open_music(path):
# 拍张照
def get_photo():
    camera = PiCamera()
    global take_photo_cnt
    # 摄像界面为 1024*768
    camera.resolution = (1024, 768)
    # 设置图像视频的饱和度
    camera.saturation = 80 
    # 设置帧率
    camera.framerate = 32

    # 打开摄像头
    time.sleep(0.1)#让相机预热
    camera.start_preview()
    
    # 拍照并保存
    # take_photo_cnt += 1
    fp = os.path.join(constants.TEMP_PATH, f"photo.jpg")

    camera.capture(fp)
    time.sleep(1)
    camera.close()
    return fp


# 拍个视频
def get_vedio():
    camera = PiCamera()

    global take_vedio_cnt    
    # 摄像界面为 1024*768
    camera.resolution = (1024, 768)
    # 设置图像视频的饱和度
    camera.saturation = 80 
    # 设置帧率
    camera.framerate = 32

    # 打开摄像头
    time.sleep(0.1)#让相机预热
    camera.start_preview()


    #录制的视频存放位置
    # take_vedio_cnt += 1
    fp = os.path.join(constants.TEMP_PATH, f"vedio.h264")

    #开始录制
    camera.start_recording(fp)
    #录制时间 单位秒
    time.sleep(10)
    #停止录制
    camera.stop_recording()

    camera.close()
    return fp



def send_email_with_photo(fp):
    # 账号密码，密码来自于 smtp 服务的授权码
    sender = '15105197821@163.com'
    receivers = '1311722138@qq.com'
    password= 'MIBQJCDOAIMFSCUR'
    
    # 创建一个 multipart 类型，多组合类型，包含文本和附件
    # related 内嵌资源：图片、声音
    message =  MIMEMultipart('related')

    # 写入内容    
    subject = "你好，这是您设置的拍照请求~~来自 airobot"
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers

    # 写入 HTML 数据，有一个 img tag，
    # src="cid:imageid" 表示显示这个 image，引用这个图片
    # alt 表示当图片无法生成时的替代文本
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
    message.attach(content)

    # 写入 jpg 数据
    file=open(fp, "rb")
    img_data = file.read()
    file.close()

    # img 写到文件，add_header 用于添加这个 img
    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    message.attach(img)

    try:
        server=smtplib.SMTP("smtp.163.com", 25 ) #SMTP开启的邮箱和端口
        server.login(sender,password)
        server.sendmail(sender,receivers,message.as_string())
        server.quit()
        print ("邮件发送成功！")
    except smtplib.SMTPException:
        print('邮件发送失败！')



def send_email_with_vedio(fp):
    # 账号密码，密码来自于 smtp 服务的授权码
    sender = '15105197821@163.com'
    receivers = '1311722138@qq.com'
    password= 'MIBQJCDOAIMFSCUR'
    
    # 创建一个 multipart 类型，多组合类型，包含文本和附件
    # related 内嵌资源：图片、声音
    message =  MIMEMultipart('related')

    # 写入内容    
    subject = "你好，这是您设置的录像请求~~来自 airobot"
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers

    # 写入 HTML 数据附带一个附件
    content = MIMEText('<html><body>视频附件</body></html>','html','utf-8')
    message.attach(content)

    # 附件写入
    vf = MIMEApplication(open(fp, 'rb').read())
    vf.add_header('Content-Disposition','attachment',filename=fp)
    message.attach(vf)

    try:
        server=smtplib.SMTP("smtp.163.com", 25 ) #SMTP开启的邮箱和端口
        server.login(sender,password)
        server.sendmail(sender,receivers,message.as_string())
        server.quit()
        print ("邮件发送成功！")
    except smtplib.SMTPException:
        print('邮件发送失败！')