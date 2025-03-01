# 血脂风险评估系统 (Hyperlipidemia Risk Assessment System)

A comprehensive system for assessing hyperlipidemia risk, providing risk stratification and treatment recommendations based on clinical guidelines.

## Project Overview

This system provides both web-based and desktop interfaces for healthcare professionals to assess patients' lipid-related cardiovascular risks. It implements the latest clinical guidelines for hyperlipidemia management, offering personalized risk stratification and treatment goals.

### Key Features

1. **Dual Interface**: Available as both web application and desktop software
2. **WeChat Integration**: Accessible through WeChat Official Account
3. **ASCVD Risk Stratification**: Comprehensive assessment of atherosclerotic cardiovascular disease risk
4. **Personalized Treatment Goals**: Customized lipid targets based on risk level
5. **Special Assessment Standards**: Specific criteria for diabetic patients
6. **Lifetime Risk Assessment**: Extended risk evaluation for eligible populations
7. **Secure HTTPS Access**: Encrypted communication via custom domain

## Project Structure
```
hyperlipidemia-classifier/
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD configuration
├── app/                         # Web application module
│   ├── __init__.py              # Flask app initialization
│   ├── routes.py                # Web routes and endpoints
│   ├── static/                  # Static assets (CSS, JS, images)
│   └── templates/
│       └── index.html           # Main web interface template
├── docs/                        # Documentation directory
│   ├── images/                  # Image resources
│   ├── archive/                 # Archived files
│   ├── logic/                   # Logic documentation
│   │   ├── assessment_flow.md   # Assessment process documentation
│   │   └── assessment_flow.puml # Assessment process diagram
│   └── ocr_output               # OCR test outputs
├── legacy/                      # Historical code archive
│   ├── main DM.py               # Original desktop application
│   ├── classifier.py            # Original classification logic
│   └── requirements.txt         # Original dependencies
├── requirements/                # Dependency management
│   ├── base.txt                 # Core dependencies
│   ├── web.txt                  # Web service dependencies
│   └── desktop.txt              # Desktop application dependencies
├── scripts/                     # Deployment and utility scripts
│   ├── deploy_hyperlipidemia.sh # Main deployment script
│   ├── deploy_with_systemd.sh   # Systemd deployment script
│   ├── deploy_wechat_integration.sh # WeChat integration deployment
│   ├── get_wechat_token.py      # Script to obtain WeChat access token
│   ├── setup_wechat_menu.py     # WeChat menu configuration script
│   ├── setup_wechat_nginx.sh    # Nginx configuration for WeChat
│   ├── test_flask_app.sh        # Flask application test script
│   └── hyperlipidemia.service   # Systemd service configuration
├── src/
│   ├── config/                  # Centralized configuration
│   │   └── settings.py          # Application settings (server, WeChat)
│   ├── core/                    # Core calculation logic
│   │   ├── lipid_risk_assessor.py # Main risk assessment logic
│   │   └── risk_calculator.py   # Risk calculation algorithms
│   ├── desktop/                 # Desktop application
│   │   └── gui_app.py           # Tkinter GUI implementation
│   ├── tests/                   # Test directory
│   ├── utils/                   # Utility functions
│   ├── web/                     # Web service adapters
│   │   ├── assessor.py          # Web assessment adapter
│   │   └── wechat_handler.py    # WeChat message handler
│   └── __init__.py
├── .gitignore
├── LICENSE                      # MIT License
├── README.md
├── run_desktop.py               # Desktop application entry point
├── setup.py                     # Package setup script
├── wsgi.py                      # WSGI application entry point
└── VERSION                      # Current version (0.2.4)
```

## Technical Framework

- **Backend**: Python 3.x
- **Web Framework**: Flask
- **Desktop GUI**: Tkinter
- **Deployment**: Gunicorn, Nginx, Systemd
- **HTTPS**: Let's Encrypt SSL
- **WeChat Integration**: WeChat Official Account API
- **Dependency Management**: pip

## Assessment Process

### Primary Prevention (No ASCVD)
1. **Basic Information Entry**:
   - Lipid indicators (TC, LDL-C, HDL-C, TG)
   - Age and gender
   - Risk factors (diabetes, CKD, smoking, hypertension)

2. **Risk Stratification Standards**:
   - **High Risk**: LDL-C ≥ 4.9 mmol/L or TC ≥ 7.2 mmol/L; diabetes and age ≥ 40 years; CKD 3-4 stage
   - **Moderate Risk**: Evaluated based on the number of risk factors and lipid levels
   - **Low Risk**: Other situations

3. **Lifetime Risk Assessment** (for moderate risk and age <55)

### Secondary Prevention (With ASCVD)
1. Assessment of severe ASCVD events
2. Assessment of high-risk factors
3. Determine risk level (very high risk/extremely high risk)

## Treatment Goals

### Non-Diabetic Patients
- **Extremely High Risk**: LDL-C<1.4 mmol/L, and >50% reduction from baseline
- **Very High Risk**: LDL-C<1.8 mmol/L, and >50% reduction from baseline
- **High Risk**: LDL-C<2.6 mmol/L
- **Moderate Risk**: LDL-C<2.6 mmol/L
- **Low Risk**: LDL-C<3.4 mmol/L

