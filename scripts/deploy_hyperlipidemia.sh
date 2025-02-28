#!/bin/bash
set -e  # 遇到错误立即退出

# 定义日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 进入项目目录
cd $HOME/hyperlipidemia_web
log "切换到项目目录"

# 确保日志目录存在
mkdir -p $HOME/hyperlipidemia_web/logs
log "确保日志目录存在"

# 检查虚拟环境是否存在，如果不存在则创建
if [ ! -d "$HOME/venv" ]; then
    log "虚拟环境不存在，正在创建..."
    python3 -m venv $HOME/venv
    log "虚拟环境创建完成"
fi

# 激活虚拟环境
source $HOME/venv/bin/activate
log "虚拟环境已激活"

# 安装依赖
log "开始安装依赖..."
pip install --upgrade pip
pip install --force-reinstall -r requirements/web.txt
log "依赖安装完成"

# 设置生产环境
export FLASK_ENV=production
export SERVER_ENV=production
export PYTHONPATH=$PYTHONPATH:$(pwd)
log "环境变量设置完成"

# 检查wsgi.py文件是否存在
if [ ! -f "wsgi.py" ]; then
    log "创建wsgi.py文件..."
    echo 'from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)' > wsgi.py
    log "wsgi.py文件创建完成"
fi

# 检查是否存在服务PID文件
PID_FILE=$HOME/hyperlipidemia_web/gunicorn.pid
if [ -f "$PID_FILE" ]; then
    log "发现PID文件，尝试停止现有服务..."
    if kill -TERM $(cat $PID_FILE) 2>/dev/null; then
        log "成功停止现有服务"
    else
        log "无法通过PID文件停止服务，尝试使用pkill..."
        pkill -f "gunicorn.*hyperlipidemia_web" || true
    fi
    rm -f $PID_FILE
else
    log "未发现PID文件，尝试使用pkill停止可能运行的服务..."
    pkill -f "gunicorn.*hyperlipidemia_web" || true
fi

# 清除旧的日志文件
LOG_FILE=$HOME/hyperlipidemia_web/logs/gunicorn.log
> $LOG_FILE
log "清除旧的日志文件"

# 启动服务
log "启动Gunicorn服务..."
$HOME/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app \
    --pid $PID_FILE \
    --log-file=$LOG_FILE \
    --log-level=debug \
    --daemon

# 检查服务是否成功启动
sleep 2
if [ -f "$PID_FILE" ] && ps -p $(cat $PID_FILE) > /dev/null; then
    log "服务成功启动，PID: $(cat $PID_FILE)"
    log "可以通过以下地址访问应用: http://74.48.63.73:5000"
else
    log "服务启动失败，查看日志..."
    if [ -f "$LOG_FILE" ]; then
        log "Gunicorn日志内容:"
        cat $LOG_FILE
    else
        log "找不到Gunicorn日志文件"
    fi
    log "尝试直接运行Flask应用进行调试..."
    FLASK_APP=wsgi.py FLASK_ENV=development python -m flask run --host=0.0.0.0 --port=5000 &
    sleep 2
    log "请检查Flask应用是否正常运行"
    exit 1
fi

log "部署完成" 