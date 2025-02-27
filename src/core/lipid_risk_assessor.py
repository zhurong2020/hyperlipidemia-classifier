"""
核心血脂计算逻辑（医生维护版本）
移除所有GUI相关代码，仅保留业务逻辑
"""

class LipidRiskCalculator:
    """血脂风险评估核心计算类"""
    
    def __init__(self):
        self.risk_factors = {
            'diabetes': False,
            'hypertension': False,
            'smoking': False,
            'ckd': False,
            'ascvd': False
        }
    
    def assess_risk(self, params):
        """
        主评估方法
        :param params: 包含以下键的字典
            - ldl_c: 低密度脂蛋白胆固醇 (mmol/L)
            - tc: 总胆固醇 (mmol/L)
            - hdl_c: 高密度脂蛋白胆固醇 (mmol/L)
            - tg: 甘油三酯 (mmol/L)
            - age: 年龄
            - gender: 性别 (male/female)
        :return: (risk_level, target, rec_class, evidence)
        """
        if self.risk_factors['ascvd']:
            return self._secondary_prevention_assessment()
        return self._primary_prevention_assessment(params)
    
    def _primary_prevention_assessment(self, params):
        """一级预防评估逻辑"""
        if params['ldl_c'] >= 4.9 or params['tc'] >= 7.2:
            return ("高危人群", "LDL-C<2.6 mmol/L", "I", "A")
        
        if self.risk_factors['diabetes'] and params['age'] >= 40:
            return ("糖尿病高危人群", "LDL-C<1.8 mmol/L", "I", "A")
        
        return self._calculate_risk_level(params)
    
    def _secondary_prevention_assessment(self):
        """二级预防评估逻辑"""
        if self.risk_factors['diabetes']:
            return ("糖尿病合并ASCVD患者", "LDL-C<1.4 mmol/L", "I", "A")
        return ("极高危人群", "LDL-C<1.8 mmol/L", "I", "A")
    
    def _calculate_risk_level(self, params):
        """详细风险计算逻辑"""
        # 此处实现完整的风险评估算法
        # 示例逻辑：
        risk_score = 0
        if params['age'] > 50:
            risk_score += 1
        if self.risk_factors['smoking']:
            risk_score += 1
        
        if risk_score >= 2:
            return ("中危人群", "LDL-C<2.6 mmol/L", "IIa", "B")
        return ("低危人群", "LDL-C<3.4 mmol/L", "IIb", "C")
    
    def set_risk_factor(self, factor, value):
        """设置风险因素状态"""
        if factor in self.risk_factors:
            self.risk_factors[factor] = value 