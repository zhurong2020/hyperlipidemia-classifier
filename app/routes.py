from app import app
from flask import render_template, request, make_response
import hashlib

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess():
    # 获取表单数据并进行评估
    # 返回评估结果
    return "Assessment Result" 

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    token = 'Thisismyfirstappinwechat'  # 与微信公众号后台设置的 Token 一致

    if request.method == 'GET':
        # 验证微信服务器
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        # 验证签名
        check_list = [token, timestamp, nonce]
        check_list.sort()
        check_str = ''.join(check_list).encode('utf-8')
        hashcode = hashlib.sha1(check_str).hexdigest()

        if hashcode == signature:
            return make_response(echostr)
        else:
            return make_response('')

    elif request.method == 'POST':
        # 处理微信消息
        # 解析和响应消息
        return make_response('success')