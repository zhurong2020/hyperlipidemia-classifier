# 微信公众号处理模块
import time
import hashlib
import xml.etree.ElementTree as ET
from flask import request, make_response
from .assessor import WebAssessor
import logging
from src.config.settings import (
    WECHAT_TOKEN, 
    WECHAT_APP_ID, 
    WECHAT_ENCODING_AES_KEY,
    WECHAT_ENCRYPTION_MODE,
    SERVER_URL,
    ASSESSMENT_URL
)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('wechat_handler')

class WeChatHandler:
    def __init__(self, token=WECHAT_TOKEN, app_id=WECHAT_APP_ID, encoding_aes_key=WECHAT_ENCODING_AES_KEY):
        """
        初始化微信处理器
        :param token: 微信公众号配置的Token
        :param app_id: 微信公众号的AppID
        :param encoding_aes_key: 消息加解密密钥（如果使用加密模式）
        """
        self.token = token
        self.app_id = app_id
        self.encoding_aes_key = encoding_aes_key
        self.assessor = WebAssessor()
    
    def verify_signature(self, signature, timestamp, nonce):
        """验证微信服务器签名"""
        check_list = [self.token, timestamp, nonce]
        check_list.sort()
        check_str = ''.join(check_list).encode('utf-8')
        hashcode = hashlib.sha1(check_str).hexdigest()
        return hashcode == signature
    
    def handle_request(self):
        """处理微信请求"""
        if request.method == 'GET':
            return self.handle_verification()
        elif request.method == 'POST':
            return self.handle_message()
    
    def handle_verification(self):
        """处理微信服务器验证请求"""
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        if self.verify_signature(signature, timestamp, nonce):
            logger.info("WeChat server verification successful")
            return make_response(echostr)
        else:
            logger.warning("WeChat server verification failed")
            return make_response('')
    
    def handle_message(self):
        """处理微信消息"""
        try:
            xml_data = request.data
            logger.info(f"Received WeChat message: {xml_data}")
            
            # 解析XML消息
            msg = self.parse_xml(xml_data)
            if not msg:
                return make_response('success')
            
            # 根据消息类型处理
            msg_type = msg.get('MsgType')
            
            if msg_type == 'text':
                return self.handle_text_message(msg)
            elif msg_type == 'event':
                return self.handle_event_message(msg)
            else:
                # 其他消息类型，返回默认回复
                return self.create_text_response(
                    msg, 
                    "感谢您的消息！请点击菜单使用血脂风险评估功能。"
                )
        except Exception as e:
            logger.error(f"Error handling WeChat message: {str(e)}")
            return make_response('success')
    
    def parse_xml(self, xml_data):
        """解析微信XML消息"""
        try:
            root = ET.fromstring(xml_data)
            msg = {}
            for child in root:
                msg[child.tag] = child.text
            return msg
        except Exception as e:
            logger.error(f"Error parsing XML: {str(e)}")
            return None
    
    def handle_text_message(self, msg):
        """处理文本消息"""
        content = msg.get('Content', '').strip()
        
        # 简单的关键词回复
        if '评估' in content or '血脂' in content:
            return self.create_text_response(
                msg, 
                "请点击菜单中的\"血脂评估\"进行风险评估。"
            )
        elif '帮助' in content or '使用' in content:
            help_text = ("血脂风险评估系统使用指南：\n"
                       "1. 点击菜单中的\"血脂评估\"\n"
                       "2. 填写相关指标数据\n"
                       "3. 获取评估结果和建议\n\n"
                       "如有问题，请回复\"联系医生\"")
            return self.create_text_response(msg, help_text)
        else:
            # 默认回复
            default_text = ("您好！欢迎使用血脂风险评估系统。\n"
                          "请点击下方菜单使用评估功能，或回复\"帮助\"获取使用指南。")
            return self.create_text_response(msg, default_text)
    
    def handle_event_message(self, msg):
        """处理事件消息"""
        event = msg.get('Event')
        
        if event == 'subscribe':
            # 用户关注
            welcome_text = ("感谢关注\"白衣飘飘chen\"！\n\n"
                          "本公众号提供血脂风险评估服务，帮助您了解自身血脂健康状况。\n\n"
                          "使用方法：\n"
                          "1. 点击下方菜单\"血脂评估\"\n"
                          "2. 填写相关指标数据\n"
                          "3. 获取评估结果和建议\n\n"
                          "如有问题，请回复\"联系医生\"")
            return self.create_text_response(msg, welcome_text)
        elif event == 'CLICK':
            # 菜单点击事件
            event_key = msg.get('EventKey')
            if event_key == 'LIPID_ASSESSMENT':
                # 血脂评估菜单
                assessment_text = f"请点击下方链接进行血脂风险评估：\n{ASSESSMENT_URL}"
                return self.create_text_response(msg, assessment_text)
            elif event_key == 'CONTACT_DOCTOR':
                # 联系医生菜单
                contact_text = ("如需咨询，请联系医生：\n"
                              "电话：XXX-XXXX-XXXX\n"
                              "工作时间：周一至周五 9:00-17:00")
                return self.create_text_response(msg, contact_text)
        
        # 默认回复
        return self.create_text_response(
            msg, 
            "感谢您的互动！请点击菜单使用血脂风险评估功能。"
        )
    
    def create_text_response(self, msg, content):
        """创建文本回复消息"""
        xml_template = ("<xml>\n"
                      "<ToUserName><![CDATA[{to_user}]]></ToUserName>\n"
                      "<FromUserName><![CDATA[{from_user}]]></FromUserName>\n"
                      "<CreateTime>{create_time}</CreateTime>\n"
                      "<MsgType><![CDATA[text]]></MsgType>\n"
                      "<Content><![CDATA[{content}]]></Content>\n"
                      "</xml>")
        
        response = xml_template.format(
            to_user=msg.get('FromUserName'),
            from_user=msg.get('ToUserName'),
            create_time=int(time.time()),
            content=content
        )
        return make_response(response)

# 创建默认处理器实例
wechat_handler = WeChatHandler()

def handle_wechat_message():
    """处理微信消息的入口函数"""
    return wechat_handler.handle_request() 