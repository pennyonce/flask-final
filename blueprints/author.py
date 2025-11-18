from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('author', __name__, url_prefix='/author')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('邮箱已存在')
                return redirect(url_for('author.login'))
            if check_password_hash(user.password, password):
                # cookie 存放登录授权的东西 flask中的session是经过加密之后存储在cookie中的
                session['user_id'] = user.id
                return redirect(url_for('author.login'))
            else:
                print('密码错误')
                return redirect(url_for('author.login'))
        else:
            print(form.errors)
            return redirect(url_for('author.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect('/author/login')
        else:
            print(form.errors)
            return '失败'
    # 验证用户提交的邮箱合法以及验证码验证是否正确
    # 表单验证：flask-wtf


@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    message = Message(subject='破解版支符宝验证码', recipients=['13829233106@163.com'],
                      body=f'您的验证码是：{captcha}，请勿泄露。')
    mail.send(message)
    # 服务器验证码存储 memcached/redis/数据库存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', 'data': None})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/mail_test')
def mail_test():
    message = Message(subject='邮箱测试', recipients=['13829233106@163.com'], body='这是测试邮件zp')
    mail.send(message)
    return '发送成功'
