# 血脂风险评估系统

## 项目结构
```
hyperlipidemia-classifier/
├── .github/
│   └── workflows/
│       └── deploy.yml   # CI/CD配置
├── app/                 # Web应用模块
│   ├── __init__.py
│   ├── routes.py        # 路由配置
│   └── templates/
│       └── index.html   # 网页模板
├── docs/                # Documentation directory
│   ├── images/          # Image resources
│   ├── archive/         # Archived files
│   │   └── main.py      # Old version code
│   ├── logic/           # Logic documentation
│   └── ocr_output
├── requirements/        # 依赖管理
│   ├── base.txt         # 基础依赖
│   ├── web.txt          # Web服务依赖
│   └── desktop.txt      # 桌面应用依赖
├── scripts/             # 部署脚本
│   └── deploy_hyperlipidemia.sh
├── src/
│   ├── config/            
│   ├── core/            # 核心计算逻辑
│   │   ├── __init__.py
│   │   ├── lipid_risk_assessor.py
│   │   └── risk_calculator.py
│   ├── desktop/         # 桌面应用
│   │   └── gui_app.py
│   ├── tests/           # 测试目录
│   ├── utils/             
│   ├── web/             # Web服务适配器
│   │   ├── assessor.py
│   │   └── wechat_handler.py
├── legacy/                   # 历史版本代码存档
│   ├── main DM.py           # 原桌面端主程序
│   ├── classifier.py        # 原核心分类逻辑
│   └── requirements.txt     # 原依赖库列表
├── .gitignore
├── LICENSE
├── README.md
├── setup.py
└── VERSION
```

## Technical Framework
- Programming Language: Python 3.x
- GUI Framework: Tkinter
- Dependency Management: pip

## Main Features
1. ASCVD risk stratification assessment
2. Lipid treatment goal setting
3. Special assessment standards for diabetic patients
4. Lifetime risk factor assessment (for specific populations)

## Tesseract Installation on Windows

To use the OCR functionality, you need to install Tesseract on your Windows system:

1. **Download and Install Tesseract**:
   - Download the Tesseract installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
   - Run the installer and follow the instructions to complete the installation.

2. **Add Tesseract to PATH**:
   - Find the installation path of Tesseract (e.g., `C:\Program Files\Tesseract-OCR`).
   - Open the Start Menu and search for "Environment Variables".
   - Click "Edit the system environment variables".
   - In the System Properties window, click "Environment Variables".
   - Under "System variables", find and select the "Path" variable, then click "Edit".
   - Click "New" and add the path to the Tesseract installation directory.
   - Click "OK" to close all dialog boxes.

3. **Verify Installation**:
   - Open a command prompt and type:
     ```bash
     tesseract --version
     ```
   - You should see the version information for Tesseract.

## Assessment Process

### Primary Prevention (No ASCVD)
1. Basic Information Entry:
   - Lipid indicators (TC, LDL-C, HDL-C, TG)
   - Age and gender
   - Risk factors (diabetes, CKD, smoking, etc.)

2. Risk Stratification Standards:
   - High Risk: LDL-C ≥ 4.9 mmol/L or TC ≥ 7.2 mmol/L; diabetes and age ≥ 40 years; CKD 3-4 stage
   - Moderate Risk: Evaluated based on the number of risk factors and lipid levels
   - Low Risk: Other situations

3. Lifetime Risk Assessment (for moderate risk and age <55)

### Secondary Prevention (With ASCVD)
1. Assessment of severe ASCVD events
2. Assessment of high-risk factors
3. Determine risk level (very high risk/extremely high risk)

## Treatment Goals

### Non-Diabetic Patients
- Extremely High Risk: LDL-C<1.4 mmol/L, and >50% reduction from baseline
- Very High Risk: LDL-C<1.8 mmol/L, and >50% reduction from baseline
- High Risk: LDL-C<2.6 mmol/L
- Moderate Risk: LDL-C<2.6 mmol/L
- Low Risk: LDL-C<3.4 mmol/L

### Diabetic Patients
1. With ASCVD:
   - LDL-C<1.4 mmol/L
   - Non-HDL-C<2.2 mmol/L

