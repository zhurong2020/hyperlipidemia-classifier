from app import app
from flask import render_template, request, make_response, jsonify
import hashlib
from src.web.assessor import WebAssessor
from src.web.wechat_handler import handle_wechat_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess():
    try:
        data = request.form
        assessor = WebAssessor()
        
        # 执行风险评估
        risk_level, target, rec_class, evidence = assessor.assess_risk(data)
        
        # 获取是否有糖尿病
        has_diabetes = data.get('diabetes') == 'true'
        
        # 获取建议
        recommendations = assessor.get_recommendations(risk_level, has_diabetes)
        
        return render_template('index.html', result={
            'risk_level': risk_level,
            'target': target,
            'rec_class': rec_class,
            'evidence': evidence,
            'recommendations': recommendations
        })
    except Exception as e:
        return str(e), 400

@app.route('/check_lifetime_risk', methods=['POST'])
def check_lifetime_risk():
    """检查是否需要显示余生风险因素评估"""
    try:
        data = request.form
        assessor = WebAssessor()
        show_lifetime_risk = assessor.should_show_lifetime_risk(data)
        
        return jsonify({
            'show_lifetime_risk': show_lifetime_risk
        })
    except Exception as e:
        return jsonify({
            'show_lifetime_risk': False,
            'error': str(e)
        })

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    """微信公众号接口"""
    # 使用新的微信处理器
    return handle_wechat_message()