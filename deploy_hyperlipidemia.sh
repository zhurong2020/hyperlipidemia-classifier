   #!/bin/bash

   # 进入项目目录
   cd ~/hyperlipidemia_web

   # 激活虚拟环境
   source venv/bin/activate

   # 安装依赖
   pip install -r requirements.txt

   # 重启 Flask 应用
   pkill -f gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app --log-level debug > gunicorn.log 2>&1 &