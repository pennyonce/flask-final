from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.author import bp as author_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

Migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(author_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()

# url传参
# 邮件发送
# ajax
# orm和数据库
# jinjia2模板
# cookie和session
# 搜索

# 前端
# 部署

# flask全栈开发
# flask + websocket实战
