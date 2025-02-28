import requests
import json

# 定义请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-3ffe211cd19b4010a4f1e57c768a0220"
}

# 定义请求体 - 为代码开发设置temperature=0.0
body = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful coding assistant. Provide concise and efficient code solutions."
        },
        {
            "role": "user",
            "content": "Write a simple Python function to check if a number is prime."
        }
    ],
    "temperature": 0.0,  # 推荐用于代码开发的温度值
    "max_tokens": 500    # 限制输出token数量以减少费用
}

try:
    # 发送API请求
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30  # 添加超时设置
    )
    
    # 检查响应状态
    response.raise_for_status()
    
    # 打印响应
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 如果成功，提取并打印回答内容
    if "choices" in result and len(result["choices"]) > 0:
        answer = result["choices"][0]["message"]["content"]
        print("\n回答内容:")
        print(answer)
    
except requests.exceptions.HTTPError as e:
    error_msg = "HTTP错误:"
    if response.status_code == 402:
        error_msg = "账户余额不足。请前往DeepSeek网站充值。"
    elif response.status_code == 429:
        error_msg = "请求频率过高。请稍后再试。"
    print(f"{error_msg} {e}")
    if hasattr(response, 'text'):
        print(f"错误详情: {response.text}")
        
except Exception as e:
    print(f"请求出错: {e}")