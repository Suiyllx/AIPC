"""
Flask 应用入口
启动方式：
  开发：python app.py
  生产：gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
"""
import logging
from flask import Flask
from flask_cors import CORS

from config import Config
from api import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # 允许前端跨域（生产环境建议指定 origins）
    CORS(app)

    # 注册蓝图
    app.register_blueprint(bp)

    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG if Config.DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    return app


if __name__ == "__main__":
    application = create_app()
    print(f"\n  MOCK_MODE = {Config.MOCK_MODE}  |  DEBUG = {Config.DEBUG}  |  BRANCH_NO = {Config.BRANCH_NO}\n")
    application.run(host="0.0.0.0", port=5001, debug=Config.DEBUG)
