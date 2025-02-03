import tkinter as tk
from tkinter import messagebox

def classify_hyperlipidemia(ldl_c, tc, hdl_c, tg, ascvd, severe_ascvd_events, high_risk_factors):
    """
    Classify hyperlipidemia level based on provided parameters.
    """
    # 获取糖尿病状态
    has_diabetes = var_diabetes.get() if 'var_diabetes' in globals() else False
    
    # 糖尿病患者的血脂目标判断
    if has_diabetes:
        if ascvd:
            return "糖尿病合并ASCVD患者", "LDL-C<1.4 mmol/L", "I", "A"
        elif high_risk_factors >= 2:  # ASCVD高危
            return "ASCVD风险为高危的糖尿病患者", "LDL-C<1.8 mmol/L", "I", "A"
        else:  # ASCVD中低危
            return "ASCVD风险为中低危的糖尿病患者", "LDL-C<2.6 mmol/L", "II a", "C"
    
    # 非糖尿病患者的原有逻辑
    if ascvd:
        if severe_ascvd_events >= 2 or (severe_ascvd_events == 1 and high_risk_factors >= 2):
            return "超高危人群", "LDL-C<1.4 mmol/L，且较基线降低幅度>50%", "I", "A"
        else:
            return "极高危人群", "LDL-C<1.8 mmol/L，且较基线降低幅度>50%", "I", "A"
    else:
        if ldl_c >= 4.9 or tc >= 7.2 or (hdl_c < 1.0 and high_risk_factors >= 2):
            return "高危人群", "LDL-C<2.6 mmol/L", "I", "A"
        else:
            return "需要进一步评估", "LDL-C<3.4 mmol/L", "II a", "B"

def count_high_risk_factors():
    factors = [
        var_ldl_c.get(),
        var_early_chd.get(),
        var_fh.get(),
        var_cabg_pci.get(),
        var_diabetes.get(),
        var_hypertension.get(),
        var_ckd.get(),
        var_smoking.get()
    ]
    return sum(factors)

def count_severe_ascvd_events():
    events = [
        var_acs.get(),
        var_mi.get(),
        var_stroke.get(),
        var_pad.get()
    ]
    return sum(events)

def update_high_risk_count():
    count = count_high_risk_factors()
    label_high_risk_count.config(text=f"高风险因素计数: {count}")

def update_severe_ascvd_count():
    count = count_severe_ascvd_events()
    label_severe_ascvd_count.config(text=f"严重ASCVD事件计数: {count}")

def on_submit():
    try:
        ascvd = var_ascvd.get() == 1
        has_diabetes = var_diabetes.get()  # 获取糖尿病状态
        
        if ascvd:
            severe_ascvd_events = count_severe_ascvd_events()
            high_risk_factors = count_high_risk_factors()
            
            # 获取原始ASCVD分级
            if severe_ascvd_events >= 2 or (severe_ascvd_events == 1 and high_risk_factors >= 2):
                risk_level = "超高危人群"
                target = "LDL-C<1.4 mmol/L，且较基线降低幅度>50%"
                rec_class = "I"
                evidence = "A"
            else:
                risk_level = "极高危人群"
                target = "LDL-C<1.8 mmol/L，且较基线降低幅度>50%"
                rec_class = "I"
                evidence = "A"
            
            # 如果有糖尿病，添加糖尿病相关的分级信息
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
        else:
            ldl_c = float(entry_ldl_c.get())
            tc = float(entry_tc.get())
            hdl_c = float(entry_hdl_c.get())
            tg = float(entry_tg.get())
            risk_level, target, rec_class, evidence = classify_hyperlipidemia(
                ldl_c, tc, hdl_c, tg, ascvd, 0, 0
            )
            result_message = (
                f"ASCVD风险等级：{risk_level}\n\n"
                f"治疗目标：\n\n"
                f"{target}\n\n"
                f"推荐类别：{rec_class}  证据等级：{evidence}"
            )
            messagebox.showinfo("风险评估结果及治疗目标", result_message)
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的数值")

