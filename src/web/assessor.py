# Web服务专用适配器
from src.core.risk_calculator import RiskCalculator

class WebAssessor:
    """Web服务风险评估适配器"""
    
    def __init__(self):
        self.calculator = RiskCalculator()
    
    def assess_risk(self, form_data):
        """处理Web表单数据并执行风险评估"""
        # 解析表单数据
        ascvd = form_data.get('ascvd') == 'true'
        
        if ascvd:
            # 二级预防评估
            return self._assess_secondary_prevention(form_data)
        else:
            # 一级预防评估
            return self._assess_primary_prevention(form_data)
    
    def _assess_secondary_prevention(self, form_data):
        """执行二级预防评估"""
        # 解析严重ASCVD事件
        severe_events = 0
        if form_data.get('acs') == 'true':
            severe_events += 1
        if form_data.get('mi') == 'true':
            severe_events += 1
        if form_data.get('stroke') == 'true':
            severe_events += 1
        if form_data.get('pad') == 'true':
            severe_events += 1
        
        # 解析高风险因素
        high_risk_factors = 0
        if form_data.get('ldl_c_high') == 'true':
            high_risk_factors += 1
        if form_data.get('early_chd') == 'true':
            high_risk_factors += 1
        if form_data.get('fh') == 'true':
            high_risk_factors += 1
        if form_data.get('cabg_pci') == 'true':
            high_risk_factors += 1
        if form_data.get('diabetes') == 'true':
            high_risk_factors += 1
        if form_data.get('hypertension') == 'true':
            high_risk_factors += 1
        if form_data.get('ckd') == 'true':
            high_risk_factors += 1
        if form_data.get('smoking') == 'true':
            high_risk_factors += 1
        
        # 执行评估
        result = self.calculator.classify_hyperlipidemia(
            ldl_c=0, tc=0, hdl_c=0, tg=0,  # 二级预防不需要这些值
            ascvd=True,
            severe_events=severe_events,
            high_risk_factors=high_risk_factors
        )
        
        return result
    
    def _assess_primary_prevention(self, form_data):
        """执行一级预防评估"""
        try:
            # 解析基本生物指标
            tc = float(form_data.get('tc', 0))
            ldl_c = float(form_data.get('ldl', 0))
            hdl_c = float(form_data.get('hdl', 0))
            tg = float(form_data.get('tg', 0))
            age = int(form_data.get('age', 0))
            gender = form_data.get('gender', 'male')
            
            # 解析高危筛查条件
            has_diabetes = form_data.get('diabetes') == 'true'
            has_ckd = form_data.get('ckd') == 'true'
            
            # 解析危险因素
            has_smoking = form_data.get('smoking') == 'true'
            has_hypertension = form_data.get('hypertension') == 'true'
            
            # 计算风险因素数量
            risk_factors = 0
            if has_smoking:
                risk_factors += 1
            if hdl_c < 1.0:
                risk_factors += 1
            if (gender == "male" and age >= 45) or (gender == "female" and age >= 55):
                risk_factors += 1
            
            # 第一步：高危筛查
            if (ldl_c >= 4.9 or tc >= 7.2 or 
                (has_diabetes and age >= 40) or 
                has_ckd):
                risk_level = "高危人群"
                target = "LDL-C<2.6 mmol/L"
                rec_class = "I"
                evidence = "A"
                return (risk_level, target, rec_class, evidence)
            
            # 第二步：根据高血压和危险因素评估
            if not has_hypertension:
                if ((4.1 <= tc < 5.2 or 2.6 <= ldl_c < 3.4) and risk_factors == 3) or \
                   ((5.2 <= tc < 7.2 or 3.4 <= ldl_c < 4.9) and 2 <= risk_factors <= 3):
                    risk_level = "中危 (5-9%)"
                else:
                    risk_level = "低危 (<5%)"
            else:
                if risk_factors == 0:
                    risk_level = "低危 (<5%)"
                elif risk_factors == 1:
                    if 3.1 <= tc < 4.1 or 1.8 <= ldl_c < 2.6:
                        risk_level = "低危 (<5%)"
                    else:
                        risk_level = "中危 (5-9%)"
                elif risk_factors == 2:
                    if 3.1 <= tc < 4.1 or 1.8 <= ldl_c < 2.6:
                        risk_level = "中危 (5-9%)"
                    else:
                        risk_level = "高危 (≥10%)"
                else:  # risk_factors == 3
                    risk_level = "高危 (≥10%)"
            
            # 检查余生危险因素（如果适用）
            if risk_level == "中危 (5-9%)" and age < 55:
                # 解析余生危险因素
                lifetime_risk_factors = 0
                if form_data.get('high_bp') == 'true':
                    lifetime_risk_factors += 1
                if form_data.get('high_nonhdl') == 'true':
                    lifetime_risk_factors += 1
                if form_data.get('low_hdl') == 'true' or hdl_c < 1.0:
                    lifetime_risk_factors += 1
                if form_data.get('high_bmi') == 'true':
                    lifetime_risk_factors += 1
                if has_smoking:
                    lifetime_risk_factors += 1
                
                if lifetime_risk_factors >= 2:
                    risk_level = "高危人群（基于余生危险评估）"
            
            # 设置治疗目标
            if risk_level.startswith("高危"):
                target = "LDL-C<2.6 mmol/L"
                rec_class = "I"
                evidence = "A"
            elif risk_level.startswith("中危"):
                target = "LDL-C<2.6 mmol/L"
                rec_class = "I"
                evidence = "A"
            else:  # 低危
                target = "LDL-C<3.4 mmol/L"
                rec_class = "II a"
                evidence = "B"
            
            return (risk_level, target, rec_class, evidence)
            
        except Exception as e:
            return (f"评估错误: {str(e)}", "", "", "")
    
    def get_recommendations(self, risk_level, has_diabetes=False):
        """根据风险等级和是否有糖尿病生成建议"""
        if "超高危" in risk_level:
            base_rec = "建议使用高强度他汀治疗，必要时联合依折麦布"
        elif "极高危" in risk_level:
            base_rec = "建议使用中高强度他汀治疗，必要时联合依折麦布"
        elif "高危" in risk_level:
            base_rec = "建议使用中强度他汀治疗，必要时联合依折麦布"
        elif "中危" in risk_level:
            base_rec = "建议生活方式干预，必要时考虑他汀治疗"
        else:  # 低危
            base_rec = "建议生活方式干预，定期随访"
        
        # 糖尿病特殊建议
        if has_diabetes:
            if "ASCVD" in risk_level:
                dm_rec = "糖尿病合并ASCVD患者建议LDL-C<1.4 mmol/L，非HDL-C<2.2 mmol/L"
                return f"{base_rec}。{dm_rec}"
            elif "高危" in risk_level:
                dm_rec = "高危糖尿病患者建议LDL-C<1.8 mmol/L，非HDL-C<2.6 mmol/L"
                return f"{base_rec}。{dm_rec}"
            else:
                dm_rec = "糖尿病患者建议LDL-C<2.6 mmol/L，非HDL-C<3.4 mmol/L"
                return f"{base_rec}。{dm_rec}"
        
        return base_rec
    
    def should_show_lifetime_risk(self, form_data):
        """判断是否需要显示余生危险因素评估"""
        try:
            # 解析基本生物指标
            tc = float(form_data.get('tc', 0))
            ldl_c = float(form_data.get('ldl', 0))
            hdl_c = float(form_data.get('hdl', 0))
            age = int(form_data.get('age', 0))
            gender = form_data.get('gender', 'male')
            
            # 解析高危筛查条件
            has_diabetes = form_data.get('diabetes') == 'true'
            has_ckd = form_data.get('ckd') == 'true'
            
            # 高危筛查
            if (ldl_c >= 4.9 or tc >= 7.2 or 
                (has_diabetes and age >= 40) or 
                has_ckd):
                return False
            
            # 解析危险因素
            has_smoking = form_data.get('smoking') == 'true'
            has_hypertension = form_data.get('hypertension') == 'true'
            
            # 计算风险因素数量
            risk_factors = 0
            if has_smoking:
                risk_factors += 1
            if hdl_c < 1.0:
                risk_factors += 1
            if (gender == "male" and age >= 45) or (gender == "female" and age >= 55):
                risk_factors += 1
            
            # 判断风险等级
            is_medium_risk = False
            
            if not has_hypertension:
                if ((4.1 <= tc < 5.2 or 2.6 <= ldl_c < 3.4) and risk_factors == 3) or \
                   ((5.2 <= tc < 7.2 or 3.4 <= ldl_c < 4.9) and 2 <= risk_factors <= 3):
                    is_medium_risk = True
            else:
                if risk_factors == 1:
                    if not (3.1 <= tc < 4.1 or 1.8 <= ldl_c < 2.6):
                        is_medium_risk = True
                elif risk_factors == 2:
                    if 3.1 <= tc < 4.1 or 1.8 <= ldl_c < 2.6:
                        is_medium_risk = True
            
            # 如果是中危且年龄<55，显示余生危险因素评估
            return is_medium_risk and age < 55
            
        except Exception:
            return False 