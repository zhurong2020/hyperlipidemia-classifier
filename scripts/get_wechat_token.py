#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
获取微信公众号访问令牌(access_token)脚本
使用方法：
python3 get_wechat_token.py <appid> <appsecret>
"""

import sys
import requests
import json

def get_access_token(appid, secret):
    """获取微信公众号访问令牌"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if 'access_token' in result:
            print(f"获取access_token成功！")
            print(f"Access Token: {result['access_token']}")
            print(f"有效期: {result['expires_in']}秒 (约{result['expires_in']/60/60:.1f}小时)")
            print("\n使用此token设置菜单的命令:")
            print(f"python3 scripts/setup_wechat_menu.py {result['access_token']}")
            return result['access_token']
        else:
            print(f"获取access_token失败: {result.get('errmsg')}")
            return None
    except Exception as e:
        print(f"请求出错: {str(e)}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("使用方法: python3 get_wechat_token.py <appid> <appsecret>")
        return
    
    appid = sys.argv[1]
    secret = sys.argv[2]
    
    get_access_token(appid, secret)

if __name__ == "__main__":
    main() 