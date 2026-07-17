from flask import Flask
from flask_cors import CORS
from config import Config
from .models import init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    CORS(app)
    init_db(app)

    # 注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # 注册错误处理
    from .api import register_error_handlers
    register_error_handlers(app)

    return app
