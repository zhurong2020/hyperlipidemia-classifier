from app import app
from flask import render_template, request, make_response
import hashlib
from src.web_assessor import WebLipidAssessor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess():
    data = request.form
    
    # 获取表单数据
    age = int(data.get('age'))
    gender = data.get('gender')
    tc = float(data.get('tc'))
    ldl = float(data.get('ldl'))
    diabetes = bool(data.get('diabetes'))
    hypertension = bool(data.get('hypertension'))
    smoking = bool(data.get('smoking'))

    # 使用 Web 适配器
    assessor = WebLipidAssessor()
    
    # 进行风险评估
    risk_level = assessor.assess_risk(
        age=age,
        gender=gender,
        tc=tc,
        ldl=ldl,
        diabetes=diabetes,
        hypertension=hypertension,
        smoking=smoking
    )
    
    # 获取建议
    recommendations = assessor.get_recommendations(risk_level)

    result = {
        'risk_level': risk_level,
        'recommendations': recommendations
    }

    return render_template('index.html', result=result)

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