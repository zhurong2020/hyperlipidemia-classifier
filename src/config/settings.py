"""
Configuration settings for the hyperlipidemia classifier application.
This file contains centralized configuration settings that can be imported throughout the application.
"""

# Server configuration
SERVER_IP = "74.48.63.73"
DOMAIN_NAME = "med.zhurong.link"
SERVER_URL = f"https://{DOMAIN_NAME}"

# WeChat configuration
WECHAT_TOKEN = "Thisismyfirstappinwechat"
WECHAT_APP_ID = "wxe63b0d994fef19ce"
WECHAT_ENCODING_AES_KEY = "VhUQjxUFKLngj27xKbfycxsmwVL1qdpJqnk9YiuL9"
WECHAT_ENCRYPTION_MODE = "compatible"  # Options: "plain", "compatible", "safe"
WECHAT_CALLBACK_PATH = "/wechat"
WECHAT_CALLBACK_URL = f"{SERVER_URL}{WECHAT_CALLBACK_PATH}"

# Application paths
ASSESSMENT_PATH = "/"
ASSESSMENT_URL = f"{SERVER_URL}{ASSESSMENT_PATH}" 