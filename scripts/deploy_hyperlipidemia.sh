#!/bin/bash
set -e  # 遇到错误立即退出

# 定义日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 进入项目目录
cd ~/hyperlipidemia_web
log "切换到项目目录"

# 确保日志目录存在
mkdir -p ~/hyperlipidemia_web/logs
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
pip install -r requirements/web.txt
log "依赖安装完成"

# 设置生产环境
export FLASK_ENV=production
export SERVER_ENV=production
log "环境变量设置完成"

# 检查是否存在服务PID文件
PID_FILE=~/hyperlipidemia_web/gunicorn.pid
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

# 启动服务
log "启动Gunicorn服务..."
$HOME/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app \
    --pid $PID_FILE \
    --log-file=~/hyperlipidemia_web/logs/gunicorn.log \
    --daemon

# 检查服务是否成功启动
sleep 2
if [ -f "$PID_FILE" ] && ps -p $(cat $PID_FILE) > /dev/null; then
    log "服务成功启动，PID: $(cat $PID_FILE)"
    log "可以通过以下地址访问应用: http://74.48.63.73:5000"
else
    log "服务启动失败，请检查日志"
    exit 1
fi

log "部署完成" 