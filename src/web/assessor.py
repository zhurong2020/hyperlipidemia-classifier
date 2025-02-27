# Web服务专用适配器
from core.risk_calculator import RiskCalculator

class WebAssessor:
    """Web服务风险评估适配器"""
    
    def __init__(self):
        self.calculator = RiskCalculator()
    
    def assess_risk(self, form_data):
        """处理Web表单数据"""
        self._parse_form_data(form_data)
        return self._perform_assessment()
    
    def _parse_form_data(self, data):
        self.calculator.set_risk_factor('diabetes', data.get('diabetes') == 'true')
        # 解析其他参数...
    
    def _perform_assessment(self):
        return self.calculator.classify_hyperlipidemia(
            ldl_c=3.5, tc=5.0, hdl_c=1.2, tg=1.8,  # 示例参数
            ascvd=False, severe_ascvd_events=0, high_risk_factors=2
        )
    
    def get_recommendations(self, risk_level):
        recommendation_map = {
            "糖尿病合并ASCVD患者": "建议使用高强度他汀治疗...",
            "ASCVD风险为高危的糖尿病患者": "建议LDL-C目标值<1.8 mmol/L...",
            # 其他建议...
        }
        return recommendation_map.get(risk_level, "请咨询专科医生") 