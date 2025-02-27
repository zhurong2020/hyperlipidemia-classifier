# 医生本地使用的GUI封装
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.risk_calculator import RiskCalculator

class DoctorGUI:
    """医生使用的桌面应用程序"""
    
    def __init__(self):
        self.calculator = RiskCalculator()
        self.root = tk.Tk()
        self.root.title("血脂风险评估系统")
        self._setup_ui()
    
    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 风险因素选择
        ttk.Label(main_frame, text="风险因素:").grid(column=0, row=0, sticky=tk.W)
        self.diabetes_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="糖尿病", variable=self.diabetes_var).grid(column=0, row=1, sticky=tk.W)
        
        # 输入字段
        ttk.Label(main_frame, text="LDL-C (mmol/L):").grid(column=0, row=2, sticky=tk.W)
        self.ldl_entry = ttk.Entry(main_frame)
        self.ldl_entry.grid(column=1, row=2)
        
        # 评估按钮
        ttk.Button(main_frame, text="评估", command=self.assess).grid(column=0, row=6, columnspan=2)
        
        # 结果展示
        self.result_label = ttk.Label(main_frame, text="")
        self.result_label.grid(column=0, row=7, columnspan=2)
    
    def assess(self):
        try:
            self._update_risk_factors()
            result = self._get_assessment()
            self.result_label.config(text=result)
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def _update_risk_factors(self):
        self.calculator.set_risk_factor('diabetes', self.diabetes_var.get())
    
    def _get_assessment(self):
        ldl_c = float(self.ldl_entry.get())
        return self.calculator.classify_hyperlipidemia(
            ldl_c=ldl_c, tc=0, hdl_c=0, tg=0,  # 示例参数，需补充完整
            ascvd=False, severe_ascvd_events=0, high_risk_factors=0
        )[0]

if __name__ == "__main__":
    app = DoctorGUI()
    app.root.mainloop() 