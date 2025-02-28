# 血脂风险评估业务流程

## 流程图
![流程图](/docs/images/assessment_flow.png)

## 流程说明

### 1. 初始判断
```python
if ascvd_selected:
    run_secondary_prevention()
else:
    run_primary_prevention()
```

### 2. 二级预防流程
```text
1. 收集严重ASCVD事件（4类）
   - 近期ACS
   - 心肌梗死史
   - 脑卒中史
   - 周围血管病变
2. 统计事件数量 → count_events()
3. 收集高风险因素（8项）→ collect_risk_factors()
4. 计算总分 → calculate_risk_score()
5. 判断风险等级：
   if events >=2 or (events==1 and factors>=2):
       等级 = 超高危
   else:
       等级 = 极高危
6. 生成治疗目标 → generate_target(等级)
```

### 3. 一级预防流程
```text
1. 输入生物指标：
   - TC, LDL-C, HDL-C, TG
   - 年龄, 性别
2. 初步筛查：
   if LDL≥4.9 or TC≥7.2 or (糖尿病+年龄≥40) or CKD3-4期:
       等级 = 高危
   else:
       3.1 计算基础风险因素 → count_basic_factors()
       3.2 高血压分级 → evaluate_hypertension()
       3.3 终生风险评估（条件触发）→ check_lifetime_risk()
3. 最终确定治疗目标
```

## 代码映射表
| 流程步骤        | 对应代码文件                 | 主要函数/方法                 |
|-----------------|------------------------------|-------------------------------|
| 初始判断        | src/core/risk_calculator.py  | assess_risk()                 |
| 二级预防流程    | src/core/secondary.py        | process_secondary()           |
| 事件统计        | src/core/event_counter.py    | count_severe_events()         |
| 风险因素收集    | src/core/factor_collector.py | collect_high_risk_factors()    |
| 一级预防流程    | src/core/primary.py          | process_primary()             |
| 目标生成        | src/core/target_generator.py | generate_treatment_target()   | 