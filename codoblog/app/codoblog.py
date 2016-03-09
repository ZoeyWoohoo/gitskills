# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, url_for, flash
from flask import request,redirect
from flask.ext.script import Manager
from flask.ext.script import Shell #为启动shell会话自动导入特定的对象（数据库实例和模型）
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.mail import Mail, Message
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand #数据库的更新与迁移
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from datetime import datetime
import os
from threading import Thread #异步发送电子邮件，避免处理请求过程中不必要的延迟

app = Flask(__name__)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.config['SECRET_KEY'] = '123456789' 
#配置变量的通用密钥，必须要保证其他人不知道你所用的字符串，最后从环境变量中导入

app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:examplekey@localhost/User'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#数据库的一些配置，这里用的是mysql 

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'example@qq.com' #os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = '#################' #os.environ.get('MAIL_PASSWORD') 最好从环境变量中导入
# app.config['MAIL_DEBUG'] = True
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'example@qq.com'
app.config['FLASKY_ADMIN'] = 'example@qq.com'   #os.environ.get('FLASKY_ADMIN')
#邮箱的一些配置，这里用的是qq邮箱


class NameForm(Form):
	name = StringField('what is your name,bitch?', validators=[Required()])
	submit = SubmitField('Submit')
#这里定义的是表单

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')
    
    def __repr__(self):
    	return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique = True, nullable = False)
    # phonenumber = db.Column(db.Integer, unique = True, nullable = False)
    # blogkey = db.Column(db.String(250), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
    	return '<User %r>' % self.username
#这里定义的是两个数据库表的模型


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))
#为启动shell会话自动导入特定的对象（数据库实例和模型）

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to,subject,template,**kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app,msg])
	thr.start()
	return thr
#定义的一个发送电子邮件的函数(此处经改动，为异步发送)



@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
			flash('Looks like you are a new guy,right?')
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known',False))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	manager.run()
