from app import app
from flask import render_template, request, make_response
import hashlib
from src.web.assessor import WebAssessor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess():
    try:
        data = request.form
        assessor = WebAssessor()
        risk_level = assessor.assess_risk(data)
        recommendations = assessor.get_recommendations(risk_level[0])
        
        return render_template('index.html', result={
            'risk_level': risk_level[0],
            'target': risk_level[1],
            'recommendations': recommendations
        })
    except Exception as e:
        return str(e), 400

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