2. High ASCVD Risk:
   - LDL-C<1.8 mmol/L
   - Non-HDL-C<2.6 mmol/L

3. Moderate to Low ASCVD Risk:
   - LDL-C<2.6 mmol/L
   - Non-HDL-C<3.4 mmol/L

## Usage Instructions
1. Run the program and first select whether the patient has ASCVD
2. Enter the relevant information as prompted
3. Click the assessment button to get risk stratification and treatment goals
4. If eligible for lifetime risk assessment, additional assessment options will appear

## Notes
- All numerical inputs must use Arabic numerals
- Lipid indicators are in mmol/L
- Age must be an integer
- Ensure all necessary information is filled in before assessment

## Installation Instructions
1. Clone the project locally
   ```bash
   git clone https://github.com/zhurong2020/hyperlipidemia-classifier
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program
   ```bash
   python src/lipid_risk_assessor.py
   ```

## Development Team
- Project Lead: [chenqizhi]
- Developer: [zhurong2020]
- Medical Consultant: [chenqizhi]

## Version History

### v0.2.1 (2024-03) - 业务逻辑优化
**核心改进**：
- 业务逻辑文档化
  - 新增`docs/logic`目录存放业务流程文档
  - 添加`assessment_flow.md`和`assessment_flow.puml`流程图
  - 记录一级预防和二级预防的详细评估逻辑
- 代码修复
  - 修复GUI界面初始显示问题
  - 补充遗漏的TG输入字段
  - 完善风险评估逻辑实现
  - 修正余生风险评估功能
- 质量提升
  - 根据原始代码校对业务流程
  - 确保新旧版本功能一致性

### v0.2.0 (2024-03) - 架构升级
**核心改进**：
- 项目结构重构
  - 新增`src/core`存放核心算法
  - 分离桌面和Web实现
  - 添加`legacy`目录保存历史代码
- 代码质量提升
  - 采用面向对象设计
  - 增加类型提示
  - 完善异常处理
- 新功能
  - 支持Web服务
  - 添加自动化测试
  - 实现UI对比工具

### v0.1.2 (2024-02) - 问题修复
- 修复输入验证漏洞
- 优化糖尿病评估逻辑
- 更新依赖版本

### v0.1.0 (2024-01) - 初始版本
- 实现基础评估功能
- 开发桌面端界面
- 制定糖尿病管理标准

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Copyright Information
© 2024 [znhskzj]. All Rights Reserved.

## 快速开始

### 运行历史版本（仅供参考）
```bash
# 进入legacy目录
cd legacy

# 安装历史版本依赖
pip install -r requirements.txt

# 运行原桌面程序
python "main DM.py"
```

### 运行新版本桌面程序
```bash
# 使用新的运行脚本
python run_desktop.py
```

### 业务逻辑文档
为了更好地理解系统的评估流程，我们提供了详细的业务逻辑文档：
1. `docs/logic/assessment_flow.md` - 完整的评估流程说明
2. `docs/logic/assessment_flow.puml` - PlantUML格式的流程图
3. `docs/logic/一级预防逻辑.txt` - 一级预防详细逻辑说明

这些文档可以帮助开发者和医疗专业人员理解系统的决策过程，确保实现的准确性。

## 版本迁移指南

我们保留了历史版本代码以方便参考：
1. `legacy/`目录包含重构前的完整代码
2. 主要改进点：
   - 模块化核心逻辑到`src/core`
   - 分离GUI和业务逻辑
   - 增强可维护性的面向对象设计
3. 对比测试方法：
```bash
# 在新旧版本间进行功能对比
python tests/ui_diff_check.py old_ui.png new_ui.png
```

## 依赖管理

历史版本依赖见[legacy/requirements.txt](legacy/requirements.txt)，新版本依赖请参考[requirements/base.txt](requirements/base.txt)。

主要变更：
- 移除了未使用的scikit-learn依赖
- 添加了Flask等Web支持
- 规范了版本约束

### 从v0.1迁移到v0.2
1. 新老版本并行运行验证：
```bash
# 老版本
python legacy/main\ DM.py

# 新版本
python run_desktop.py
```
2. 主要变更点：
   - 移除了全局变量
   - 使用类封装界面逻辑
   - 分离业务逻辑到独立模块
