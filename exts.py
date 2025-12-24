# 解决循环引用的问题 放置第三方插件对象
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_redis import FlaskRedis

db = SQLAlchemy()
mail = Mail()
flask_redis = FlaskRedis()