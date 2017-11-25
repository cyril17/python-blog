# coding=utf-8

from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.mail import Mail
from flask.ext.redis import FlaskRedis
from flask.ext.compress import Compress

from config import config


mongo = PyMongo()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()
mail = Mail()
redis = FlaskRedis()
compress = Compress()

from core.models.helpers.redis_cache_decorator import JinjaCache
jinja_cache_ext = JinjaCache()


def create_app(config_name):
    """
    u根据配置创建 app
    :param config_name:
    :return: flask app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    compress.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)
    redis.init_app(app)
    jinja_cache_ext.init_app(app)

    # 引入蓝本
    from .core.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .core.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')
    from .core.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .core.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    return app
