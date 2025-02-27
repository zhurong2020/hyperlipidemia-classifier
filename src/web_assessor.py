from src.lipid_risk_assessor import LipidRiskAssessor

class WebLipidAssessor:
    def __init__(self):
        self.core_assessor = LipidRiskAssessor()

    def assess_risk(self, age, gender, tc, ldl, diabetes, hypertension, smoking):
        # 调用核心逻辑，但跳过 GUI 相关部分
        try:
            # 这里调用核心评估器的相关方法
            risk_level = self.core_assessor.calculate_risk(
                age=age,
                gender=gender,
                tc=tc,
                ldl=ldl,
                diabetes=diabetes,
                hypertension=hypertension,
                smoking=smoking
            )
            return risk_level
        except Exception as e:
            return f"评估错误: {str(e)}"

    def get_recommendations(self, risk_level):
        # 获取建议
        try:
            return self.core_assessor.get_recommendation(risk_level)
        except Exception as e:
            return f"无法获取建议: {str(e)}" 