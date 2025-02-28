# 医生本地使用的GUI封装
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.risk_calculator import RiskCalculator

class DoctorGUI:
    """完整的医生桌面应用程序"""
    
    def __init__(self):
        self.calculator = RiskCalculator()
        self.root = tk.Tk()
        self._setup_main_window()
    
    def _setup_main_window(self):
        self.root.title("Hyperlipidemia Classifier")
        
        # ASCVD选择框
        self.ascvd_label = tk.Label(self.root, 
            text="是否存在动脉粥样硬化性心血管疾病（ASCVD）（冠心病、脑卒中和外周动脉疾病）:")
        self.ascvd_label.grid(row=0, column=0, columnspan=2, sticky='w')
        
        self.var_ascvd = tk.IntVar(value=-1)
        tk.Radiobutton(self.root, text="是", variable=self.var_ascvd, 
            value=1, command=self.show_secondary_prevention).grid(row=1, column=0, sticky='w')
        tk.Radiobutton(self.root, text="否", variable=self.var_ascvd,
            value=0, command=self.show_primary_prevention).grid(row=1, column=1, sticky='w')
        
        # 结果展示
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(column=0, row=7, columnspan=2)
    
    def show_secondary_prevention(self):
        self._clear_widgets()
        
        # 二级预防标签
        tk.Label(self.root, text="二级预防", font=("Arial", 14)).grid(row=2, column=0, columnspan=2)
        
        # 严重ASCVD事件计数标签（必须存在）
        self.label_severe_events = tk.Label(self.root, text="严重ASCVD事件计数: 0")
        self.label_severe_events.grid(row=3, column=0, columnspan=2)
        
        # 初始化所有事件变量
        self.var_acs = tk.IntVar()
        self.var_mi = tk.IntVar()
        self.var_stroke = tk.IntVar()
        self.var_pad = tk.IntVar()
        
        # 创建事件复选框
        tk.Checkbutton(self.root, text="近期ACS病史（<1年）", 
                      variable=self.var_acs, command=self.update_counts).grid(row=4, column=0, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="既往心肌梗死病史（除上述ACS以外）", 
                      variable=self.var_mi, command=self.update_counts).grid(row=5, column=0, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="缺血性脑卒中史", 
                      variable=self.var_stroke, command=self.update_counts).grid(row=6, column=0, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="有症状的周围血管病变", 
                      variable=self.var_pad, command=self.update_counts).grid(row=7, column=0, columnspan=2, sticky='w')
        
        # 初始化高风险因素变量
        self.var_ldl_c = tk.IntVar()
        self.var_early_chd = tk.IntVar()
        self.var_fh = tk.IntVar()
        self.var_cabg_pci = tk.IntVar()
        self.var_diabetes = tk.IntVar()
        self.var_hypertension = tk.IntVar()
        self.var_ckd = tk.IntVar()
        self.var_smoking = tk.IntVar()
        
        # 高风险因素计数标签
        self.label_high_risk = tk.Label(self.root, text="高风险因素计数: 0")
        self.label_high_risk.grid(row=8, column=0, columnspan=2)
        
        # 创建高风险因素复选框
        self._create_risk_checkbox("LDL-C ≤ 1.8 mmol/L, 再次发生严重的 ASCVD事件", 9, self.var_ldl_c)
        self._create_risk_checkbox("早发冠心病（男<55岁，女<65岁）", 10, self.var_early_chd)
        self._create_risk_checkbox("家族性高胆固醇血症", 11, self.var_fh)
        self._create_risk_checkbox("既往有CABG或PCI史", 12, self.var_cabg_pci)
        self._create_risk_checkbox("糖尿病", 13, self.var_diabetes)
        self._create_risk_checkbox("高血压", 14, self.var_hypertension)
        self._create_risk_checkbox("CKD3-4期", 15, self.var_ckd)
        self._create_risk_checkbox("吸烟", 16, self.var_smoking)
        
        # 提交按钮
        tk.Button(self.root, text="提交", command=self._on_submit).grid(row=17, column=0, columnspan=2)
    
    def show_primary_prevention(self):
        self._clear_widgets()
        
        # 一级预防标签
        tk.Label(self.root, text="一级预防", font=("Arial", 14)).grid(row=2, column=0, columnspan=2)
        
        # 输入字段
        self._create_input_field("总胆固醇 (TC, mmol/L):", 3)
        self._create_input_field("低密度脂蛋白胆固醇 (LDL-C, mmol/L):", 4)
        self._create_input_field("高密度脂蛋白胆固醇 (HDL-C, mmol/L):", 5)
        self._create_input_field("甘油三酯 (TG, mmol/L):", 6)
        self._create_input_field("年龄:", 7)
        
        # 性别选择 - 调整布局
        tk.Label(self.root, text="性别:").grid(row=8, column=0, sticky="w")
        gender_frame = tk.Frame(self.root)
        gender_frame.grid(row=8, column=1, sticky="w")
        
        self.gender_var = tk.StringVar(value="male")
        tk.Radiobutton(gender_frame, text="男性", variable=self.gender_var, 
                      value="male").pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="女性", variable=self.gender_var,
                      value="female").pack(side=tk.LEFT)
        
        # 高危筛查复选框
        tk.Label(self.root, text="高危筛查:", font=("Arial", 12)).grid(row=9, column=0, columnspan=2, sticky="w")
        self.var_diabetes = tk.BooleanVar()
        tk.Checkbutton(self.root, text="糖尿病", variable=self.var_diabetes).grid(row=10, column=0, sticky="w")
        
        self.var_ckd = tk.BooleanVar()
        tk.Checkbutton(self.root, text="CKD 3-4期", variable=self.var_ckd).grid(row=11, column=0, sticky="w")
        
        # 危险因素复选框
        tk.Label(self.root, text="危险因素:", font=("Arial", 12)).grid(row=12, column=0, columnspan=2, sticky="w")
        self.var_smoking = tk.BooleanVar()
        tk.Checkbutton(self.root, text="吸烟", variable=self.var_smoking).grid(row=13, column=0, sticky="w")
        
        self.var_hypertension = tk.BooleanVar()
        tk.Checkbutton(self.root, text="高血压", variable=self.var_hypertension).grid(row=14, column=0, sticky="w")
        
        # 余生危险因素框架
        self.lifetime_risk_frame = tk.Frame(self.root)
        self.lifetime_risk_frame.grid(row=15, column=0, columnspan=2, sticky="w")
        self.lifetime_risk_frame.grid_remove()
        
        # 评估按钮
        self.evaluate_button = tk.Button(self.root, text="评估风险", 
                                        command=self._on_evaluate_primary)
        self.evaluate_button.grid(row=16, column=0, columnspan=2)
    
    def assess(self):
        """主评估方法，根据用户选择调用相应的评估逻辑"""
        try:
            # 根据ASCVD选择调用不同的评估方法
            if self.var_ascvd.get() == 1:
                # 二级预防
                self._on_submit()
            else:
                # 一级预防
                self._on_evaluate_primary()
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def _update_risk_factors(self):
        """更新风险因素 - 不再需要，由具体评估方法处理"""
        pass

    def _get_assessment(self):
        # 检查是否是二级预防
        if self.var_ascvd.get() == 1:
            # 二级预防逻辑
            return self.calculator.classify_hyperlipidemia(
                ldl_c=0,  # 二级预防不需要这些值
                tc=0, 
                hdl_c=0,
                tg=0,
                ascvd=True,
                severe_ascvd_events=self._get_severe_events_count(),
                high_risk_factors=self._get_high_risk_count()
            )[0]
        else:
            # 一级预防逻辑
            try:
                ldl_c = float(self.entry_ldl_c.get())
                tc = float(self.entry_tc.get())
                hdl_c = float(self.entry_hdl_c.get())
                tg = float(self.entry_tg.get())
                
                return self.calculator.classify_hyperlipidemia(
                    ldl_c=ldl_c, 
                    tc=tc,
                    hdl_c=hdl_c,
                    tg=tg,
                    ascvd=False,
                    severe_ascvd_events=0,
                    high_risk_factors=0  # 这里应该计算风险因素
                )[0]
            except ValueError as e:
                messagebox.showerror("输入错误", "请输入有效的数值")
                raise e

    def _create_secondary_prevention_widgets(self):
        # 严重ASCVD事件计数
        self.label_severe_events = tk.Label(self.root, text="严重ASCVD事件计数: 0")
        self.var_acs = tk.IntVar()
        tk.Checkbutton(self.root, text="近期ACS病史", variable=self.var_acs, 
            command=self.update_counts).grid(row=2, column=0)
    
    def update_counts(self):
        """更新所有计数显示"""
        self._update_severe_count()
        self._update_high_risk_count()

    def _get_severe_events_count(self):
        """获取严重ASCVD事件总数"""
        return sum([
            self.var_acs.get(),
            self.var_mi.get(),
            self.var_stroke.get(),
            self.var_pad.get()
        ])

    def _get_high_risk_count(self):
        """获取高风险因素总数"""
        return sum([
            self.var_ldl_c.get(),
            self.var_early_chd.get(),
            self.var_fh.get(),
            self.var_cabg_pci.get(),
            self.var_diabetes.get(),
            self.var_hypertension.get(),
            self.var_ckd.get(),
            self.var_smoking.get()
        ])

    def _clear_widgets(self):
        """清除除主选择框外的所有控件"""
        for widget in self.root.winfo_children():
            # 保留ASCVD选择相关控件
            if widget == self.ascvd_label or \
               isinstance(widget, tk.Radiobutton) and widget.cget("variable") == str(self.var_ascvd):
                continue
            # 销毁其他所有控件
            if isinstance(widget, (tk.Label, tk.Entry, tk.Checkbutton, tk.Button, tk.Frame)) and widget != self.result_label:
                widget.destroy()

    def _update_severe_count(self):
        count = (self.var_acs.get() + self.var_mi.get() + self.var_stroke.get() + 
                self.var_pad.get())
        self.label_severe_events.config(text=f"严重ASCVD事件计数: {count}")

    def _update_high_risk_count(self):
        count = (self.var_ldl_c.get() + self.var_early_chd.get() +
                self.var_fh.get() + self.var_cabg_pci.get() +
                self.var_diabetes.get() + self.var_hypertension.get() +
                self.var_ckd.get() + self.var_smoking.get())
        self.label_high_risk.config(text=f"高风险因素计数: {count}")

    def _on_submit(self):
        try:
            ascvd = self.var_ascvd.get() == 1
            has_diabetes = self.var_diabetes.get()
            
            if ascvd:
                severe_events = self._get_severe_events_count()
                high_risk = self._get_high_risk_count()
                result = self.calculator.classify_hyperlipidemia(
                    ldl_c=0, tc=0, hdl_c=0, tg=0,  # 实际参数需要从界面获取
                    ascvd=True, 
                    severe_events=severe_events,
                    high_risk_factors=high_risk
                )
                
                # 格式化结果显示，与原代码一致
                risk_level, target, rec_class, evidence = result
                
                if has_diabetes:
                    dm_target = "LDL-C<1.4 mmol/L\n非HDL-C<2.2 mmol/L"
                    result_message = (
                        f"ASCVD风险等级：{risk_level}\n"
                        f"治疗目标：{target}\n"
                        f"推荐类别：{rec_class}  证据等级：{evidence}\n\n"
                        f"糖尿病合并ASCVD患者分级：\n"
                        f"治疗目标：{dm_target}\n"
                        f"推荐类别：I  证据等级：A"
                    )
                else:
                    result_message = (
                        f"ASCVD风险等级：{risk_level}\n\n"
                        f"治疗目标：\n\n"
                        f"{target}\n\n"
                        f"推荐类别：{rec_class}  证据等级：{evidence}"
                    )
                
                messagebox.showinfo("风险评估结果及治疗目标", result_message)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _on_evaluate_primary(self):
        """处理一级预防评估逻辑"""
        try:
            # 验证所有必填字段
            missing_fields = []
            invalid_fields = []
            
            # 检查TC字段
            tc_value = self.entry_tc.get()
            if tc_value in ["", "正常范围: 3.1-5.2"] or self.entry_tc.cget("fg") == "gray":
                missing_fields.append("总胆固醇 (TC)")
            else:
                try:
                    tc = float(tc_value)
                except ValueError:
                    invalid_fields.append("总胆固醇 (TC)")
            
            # 检查LDL-C字段
            ldl_c_value = self.entry_ldl_c.get()
            if ldl_c_value in ["", "正常范围: 1.8-3.4"] or self.entry_ldl_c.cget("fg") == "gray":
                missing_fields.append("低密度脂蛋白胆固醇 (LDL-C)")
            else:
                try:
                    ldl_c = float(ldl_c_value)
                except ValueError:
                    invalid_fields.append("低密度脂蛋白胆固醇 (LDL-C)")
            
            # 检查HDL-C字段
            hdl_c_value = self.entry_hdl_c.get()
            if hdl_c_value in ["", "正常范围: >1.0"] or self.entry_hdl_c.cget("fg") == "gray":
                missing_fields.append("高密度脂蛋白胆固醇 (HDL-C)")
            else:
                try:
                    hdl_c = float(hdl_c_value)
                except ValueError:
                    invalid_fields.append("高密度脂蛋白胆固醇 (HDL-C)")
            
            # 检查TG字段
            tg_value = self.entry_tg.get()
            if tg_value in ["", "正常范围: <1.7"] or self.entry_tg.cget("fg") == "gray":
                missing_fields.append("甘油三酯 (TG)")
            else:
                try:
                    tg = float(tg_value)
                except ValueError:
                    invalid_fields.append("甘油三酯 (TG)")
            
            # 检查年龄字段
            age_value = self.entry_age.get()
            if age_value in ["", "例如: 45"] or self.entry_age.cget("fg") == "gray":
                missing_fields.append("年龄")
            else:
                try:
                    age = int(age_value)
                except ValueError:
                    invalid_fields.append("年龄")
            
            # 显示错误信息
            if missing_fields:
                messagebox.showerror("缺少数据", f"请填写以下字段：\n{', '.join(missing_fields)}")
                return
            
            if invalid_fields:
                messagebox.showerror("无效数据", f"以下字段包含无效数值：\n{', '.join(invalid_fields)}\n请输入有效的数字")
                return
            
            # 所有验证通过，继续处理
            tc = float(tc_value)
            ldl_c = float(ldl_c_value)
            hdl_c = float(hdl_c_value)
            tg = float(tg_value)
            age = int(age_value)
            gender = self.gender_var.get()
            has_diabetes = self.var_diabetes.get()
            has_ckd = self.var_ckd.get()
            
            # 第一步：高危筛查
            if (ldl_c >= 4.9 or tc >= 7.2 or 
                (has_diabetes and age >= 40) or 
                has_ckd):
                risk_level = "高危人群"
                target = "LDL-C<2.6 mmol/L"
                rec_class = "I"
                evidence = "A"
                
                # 如果是糖尿病导致的高危
                if has_diabetes and age >= 40:
                    result_message = (
                        f"ASCVD风险等级：{risk_level}\n"
                        f"治疗目标：{target}\n"
                        f"推荐类别：{rec_class}  证据等级：{evidence}\n\n"
                        f"糖尿病患者分级（年龄≥40岁）：\n"
                        f"治疗目标：LDL-C<1.8 mmol/L\n非HDL-C<2.6 mmol/L\n"
                        f"推荐类别：I  证据等级：A"
                    )
                else:
                    result_message = (
                        f"ASCVD风险等级：{risk_level}\n\n"
                        f"治疗目标：\n\n"
                        f"{target}\n\n"
                        f"推荐类别：{rec_class}  证据等级：{evidence}"
                    )
                
                # 隐藏余生风险评估框架（如果显示）
                if hasattr(self, 'lifetime_risk_frame') and self.lifetime_risk_frame.winfo_viewable():
                    self.lifetime_risk_frame.grid_remove()
                
                return messagebox.showinfo("风险评估结果及治疗目标", result_message)

            # 计算危险因素数量
            risk_factors = 0
            if self.var_smoking.get():
                risk_factors += 1
            if hdl_c < 1.0:
                risk_factors += 1
            if (gender == "male" and age >= 45) or (gender == "female" and age >= 55):
                risk_factors += 1

            # 第二步：根据高血压和危险因素评估
            has_hypertension = self.var_hypertension.get()
            
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
            
            # 添加调试信息
            print(f"风险评估信息: 高血压={has_hypertension}, 风险因素数={risk_factors}, TC={tc}, LDL-C={ldl_c}")
            print(f"评估结果: 风险等级={risk_level}")

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

            # 判断是否需要显示余生危险评估
            if risk_level == "中危 (5-9%)" and age < 55:
                if not hasattr(self, 'lifetime_risk_frame') or not self.lifetime_risk_frame.winfo_viewable():
                    # 第一次点击，显示余生危险因素选项
                    self._show_lifetime_risk_factors()
                    return
                else:
                    # 已经显示了余生危险因素，计算结果
                    lifetime_risk_factors = 0
                    if self.var_high_bp.get():
                        lifetime_risk_factors += 1
                    if self.var_high_nonhdl.get():
                        lifetime_risk_factors += 1
                    if self.var_low_hdl.get():
                        lifetime_risk_factors += 1
                    if self.var_high_bmi.get():
                        lifetime_risk_factors += 1
                    if self.var_smoking.get():
                        lifetime_risk_factors += 1

                    if lifetime_risk_factors >= 2:
                        risk_level = "高危人群（基于余生危险评估）"
                        target = "LDL-C<2.6 mmol/L"
                        rec_class = "I"
                        evidence = "A"

            # 显示最终结果
            if has_diabetes:
                result_message = (
                    f"ASCVD风险等级：{risk_level}\n"
                    f"治疗目标：{target}\n"
                    f"推荐类别：{rec_class}  证据等级：{evidence}\n\n"
                    f"糖尿病患者分级（ASCVD风险为中低危）：\n"
                    f"治疗目标：LDL-C<2.6 mmol/L\n非HDL-C<3.4 mmol/L\n"
                    f"推荐类别：II a  证据等级：C"
                )
            else:
                result_message = (
                    f"ASCVD风险等级：{risk_level}\n\n"
                    f"治疗目标：\n\n"
                    f"{target}\n\n"
                    f"推荐类别：{rec_class}  证据等级：{evidence}"
                )
            
            # 隐藏余生风险评估框架（如果显示）
            if hasattr(self, 'lifetime_risk_frame') and self.lifetime_risk_frame.winfo_viewable():
                self.lifetime_risk_frame.grid_remove()
                
            messagebox.showinfo("风险评估结果及治疗目标", result_message)
            
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")

    def _create_input_field(self, label_text, row):
        tk.Label(self.root, text=label_text).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1)
        
        # 设置默认提示文本（灰色显示）
        placeholder = ""
        if "总胆固醇" in label_text:
            placeholder = "正常范围: 3.1-5.2"
            setattr(self, "entry_tc", entry)
        elif "低密度脂蛋白胆固醇" in label_text or "LDL-C" in label_text:
            placeholder = "正常范围: 1.8-3.4"
            setattr(self, "entry_ldl_c", entry)
        elif "高密度脂蛋白胆固醇" in label_text or "HDL-C" in label_text:
            placeholder = "正常范围: >1.0"
            setattr(self, "entry_hdl_c", entry)
        elif "甘油三酯" in label_text or "TG" in label_text:
            placeholder = "正常范围: <1.7"
            setattr(self, "entry_tg", entry)
        elif "年龄" in label_text:
            placeholder = "例如: 45"
            setattr(self, "entry_age", entry)
        else:
            # 从标签文本中提取变量名（作为后备方案）
            var_name = label_text.split()[0].lower()
            if "(" in var_name:
                var_name = var_name.split("(")[0].strip()
            setattr(self, f"entry_{var_name}", entry)
        
        # 添加占位符文本和焦点事件
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg='gray')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

    def _create_checkbox(self, text, row):
        var = tk.BooleanVar()
        tk.Checkbutton(self.root, text=text, variable=var).grid(
            row=row, column=0, sticky="w")
        setattr(self, f"var_{text}", var)

    def _show_lifetime_risk_factors(self):
        """显示余生危险因素评估部分"""
        self.lifetime_risk_frame.grid()
        
        tk.Label(self.lifetime_risk_frame, text="余生危险因素:", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, sticky="w")
        
        # 创建余生风险因素复选框
        self.var_high_bp = tk.BooleanVar()
        tk.Checkbutton(self.lifetime_risk_frame, text="收缩压≥160mmHg或舒张压≥100mmHg", 
                      variable=self.var_high_bp).grid(row=1, column=0, columnspan=2, sticky="w")
        
        self.var_high_nonhdl = tk.BooleanVar()
        tk.Checkbutton(self.lifetime_risk_frame, text="非HDL-C≥5.2 mmol/L", 
                      variable=self.var_high_nonhdl).grid(row=2, column=0, sticky="w")
        
        self.var_low_hdl = tk.BooleanVar()
        tk.Checkbutton(self.lifetime_risk_frame, text="HDL-C<1.0 mmol/L", 
                      variable=self.var_low_hdl).grid(row=3, column=0, sticky="w")
        
        self.var_high_bmi = tk.BooleanVar()
        tk.Checkbutton(self.lifetime_risk_frame, text="BMI≥28 kg/m²", 
                      variable=self.var_high_bmi).grid(row=4, column=0, sticky="w")
        
        # 移动评估按钮到余生危险因素下方
        self.evaluate_button.grid(row=17, column=0, columnspan=2)

    def _create_risk_checkbox(self, text, row, var):
        """创建带计数更新的复选框"""
        tk.Checkbutton(self.root, text=text, variable=var, 
                      command=self.update_counts).grid(row=row, column=0, columnspan=2, sticky='w')

    def _format_result(self, result, has_diabetes):
        """格式化输出结果"""
        risk_level, target, rec_class, evidence = result
        message = f"ASCVD风险等级：{risk_level}\n治疗目标：{target}\n推荐类别：{rec_class}  证据等级：{evidence}"
        
        if has_diabetes:
            if "糖尿病" in risk_level:
                message += "\n\n糖尿病相关建议：\n- 建议定期监测血糖\n- 推荐HbA1c目标<7%"
            else:
                message += "\n\n糖尿病注意事项：\n- 即使风险等级较低仍需控制血糖"
        
        if "高危" in risk_level:
            message += "\n\n建议：\n- 立即开始药物治疗\n- 每3个月复查血脂"
        elif "中危" in risk_level:
            message += "\n\n建议：\n- 生活方式干预\n- 6个月后复查"
        
        return message

    def _calculate_lifetime_risk(self):
        """计算余生危险因素总数"""
        return sum([
            self.var_high_bp.get(),
            self.var_high_nonhdl.get(),
            self.var_low_hdl.get(),
            self.var_high_bmi.get(),
            self.var_smoking.get()
        ])

if __name__ == "__main__":
    app = DoctorGUI()
    app.root.mainloop() 