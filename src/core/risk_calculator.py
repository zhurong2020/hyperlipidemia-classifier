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
    
    def classify_hyperlipidemia(self, ldl_c, tc, hdl_c, tg, ascvd, severe_events, high_risk_factors):
        """
        核心分类逻辑（无GUI依赖）
        参数单位均为mmol/L
        """
        # 先执行原有ASCVD评估
        if self.risk_factors['diabetes']:
            return self._diabetes_classification(ascvd, high_risk_factors)
        
        if ascvd:
            return self._ascvd_classification(severe_events, high_risk_factors)
        
        # 当不满足ASCVD条件时，执行基础分类
        if ldl_c < 3.0 and tc < 5.2 and hdl_c >= 1.0 and tg < 1.7:
            return self._basic_classification(ldl_c, tc, hdl_c, tg)
        
        # 其他情况继续原有逻辑
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
    
    def _basic_classification(self, ldl_c, tc, hdl_c, tg):
        """保留原有基础分类逻辑"""
        if ldl_c >= 4.0:
            return ("高LDL-C", "建议生活方式改变和药物治疗", "IIa", "B")
        elif ldl_c >= 3.0:
            return ("临界高LDL-C", "建议监测和生活方式改变", "IIb", "C")
        
        if tc >= 6.2:
            return ("高总胆固醇", "建议生活方式改变和药物治疗", "IIa", "B")
        elif tc >= 5.2:
            return ("临界高总胆固醇", "建议监测和生活方式改变", "IIb", "C")
        
        if hdl_c < 1.0:
            return ("低HDL-C", "建议生活方式改变", "III", "C")
        
        if tg >= 2.3:
            return ("高甘油三酯", "建议生活方式改变和药物治疗", "IIa", "B")
        elif tg >= 1.7:
            return ("临界高甘油三酯", "建议监测和生活方式改变", "IIb", "C")
        
        return ("正常血脂水平", "保持健康生活方式", "III", "C")
    
    # 其他辅助方法... 