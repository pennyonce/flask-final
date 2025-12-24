from flask import Blueprint, render_template, jsonify, redirect, url_for, session, current_app
from exts import mail, db, flask_redis
from flask_mail import Message
from flask import request
import string
import random
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
            code = request.form.get('captcha')
            key = f'verify_code:{email}'
            try:
                stored_code = flask_redis.get(key)
                # 验证码不存在或者过期
                if not stored_code:
                    return jsonify({'result': False, 'message': '验证码已过期或不存在'}), 400
                if stored_code.decode('utf-8') != code:
                    return jsonify({'result': False, 'message': '验证码错误'})

                user = UserModel(email=email, username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flask_redis.delete(key)
                return redirect('/author/login')
            except Exception as e:
                current_app.logger.error(f'验证错误:{str(e)}')
                return jsonify({'result': False, 'message': '系统错误请重试'})
        else:
            print(form.errors)
            return '失败'
    # 验证用户提交的邮箱合法以及验证码验证是否正确
    # 表单验证：flask-wtf


@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')
    if not email:
        return jsonify({'result': False, 'message': '请输入邮箱！'})
    # 生成验证码
    source = string.digits * 4
    code = ''.join(random.sample(source, 4))
    print(code)
    message = Message(
        subject='破解版吱符宝注册验证码',
        recipients=[email],
        body=f'验证码为:{code},一分钟有效',
    )
    key = f'verify_code:{email}'
    try:
        flask_redis.setex(key, 60, code)
        mail.send(message)
        print(f'【模拟】发送验证码{code}到邮箱{email}')
        return jsonify({'result': True,
                        'message': '验证码发送成功！'})
    except Exception as e:
        current_app.logger.error(f'发送验证码时redis错误:{e}')
        return jsonify({'result': False, 'message': '系统错误请重试'}), 500


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/mail_test')
def mail_test():
    message = Message(subject='邮箱测试', recipients=['13829233106@163.com'], body='这是测试邮件zp')
    mail.send(message)
    return '发送成功'