def clear_widgets():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text").startswith("是否存在动脉粥样硬化性心血管疾病"):
            continue
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Button):
            widget.grid_forget()

def show_secondary_prevention_options():
    clear_widgets()
    
    # 创建二级预防标签
    tk.Label(root, text="二级预防", font=("Arial", 14)).grid(row=2, column=0, columnspan=2)

    # 创建严重ASCVD事件计数标签
    global label_severe_ascvd_count
    label_severe_ascvd_count = tk.Label(root, text="严重ASCVD事件计数: 0")
    label_severe_ascvd_count.grid(row=3, column=0, columnspan=2)

    # 创建并放置严重ASCVD事件复选框
    global var_acs, var_mi, var_stroke, var_pad
    var_acs = tk.IntVar()
    tk.Checkbutton(root, text="近期ACS病史（<1年）", variable=var_acs, command=update_severe_ascvd_count).grid(row=4, column=0, columnspan=2, sticky='w')

    var_mi = tk.IntVar()
    tk.Checkbutton(root, text="既往心肌梗死病史（除上述ACS以外）", variable=var_mi, command=update_severe_ascvd_count).grid(row=5, column=0, columnspan=2, sticky='w')

    var_stroke = tk.IntVar()
    tk.Checkbutton(root, text="缺血性脑卒中史", variable=var_stroke, command=update_severe_ascvd_count).grid(row=6, column=0, columnspan=2, sticky='w')

    var_pad = tk.IntVar()
    tk.Checkbutton(root, text="有症状的周围血管病变，既往接受过血运重建或截肢", variable=var_pad, command=update_severe_ascvd_count).grid(row=7, column=0, columnspan=2, sticky='w')

    # 创建高风险因素计数标签
    global label_high_risk_count
    label_high_risk_count = tk.Label(root, text="高风险因素计数: 0")
    label_high_risk_count.grid(row=8, column=0, columnspan=2)

    # 创建并放置高风险因素复选框
    global var_ldl_c, var_early_chd, var_fh, var_cabg_pci, var_diabetes, var_hypertension, var_ckd, var_smoking
    var_ldl_c = tk.IntVar()
    tk.Checkbutton(root, text="LDL-C ≤ 1.8 mmol/L, 再次发生严重的 ASCVD事件", variable=var_ldl_c, command=update_high_risk_count).grid(row=9, column=0, columnspan=2, sticky='w')

    var_early_chd = tk.IntVar()
    tk.Checkbutton(root, text="早发冠心病（男<55岁，女<65岁）", variable=var_early_chd, command=update_high_risk_count).grid(row=10, column=0, columnspan=2, sticky='w')

    var_fh = tk.IntVar()
    tk.Checkbutton(root, text="家族性高胆固醇血症或基线LDL—C≥4.9 mmol/L", variable=var_fh, command=update_high_risk_count).grid(row=11, column=0, columnspan=2, sticky='w')

    var_cabg_pci = tk.IntVar()
    tk.Checkbutton(root, text="既往有CABG或PCI史", variable=var_cabg_pci, command=update_high_risk_count).grid(row=12, column=0, columnspan=2, sticky='w')

    var_diabetes = tk.IntVar()
    tk.Checkbutton(root, text="糖尿病", variable=var_diabetes, command=update_high_risk_count).grid(row=13, column=0, columnspan=2, sticky='w')

    var_hypertension = tk.IntVar()
    tk.Checkbutton(root, text="高血压", variable=var_hypertension, command=update_high_risk_count).grid(row=14, column=0, columnspan=2, sticky='w')

    var_ckd = tk.IntVar()
    tk.Checkbutton(root, text="CKD3-4期", variable=var_ckd, command=update_high_risk_count).grid(row=15, column=0, columnspan=2, sticky='w')

    var_smoking = tk.IntVar()
    tk.Checkbutton(root, text="吸烟", variable=var_smoking, command=update_high_risk_count).grid(row=16, column=0, columnspan=2, sticky='w')

    # 创建并放置提交按钮
    tk.Button(root, text="Submit", command=on_submit).grid(row=17, column=0, columnspan=2)

