# 医生维护的核心算法（示例）
class RiskCalculator:
    """核心血脂风险评估计算器"""
    
    def __init__(self):
        self.risk_factors = {
            'diabetes': False,
            'hypertension': False,
            'smoking': False,
            'ckd': False
        }
    
    def classify_hyperlipidemia(self, ldl_c, tc, hdl_c, tg, ascvd, severe_ascvd_events, high_risk_factors):
        """
        核心分类逻辑（无GUI依赖）
        参数单位均为mmol/L
        """
        if self.risk_factors['diabetes']:
            return self._diabetes_classification(ascvd, high_risk_factors)
        
        if ascvd:
            return self._ascvd_classification(severe_ascvd_events, high_risk_factors)
        
        return self._primary_prevention_classification(ldl_c, tc, hdl_c, high_risk_factors)
    
    def _diabetes_classification(self, ascvd, high_risk_factors):
        if ascvd:
            return ("糖尿病合并ASCVD患者", "LDL-C<1.4 mmol/L", "I", "A")
        elif high_risk_factors >= 2:
            return ("ASCVD风险为高危的糖尿病患者", "LDL-C<1.8 mmol/L", "I", "A")
        else:
            return ("ASCVD风险为中低危的糖尿病患者", "LDL-C<2.6 mmol/L", "II a", "C")
    
    def _ascvd_classification(self, severe_events, high_risk_factors):
        if severe_events >= 2 or (severe_events == 1 and high_risk_factors >= 2):
            return ("超高危人群", "LDL-C<1.4 mmol/L，且较基线降低幅度>50%", "I", "A")
        return ("极高危人群", "LDL-C<1.8 mmol/L，且较基线降低幅度>50%", "I", "A")
    
    def _primary_prevention_classification(self, ldl_c, tc, hdl_c, high_risk_factors):
        if ldl_c >= 4.9 or tc >= 7.2 or (hdl_c < 1.0 and high_risk_factors >= 2):
            return ("高危人群", "LDL-C<2.6 mmol/L", "I", "A")
        return ("需要进一步评估", "LDL-C<3.4 mmol/L", "II a", "B")
    
    def set_risk_factor(self, factor, value):
        """设置风险因素状态"""
        if factor in self.risk_factors:
            self.risk_factors[factor] = value
    
    # 其他辅助方法... 