#!/bin/bash

# 定义日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 进入项目目录
cd $HOME/hyperlipidemia_web
log "切换到项目目录"

# 激活虚拟环境
source $HOME/venv/bin/activate
log "虚拟环境已激活"

# 设置环境变量
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export PYTHONPATH=$PYTHONPATH:$(pwd)
log "环境变量设置完成"

# 检查wsgi.py文件是否存在
if [ ! -f "wsgi.py" ]; then
    log "wsgi.py文件不存在，创建..."
    echo 'from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)' > wsgi.py
    log "wsgi.py文件创建完成"
fi

# 检查app目录结构
log "检查app目录结构:"
ls -la app/
log "检查app/__init__.py文件:"
cat app/__init__.py

# 尝试直接导入app模块
log "尝试导入app模块:"
python -c "import app; print('成功导入app模块')"

# 尝试直接导入wsgi模块
log "尝试导入wsgi模块:"
python -c "import wsgi; print('成功导入wsgi模块')"

# 尝试运行Flask应用
log "尝试运行Flask应用:"
python -m flask run --host=0.0.0.0 --port=5000 --no-debugger --no-reload &
FLASK_PID=$!
log "Flask应用启动，PID: $FLASK_PID"

# 等待应用启动
sleep 3

# 测试应用是否响应
log "测试应用是否响应:"
curl -s http://localhost:5000 > /dev/null
if [ $? -eq 0 ]; then
    log "应用响应正常"
else
    log "应用无响应"
fi

# 停止Flask应用
kill $FLASK_PID
log "测试完成，已停止Flask应用" 