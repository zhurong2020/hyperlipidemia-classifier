# 微信公众号集成指南

本文档提供了将血脂风险评估系统与微信公众号"白衣飘飘chen"集成的详细步骤。

## 目录

1. [准备工作](#准备工作)
2. [服务器配置](#服务器配置)
3. [微信公众号配置](#微信公众号配置)
4. [自定义菜单配置](#自定义菜单配置)
5. [测试与验证](#测试与验证)
6. [常见问题](#常见问题)

## 准备工作

### 所需信息

- 微信公众号信息：
  - 原始ID: gh_da2cb6e986d3
  - 公众号名称: 白衣飘飘chen
  - 类型: 订阅号
  - 开发者ID(AppID): wxe63b0d994fef19ce
  - 运营者微信号: a27138100

- 服务器信息：
  - 域名: med.zhurong.link
  - IP地址: 74.48.63.73
  - 操作系统: Ubuntu 20.04.6 LTS
  - 已开放端口: 80, 443, 5000等

### 所需软件

- Python 3.8+
- Nginx
- Gunicorn
- Flask 2.0.1
- Werkzeug 2.0.1
- Let's Encrypt SSL证书

## 服务器配置

### 1. 部署应用

使用我们提供的部署脚本来部署应用：

```bash
# 克隆代码库（如果尚未克隆）
git clone https://github.com/zhurong2020/hyperlipidemia-classifier.git hyperlipidemia_web
cd hyperlipidemia_web

# 运行微信集成部署脚本
bash scripts/deploy_wechat_integration.sh
```

### 2. 配置Nginx

使用我们提供的Nginx配置脚本：

```bash
# 需要root权限
sudo bash scripts/setup_wechat_nginx.sh
```

此脚本将：
- 创建Nginx配置文件
- 配置HTTPS支持
- 设置HTTP到HTTPS的重定向
- 配置反向代理到Flask应用
- 设置适当的超时时间
- 重新加载Nginx配置

## 微信公众号配置

登录微信公众平台(mp.weixin.qq.com)，进行以下配置：

### 1. 基本配置

1. 进入"设置与开发" -> "基本配置"
2. 在"服务器配置"部分，填写以下信息：
   - URL(服务器地址): `https://med.zhurong.link/wechat`
   - Token: `Thisismyfirstappinwechat`
   - EncodingAESKey: `VhUQjxUFKLngj27xKbfycxsmwVL1qdpJqnk9YiuL9`
   - 消息加解密方式: 兼容模式
3. 点击"提交"按钮

### 2. 网页授权域名

1. 进入"设置与开发" -> "公众号设置" -> "功能设置"
2. 在"网页授权域名"部分，添加您的域名
   - 域名: `med.zhurong.link`

## 自定义菜单配置

### 1. 获取access_token

1. 访问微信公众平台接口调试工具：https://mp.weixin.qq.com/debug/cgi-bin/apiinfo
2. 选择"获取access_token接口"
3. 输入您的AppID和AppSecret
4. 点击"检查问题"按钮获取access_token

### 2. 创建自定义菜单

使用我们提供的菜单配置脚本：

```bash
# 激活虚拟环境
source ~/venv/bin/activate

# 运行菜单配置脚本
python scripts/setup_wechat_menu.py <access_token>
```

默认菜单配置包括：
- 血脂评估：点击后直接跳转到评估系统网页
- 使用指南：包含评估说明和指标解读子菜单
- 联系医生：提供医生联系方式

## 测试与验证

### 1. 验证服务器配置

1. 访问 `https://med.zhurong.link` 确认应用正常运行
2. 检查Nginx日志：
   ```bash
   sudo tail -f /var/log/nginx/hyperlipidemia_access.log
   sudo tail -f /var/log/nginx/hyperlipidemia_error.log
   ```
3. 检查应用日志：
   ```bash
   tail -f ~/hyperlipidemia_web/logs/gunicorn.log
   tail -f ~/hyperlipidemia_web/logs/gunicorn_error.log
   ```

### 2. 验证微信公众号配置

1. 关注公众号"白衣飘飘chen"
2. 发送消息测试自动回复功能
3. 点击菜单测试各功能是否正常

## 常见问题

### 微信服务器验证失败

可能原因：
- URL不可访问：确保Nginx和Gunicorn正常运行
- Token不匹配：确保Token与代码中设置的一致
- 响应超时：检查网络连接和应用响应时间
- SSL证书问题：确保SSL证书有效且正确配置

解决方法：
```bash
# 检查应用状态
ps aux | grep gunicorn
# 重启应用
bash scripts/deploy_wechat_integration.sh
# 检查Nginx状态
sudo systemctl status nginx
# 检查SSL证书
sudo certbot certificates
```

### 自定义菜单不显示

可能原因：
- access_token过期：access_token有效期为2小时
- 菜单创建失败：检查API返回的错误信息
- 公众号类型限制：订阅号每天可以修改一次菜单

解决方法：
```bash
# 获取当前菜单配置
python scripts/setup_wechat_menu.py <access_token> get
# 删除当前菜单
python scripts/setup_wechat_menu.py <access_token> delete
# 重新创建菜单
python scripts/setup_wechat_menu.py <access_token> create
```

### 应用无法响应微信消息

可能原因：
- XML解析错误：检查消息格式
- 应用处理超时：微信服务器要求5秒内响应
- 路由配置错误：确保/wechat路由正确配置
- 加密模式不匹配：确保代码支持所选的加密模式

解决方法：
```bash
# 检查应用日志
tail -f ~/hyperlipidemia_web/logs/flask_app.log
# 增加日志记录
# 在wechat_handler.py中添加更详细的日志记录
```

## 更多资源

- [微信公众平台开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [Flask文档](https://flask.palletsprojects.com/)
- [Nginx文档](https://nginx.org/en/docs/) 