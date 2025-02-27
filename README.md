# 血脂风险评估系统

## 项目结构
```
hyperlipidemia-classifier/
├── .gitignore           # Git ignore file
├── LICENSE              # MIT License file
├── README.md            # Project documentation
├── requirements.txt     # Project dependencies
├── setup.py             # Package installation configuration
├── docs/                # Documentation directory
│   ├── images/          # Image resources
│   │   ├── flow_chart_1.jpg
│   │   ├── flow_chart_2.jpg
│   │   ├── risk_assessment.jpg
│   │   └── ui_screenshot.jpg
│   ├── archive/         # Archived files
│   │   └── main.py      # Old version code
│   └── logic/           # Logic documentation
│       ├── __init__.py  # Package initialization file
│       └── 一级预防逻辑.txt
└── src/                 # Source code directory
    ├── __init__.py      # Package initialization file
    ├── lipid_risk_assessor.py  # Main program
    ├── classifier.py    # Classifier module
    ├── config/          # Configuration files directory
    │   └── __init__.py  # Package initialization file
    ├── utils/           # Utility functions directory
    │   ├── __init__.py  # Package initialization file with utility functions
    │   └── ocr_to_markdown.py  # OCR script
    └── tests/           # Tests directory
        ├── __init__.py  # Package initialization file
        └── test_classifier.py
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
- v1.0.0 (2024-01)
  * Initial release
  * Basic lipid assessment functionality
  * Added diabetes management module
  * Optimized user interface

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Copyright Information
© 2024 [znhskzj]. All Rights Reserved.

## 新项目结构
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
├── .gitignore
├── LICENSE
├── README.md
├── setup.py
└── VERSION

```