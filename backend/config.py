import os
from dotenv import load_dotenv

load_dotenv()  # 从同目录的 .env 读取变量，生产环境由系统注入

class Config:
    ORACLE_HOST    = os.getenv("ORACLE_HOST", "172.19.187.61")
    ORACLE_PORT    = int(os.getenv("ORACLE_PORT", 1521))
    ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "ORCL")
    ORACLE_USER    = os.getenv("ORACLE_USER", "")
    ORACLE_PASSWORD= os.getenv("ORACLE_PASSWORD", "")
    BRANCH_NO      = os.getenv("BRANCH_NO", "291")
    DEBUG          = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    # 本地开发无内网时置为 true，接口返回仿真假数据，字段结构与真实完全一致
    MOCK_MODE      = os.getenv("MOCK_MODE", "false").lower() == "true"
