#!/bin/bash

# 微信公众号集成部署脚本
# 此脚本用于部署微信公众号与Flask应用的集成

# 设置退出时立即报错
set -e

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查依赖
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        log "错误: 未找到 $1，请先安装"
        exit 1
    fi
}

# 检查依赖
check_dependency python3
check_dependency pip
check_dependency nginx

# 设置变量
APP_DIR="$HOME/hyperlipidemia_web"
VENV_DIR="$HOME/venv"
LOGS_DIR="$APP_DIR/logs"
REQUIREMENTS_FILE="$APP_DIR/requirements/web.txt"
DOMAIN_NAME="med.zhurong.link"

# 创建日志目录
log "确保日志目录存在"
mkdir -p "$LOGS_DIR"

# 切换到应用目录
log "切换到应用目录: $APP_DIR"
cd "$APP_DIR"

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    log "创建Python虚拟环境"
    python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境
log "激活虚拟环境"
source "$VENV_DIR/bin/activate"

# 更新pip并安装依赖
log "更新pip并安装依赖"
pip install --upgrade pip
pip install --force-reinstall -r "$REQUIREMENTS_FILE"

# 安装微信集成所需的额外依赖
log "安装微信集成所需的额外依赖"
pip install requests xmltodict

# 确保wsgi.py文件存在
if [ ! -f "$APP_DIR/wsgi.py" ]; then
    log "创建wsgi.py文件"
    cat > "$APP_DIR/wsgi.py" << EOF
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
EOF
fi

# 检查Gunicorn进程
GUNICORN_PID_FILE="$APP_DIR/gunicorn.pid"
if [ -f "$GUNICORN_PID_FILE" ]; then
    log "停止现有Gunicorn进程"
    PID=$(cat "$GUNICORN_PID_FILE")
    if ps -p $PID > /dev/null; then
        kill $PID
        sleep 2
    fi
    rm -f "$GUNICORN_PID_FILE"
fi

# 清理旧日志
log "清理旧日志"
> "$LOGS_DIR/gunicorn.log"
> "$LOGS_DIR/gunicorn_error.log"
> "$LOGS_DIR/flask_app.log"

# 设置环境变量
export FLASK_APP="wsgi.py"
export FLASK_ENV="production"
export PYTHONPATH="$APP_DIR"

# 启动Gunicorn
log "启动Gunicorn"
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 60 \
         --access-logfile "$LOGS_DIR/gunicorn.log" \
         --error-logfile "$LOGS_DIR/gunicorn_error.log" \
         --pid "$GUNICORN_PID_FILE" \
         --daemon \
         wsgi:app

# 检查Gunicorn是否成功启动
sleep 2
if [ -f "$GUNICORN_PID_FILE" ]; then
    PID=$(cat "$GUNICORN_PID_FILE")
    if ps -p $PID > /dev/null; then
        log "Gunicorn成功启动，PID: $PID"
    else
        log "Gunicorn启动失败"
        exit 1
    fi
else
    log "Gunicorn启动失败，未找到PID文件"
    exit 1
fi

# 检查应用是否响应
log "检查应用是否响应"
if curl -s http://localhost:5000 > /dev/null; then
    log "应用响应正常"
else
    log "应用未响应，请检查日志"
    log "Gunicorn日志:"
    tail -n 20 "$LOGS_DIR/gunicorn.log"
    log "Gunicorn错误日志:"
    tail -n 20 "$LOGS_DIR/gunicorn_error.log"
    exit 1
fi

# 配置Nginx（如果需要）
if [ ! -f "/etc/nginx/conf.d/wechat_hyperlipidemia.conf" ]; then
    log "Nginx配置不存在，请运行setup_wechat_nginx.sh脚本"
    log "sudo bash $APP_DIR/scripts/setup_wechat_nginx.sh"
else
    log "Nginx配置已存在"
fi

# 输出微信公众号配置信息
log "=== 微信公众号配置信息 ==="
log "URL(服务器地址): https://$DOMAIN_NAME/wechat"
log "Token: Thisismyfirstappinwechat"
log "EncodingAESKey: VhUQjxUFKLngj27xKbfycxsmwVL1qdpJqnk9YiuL9"
log "消息加解密方式: 兼容模式"
log "==========================="
log "部署完成！"
log "请确保您的服务器防火墙已开放80和443端口"
log "如需配置微信公众号菜单，请运行:"
log "python $APP_DIR/scripts/setup_wechat_menu.py <access_token>" 