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

# 检查服务文件是否已安装，或者需要更新
SERVICE_FILE=/etc/systemd/system/hyperlipidemia.service
log "更新服务文件..."
# 服务文件已经预先配置好用户名和组

# 需要sudo权限安装服务文件
sudo cp scripts/hyperlipidemia.service $SERVICE_FILE
sudo systemctl daemon-reload
sudo systemctl enable hyperlipidemia
log "服务文件更新完成"

# 重启服务
log "重启服务..."
sudo systemctl restart hyperlipidemia

# 检查服务状态
sleep 2
if sudo systemctl is-active --quiet hyperlipidemia; then
    log "服务成功启动"
    log "可以通过以下地址访问应用: http://74.48.63.73:5000"
else
    log "服务启动失败，请检查日志: sudo journalctl -u hyperlipidemia"
    exit 1
fi

log "部署完成" 