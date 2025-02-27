from src.lipid_risk_assessor import LipidRiskAssessor

class WebLipidAssessor:
    def __init__(self):
        try:
            self.core_assessor = LipidRiskAssessor()
        except Exception as e:
            print(f"初始化错误: {str(e)}")
            self.core_assessor = None

    def assess_risk(self, age, gender, tc, ldl, diabetes, hypertension, smoking):
        if self.core_assessor is None:
            return "系统初始化错误"
        try:
            return self.core_assessor.calculate_risk(
                age=age,
                gender=gender,
                tc=tc,
                ldl=ldl,
                diabetes=diabetes,
                hypertension=hypertension,
                smoking=smoking
            )
        except Exception as e:
            return f"评估错误: {str(e)}"

    def get_recommendations(self, risk_level):
        if self.core_assessor is None:
            return "系统初始化错误"
        try:
            return self.core_assessor.get_recommendation(risk_level)
        except Exception as e:
            return f"无法获取建议: {str(e)}"