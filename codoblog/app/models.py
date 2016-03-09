# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin #AnonymousUserMixin  可实现用户认证的大多数需求
from . import db
from . import login_manager
from flask.ext.login import login_required #为了保护路由只让认证用户访问，Flask-login提供的一个修饰器

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
#引入使用itsdangerous生成确认令牌

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#加载用户的回调函数，如果能找到用户，返回用户对象，否则返回None

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique = True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    #这个函数生成一个令牌，有效期默认为一个小时

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
    #这个函数检验令牌，如果检验通过，则把新添加的confirmed属性设为True

    @property
    def password(self):
    	raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
    	self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
    	return check_password_hash(self.password_hash, password)

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(permissions=0xff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()

    # def can(self, permissions):
    #     return self.role is not None and (self.role.permissions & permissions) == permissions

    # def is_administrator(self):
    #     return self.can(permissions.ADMINISTER)

# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False

#     def is_administrator(self):
#         return False

# login_manager.anonymous_user = AnonymousUser

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64),unique = True)

    # default = db.Column(db.Boolean, default=False, index=True)
    # permissions = db.Column(db.Integer)
    #新加的两项用以区分角色，权限

    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    # @staticmethod
    # def insert_roles():
    #     roles = {
    #     'User': (Permission.FOLLOW|Permission.COMMIT|Permission.WRITE_ARTICLES, True),
    #     'Moderator': (Permission.FOLLOW|Permission.COMMIT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS, False),
    #     'Administrator': (0xff, False)
    #     }
    #     for r in roles:
    #         role = Role.query.filter_by(name=r).first()
    #         if role is None:
    #             role = Role(name=r)
    #         role.permissions = roles[r][0]
    #         role.default = roles[r][1]
    #         db.session.add(role)
    #     db.sessioncommit()

# class Permission:
#     FOLLOW = 0x01  #关注其他用户
#     COMMIT = 0x02  #在别人文章下发表评论
#     WRITE_ARTICLES = 0x04  #写原创文章
#     MODERATE_COMMENTS = 0x08  #查处不当言论
#     ADMINISTER = 0x80  #管理网站（管理员权限）
    #定义的一些角色权限