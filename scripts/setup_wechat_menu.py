#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
微信公众号自定义菜单设置脚本
使用方法：
1. 获取access_token: https://mp.weixin.qq.com/debug/cgi-bin/apiinfo
2. 运行脚本: python setup_wechat_menu.py <access_token>
"""

import sys
import json
import requests
import os
import sys

# 添加项目根目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.config.settings import ASSESSMENT_URL

def create_menu(access_token):
    """创建微信公众号自定义菜单"""
    url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}"
    
    # 菜单配置
    menu_data = {
        "button": [
            {
                "name": "血脂评估",
                "type": "view",
                "url": ASSESSMENT_URL
            },
            {
                "name": "使用指南",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "评估说明",
                        "key": "ASSESSMENT_GUIDE"
                    },
                    {
                        "type": "click",
                        "name": "指标解读",
                        "key": "INDICATOR_GUIDE"
                    }
                ]
            },
            {
                "name": "联系医生",
                "type": "click",
                "key": "CONTACT_DOCTOR"
            }
        ]
    }
    
    # 发送请求
    response = requests.post(url, json=menu_data)
    result = response.json()
    
    # 输出结果
    if result.get('errcode') == 0:
        print("菜单创建成功！")
    else:
        print(f"菜单创建失败: {result.get('errmsg')}")
    
    return result

def get_menu(access_token):
    """获取当前菜单配置"""
    url = f"https://api.weixin.qq.com/cgi-bin/menu/get?access_token={access_token}"
    
    response = requests.get(url)
    result = response.json()
    
    if 'menu' in result:
        print("当前菜单配置:")
        print(json.dumps(result['menu'], indent=2, ensure_ascii=False))
    else:
        print(f"获取菜单失败: {result.get('errmsg')}")
    
    return result

def delete_menu(access_token):
    """删除当前菜单"""
    url = f"https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={access_token}"
    
    response = requests.get(url)
    result = response.json()
    
    if result.get('errcode') == 0:
        print("菜单删除成功！")
    else:
        print(f"菜单删除失败: {result.get('errmsg')}")
    
    return result

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python setup_wechat_menu.py <access_token> [create|get|delete]")
        print("默认操作为 create")
        return
    
    access_token = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else 'create'
    
    if action == 'create':
        create_menu(access_token)
    elif action == 'get':
        get_menu(access_token)
    elif action == 'delete':
        delete_menu(access_token)
    else:
        print(f"未知操作: {action}")
        print("可用操作: create, get, delete")

if __name__ == "__main__":
    main() 