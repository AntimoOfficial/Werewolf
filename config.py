import os
from dotenv import load_dotenv

def load_api_key():
    """
    从 .env 文件中加载 API 密钥。
    确保在项目根目录中创建了 .env 文件，并包含如下格式的行：
    API_KEY="your_api_key_here"
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY 未在 .env 文件中设置。请检查文件是否存在且格式正确。")
    return api_key

# 在模块加载时可以先进行一次检查，以便尽早发现问题
try:
    API_KEY = load_api_key()
except ValueError as e:
    print(f"配置错误: {e}")
    API_KEY = None
