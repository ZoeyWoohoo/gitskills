import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = "123456789"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'example@qq.com'
	FLASKY_ADMIN = 'example@qq.com'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.qq.com'
	MAIl_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'example@qq.com' #os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = '##############' #os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = 'mysql://root:examplekey@localhost/User'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:examplekey@localhost/User'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:examplekey@localhost/User'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}