def show_primary_prevention_options():
    clear_widgets()
    
    # 创建一级预防标签
    tk.Label(root, text="一级预防", font=("Arial", 14)).grid(row=2, column=0, columnspan=2)

    # 基本信息输入
    tk.Label(root, text="总胆固醇 (TC, mmol/L):").grid(row=3, column=0, sticky="w")
    global entry_tc
    entry_tc = tk.Entry(root)
    entry_tc.grid(row=3, column=1)

    tk.Label(root, text="低密度脂蛋白胆固醇 (LDL-C, mmol/L):").grid(row=4, column=0, sticky="w")
    global entry_ldl_c
    entry_ldl_c = tk.Entry(root)
    entry_ldl_c.grid(row=4, column=1)

    tk.Label(root, text="高密度脂蛋白胆固醇 (HDL-C, mmol/L):").grid(row=5, column=0, sticky="w")
    global entry_hdl_c
    entry_hdl_c = tk.Entry(root)
    entry_hdl_c.grid(row=5, column=1)

    tk.Label(root, text="年龄:").grid(row=6, column=0, sticky="w")
    global entry_age
    entry_age = tk.Entry(root)
    entry_age.grid(row=6, column=1)

    # 性别选择
    tk.Label(root, text="性别:").grid(row=7, column=0, sticky="w")
    global gender_var
    gender_var = tk.StringVar(value="male")
    tk.Radiobutton(root, text="男性", variable=gender_var, value="male").grid(row=7, column=1, sticky="w")
    tk.Radiobutton(root, text="女性", variable=gender_var, value="female").grid(row=7, column=2, sticky="w")

    # 第一步高危因素
    tk.Label(root, text="高危筛查:", font=("Arial", 12)).grid(row=8, column=0, columnspan=2, sticky="w")
    global var_diabetes, var_ckd
    var_diabetes = tk.BooleanVar()
    tk.Checkbutton(root, text="糖尿病", variable=var_diabetes).grid(row=9, column=0, sticky="w")
    
    var_ckd = tk.BooleanVar()
    tk.Checkbutton(root, text="CKD 3-4期", variable=var_ckd).grid(row=10, column=0, sticky="w")

    # 第二步危险因素
    tk.Label(root, text="危险因素:", font=("Arial", 12)).grid(row=11, column=0, columnspan=2, sticky="w")
    global var_smoking, var_hypertension
    var_smoking = tk.BooleanVar()
    tk.Checkbutton(root, text="吸烟", variable=var_smoking).grid(row=12, column=0, sticky="w")
    
    var_hypertension = tk.BooleanVar()
    tk.Checkbutton(root, text="高血压", variable=var_hypertension).grid(row=13, column=0, sticky="w")

    # 创建全局变量用于余生危险因素的控件
    global lifetime_risk_frame
    lifetime_risk_frame = tk.Frame(root)
    lifetime_risk_frame.grid(row=14, column=0, columnspan=2, sticky="w")
    lifetime_risk_frame.grid_remove()  # 初始隐藏

    # 评估按钮
    global evaluate_button
    evaluate_button = tk.Button(root, text="评估风险", command=on_evaluate_primary_prevention)
    evaluate_button.grid(row=15, column=0, columnspan=2)