### Diabetic Patients
1. **With ASCVD**:
   - LDL-C<1.4 mmol/L
   - Non-HDL-C<2.2 mmol/L

2. **High ASCVD Risk**:
   - LDL-C<1.8 mmol/L
   - Non-HDL-C<2.6 mmol/L

3. **Moderate to Low ASCVD Risk**:
   - LDL-C<2.6 mmol/L
   - Non-HDL-C<3.4 mmol/L

## Installation and Usage

### Web Application
1. Clone the repository:
   ```bash
   git clone https://github.com/zhurong2020/hyperlipidemia-classifier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements/web.txt
   ```

3. Run the development server:
   ```bash
   python wsgi.py
   ```

4. Access the application at:
   - Local development: http://localhost:5000
   - Production: https://med.zhurong.link

### Desktop Application
1. Install dependencies:
   ```bash
   pip install -r requirements/desktop.txt
   ```

2. Run the desktop application:
   ```bash
   python run_desktop.py
   ```

### Deployment
1. Deploy to production server:
   ```bash
   cd scripts
   ./deploy_hyperlipidemia.sh
   ```

2. Deploy with systemd:
   ```bash
   cd scripts
   ./deploy_with_systemd.sh
   ```

3. Configure WeChat integration:
   ```bash
   cd scripts
   ./deploy_wechat_integration.sh
   ```

## WeChat Integration

The system can be accessed through a WeChat Official Account:

1. **Access Method**: Scan QR code or search for the Official Account "白衣飘飘chen"
2. **Usage**: Click on the "血脂评估" menu item to access the web application
3. **Configuration**:
   - Server URL: https://med.zhurong.link/wechat
   - Token: Configured in settings.py
   - EncodingAESKey: Configured in settings.py
   - Encryption Mode: Compatible mode

## Version History

### v0.2.4 (2024-02) - HTTPS and Centralized Configuration
**Core Improvements**:
- **Centralized Configuration**
  - Created new settings file at `src/config/settings.py`
  - Consolidated server and WeChat configuration
  - Updated all scripts to use the centralized settings
- **HTTPS Support**
  - Added support for secure HTTPS connections
  - Configured custom domain (med.zhurong.link)
  - Implemented SSL certificate management
- **WeChat Integration**
  - Updated WeChat configuration for compatibility mode
  - Improved menu integration with direct link to web application
  - Fixed string escaping issues in WeChat handler
- **UI Improvements**
  - Simplified user interface by removing redundant buttons
  - Streamlined risk assessment workflow

### v0.2.3 (2024-02) - WeChat Integration
**Core Improvements**:
- **WeChat Official Account Integration**
  - Added WeChat message handling
  - Implemented custom menu configuration
  - Created deployment scripts for WeChat setup
- **Server Configuration**
  - Added Nginx configuration for WeChat callbacks
  - Implemented token verification
  - Set up message encryption/decryption

### v0.2.2 (2024-02) - Deployment Optimization
**Core Improvements**:
- **Deployment Script Optimization**
  - Replaced `~` with `$HOME` to avoid path resolution issues
  - Enhanced error handling and logging
  - Added `test_flask_app.sh` for Flask application diagnostics
- **Dependency Management Improvements**
  - Fixed Flask and Werkzeug version compatibility issues
  - Added `--force-reinstall` option for dependency installation
  - Added version checking functionality in test scripts
- **Bug Fixes**
  - Resolved Werkzeug `url_quote` import error
  - Fixed directory creation issues in deployment scripts
  - Improved systemd service configuration

### v0.2.1 (2024-02) - Business Logic Optimization
**Core Improvements**:
- **Business Logic Documentation**
  - Added `docs/logic` directory for business process documentation
  - Created assessment flow diagrams and documentation
  - Documented primary and secondary prevention assessment logic
- **Code Fixes**
  - Fixed GUI initial display issues
  - Added missing TG input field
  - Improved risk assessment logic implementation
  - Fixed lifetime risk assessment functionality
- **Quality Improvements**
  - Verified business processes against original code
  - Ensured consistency between old and new versions

### v0.2.0 (2024-01) - Architecture Upgrade
**Core Improvements**:
- **Project Structure Refactoring**
  - Added `src/core` for core algorithms
  - Separated desktop and web implementations
  - Created `legacy` directory for historical code
- **Code Quality Improvements**
  - Implemented object-oriented design
  - Added type hints
  - Improved exception handling
- **New Features**
  - Added web service support
  - Implemented automated testing
  - Created UI comparison tools

### v0.1.2 (2024-01) - Bug Fixes
- Fixed input validation vulnerabilities
- Optimized diabetes assessment logic
- Updated dependency versions

### v0.1.0 (2023-12) - Initial Version
- Implemented basic assessment functionality
- Developed desktop interface
- Established diabetes management standards

## Development Team
- Project Lead: [chenqizhi]
- Developer: [zhurong2020]
- Medical Consultant: [chenqizhi]

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Copyright Information
© 2024 [znhskzj]. All Rights Reserved.
