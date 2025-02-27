#!/bin/bash
cd ~/hyperlipidemia_web

# 安装依赖
pip install -r requirements/web.txt

# 设置生产环境
export FLASK_ENV=production
export SERVER_ENV=production

# 重启服务
pkill -f gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app --log-file=- 