def show_lifetime_risk_factors():
    """显示余生危险因素评估部分"""
    lifetime_risk_frame.grid()
    
    tk.Label(lifetime_risk_frame, text="余生危险因素:", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, sticky="w")
    global var_high_bp, var_high_nonhdl, var_low_hdl, var_high_bmi
    var_high_bp = tk.BooleanVar()
    tk.Checkbutton(lifetime_risk_frame, text="收缩压≥160mmHg或舒张压≥100mmHg", variable=var_high_bp).grid(row=1, column=0, columnspan=2, sticky="w")
    
    var_high_nonhdl = tk.BooleanVar()
    tk.Checkbutton(lifetime_risk_frame, text="非HDL-C≥5.2 mmol/L", variable=var_high_nonhdl).grid(row=2, column=0, sticky="w")
    
    var_low_hdl = tk.BooleanVar()
    tk.Checkbutton(lifetime_risk_frame, text="HDL-C<1.0 mmol/L", variable=var_low_hdl).grid(row=3, column=0, sticky="w")
    
    var_high_bmi = tk.BooleanVar()
    tk.Checkbutton(lifetime_risk_frame, text="BMI≥28 kg/m²", variable=var_high_bmi).grid(row=4, column=0, sticky="w")
    
    # 移动评估按钮到余生危险因素下方
    evaluate_button.grid(row=16, column=0, columnspan=2)

def hide_lifetime_risk_factors():
    """隐藏余生危险因素评估部分"""
    lifetime_risk_frame.grid_remove()
    evaluate_button.grid(row=15, column=0, columnspan=2)

def on_evaluate_primary_prevention():
    try:
        # 获取基本信息
        tc = float(entry_tc.get())
        ldl_c = float(entry_ldl_c.get())
        hdl_c = float(entry_hdl_c.get())
        age = int(entry_age.get())
        gender = gender_var.get()
        has_diabetes = var_diabetes.get()

        # 第一步：高危筛查
        if (ldl_c >= 4.9 or tc >= 7.2 or 
            (has_diabetes and age >= 40) or 
            var_ckd.get()):
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
            hide_lifetime_risk_factors()
            return messagebox.showinfo("风险评估结果及治疗目标", result_message)

        # 计算危险因素数量
        risk_factors = 0
        if var_smoking.get():
            risk_factors += 1
        if hdl_c < 1.0:
            risk_factors += 1
        if (gender == "male" and age >= 45) or (gender == "female" and age >= 55):
            risk_factors += 1

        # 第二步：根据高血压和危险因素评估
        has_hypertension = var_hypertension.get()
        
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
            if not lifetime_risk_frame.winfo_viewable():
                show_lifetime_risk_factors()
                return  # 第一次点击，显示余生危险因素选项并返回
            else:
                # 已经显示了余生危险因素，计算结果
                lifetime_risk_factors = 0
                if var_high_bp.get():
                    lifetime_risk_factors += 1
                if var_high_nonhdl.get():
                    lifetime_risk_factors += 1
                if var_low_hdl.get():
                    lifetime_risk_factors += 1
                if var_high_bmi.get():
                    lifetime_risk_factors += 1
                if var_smoking.get():
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
                messagebox.showinfo("风险评估结果及治疗目标", result_message)
                hide_lifetime_risk_factors()
        else:
            # 不需要余生危险评估的情况
            hide_lifetime_risk_factors()
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
            messagebox.showinfo("风险评估结果及治疗目标", result_message)

    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的数值")

# 创建主窗口
root = tk.Tk()
root.title("Hyperlipidemia Classifier")

# 创建并放置ASCVD选择框
ascvd_label = tk.Label(root, text="是否存在动脉粥样硬化性心血管疾病（ASCVD）（冠心病、脑卒中和外周动脉疾病）:")
ascvd_label.grid(row=0, column=0, columnspan=2, sticky='w')
var_ascvd = tk.IntVar(value=-1)  # Initialize to a value that does not correspond to either option
tk.Radiobutton(root, text="是", variable=var_ascvd, value=1, command=show_secondary_prevention_options).grid(row=1, column=0, sticky='w')
tk.Radiobutton(root, text="否", variable=var_ascvd, value=0, command=show_primary_prevention_options).grid(row=1, column=1, sticky='w')

root.mainloop()