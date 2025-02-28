#!/bin/bash

# 微信公众号Nginx配置脚本
# 此脚本用于配置Nginx以支持微信公众号与Flask应用的集成

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    log "请以root权限运行此脚本"
    exit 1
fi

# 检查Nginx是否安装
if ! command -v nginx &> /dev/null; then
    log "Nginx未安装，请先安装Nginx"
    exit 1
fi

# 设置变量
NGINX_CONF_DIR="/etc/nginx/conf.d"
NGINX_SITE_CONF="$NGINX_CONF_DIR/wechat_hyperlipidemia.conf"
APP_DIR="$HOME/hyperlipidemia_web"
DOMAIN_NAME="med.zhurong.link"
CERT_DOMAIN="zhurong.link"  # 使用已存在的证书域名
SERVER_IP="74.48.63.73"

# 创建Nginx配置
log "创建Nginx配置文件: $NGINX_SITE_CONF"

cat > "$NGINX_SITE_CONF" << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;
    
    # 将HTTP请求重定向到HTTPS
    location / {
        return 301 https://$DOMAIN_NAME\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name $DOMAIN_NAME;

    ssl_certificate /etc/letsencrypt/live/$CERT_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$CERT_DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';

    access_log /var/log/nginx/hyperlipidemia_access.log;
    error_log /var/log/nginx/hyperlipidemia_error.log;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /wechat {
        # 特别处理微信请求
        proxy_pass http://127.0.0.1:5000/wechat;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 增加超时时间，微信服务器要求5秒内响应
        proxy_connect_timeout 3s;
        proxy_read_timeout 4s;
        proxy_send_timeout 4s;
    }

    # 静态文件缓存
    location /static {
        alias $APP_DIR/app/static;
        expires 30d;
    }
}
EOF

# 检查配置文件语法
log "检查Nginx配置语法"
nginx -t

if [ $? -ne 0 ]; then
    log "Nginx配置语法错误，请检查配置"
    exit 1
fi

# 重新加载Nginx配置
log "重新加载Nginx配置"
systemctl reload nginx

if [ $? -ne 0 ]; then
    log "重新加载Nginx配置失败"
    exit 1
fi

log "Nginx配置成功完成"
log "现在您可以通过 https://$DOMAIN_NAME 访问您的应用"
log "微信公众号应配置服务器地址为: https://$DOMAIN_NAME/wechat"

# 检查防火墙设置
if command -v ufw &> /dev/null; then
    log "检查UFW防火墙设置"
    if ! ufw status | grep -q "80/tcp.*ALLOW"; then
        log "开放80端口"
        ufw allow 80/tcp
    else
        log "80端口已开放"
    fi
    
    if ! ufw status | grep -q "443/tcp.*ALLOW"; then
        log "开放443端口"
        ufw allow 443/tcp
        ufw reload
    else
        log "443端口已开放"
    fi
fi

# 输出微信公众号配置信息
log "=== 微信公众号配置信息 ==="
log "URL(服务器地址): https://$DOMAIN_NAME/wechat"
log "Token: Thisismyfirstappinwechat"
log "EncodingAESKey: VhUQjxUFKLngj27xKbfycxsmwVL1qdpJqnk9YiuL9"
log "消息加解密方式: 兼容模式"
log "==========================" 