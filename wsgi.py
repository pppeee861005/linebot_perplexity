"""
WSGI 應用程式配置
用於 PythonAnywhere 部署
"""

import os
import sys
from dotenv import load_dotenv

# 添加專案目錄到 Python 路徑
project_dir = '/home/peter861005/project_linebot/linebot_search'
sys.path.insert(0, project_dir)

# 載入 .env 檔案中的環境變數
env_path = os.path.join(project_dir, '.env')
load_dotenv(env_path)

# 導入 Flask 應用程式
from main import app

# WSGI 應用程式實例
application = app

if __name__ == "__main__":
    application.run()
