# 配置相关文件

SECRET_KEY = 'GHBNDmoiivfjfon'

# 数据库的配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'test_oa'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
# 是否需要进行加密
MAIL_USE_SSL = True
MAIL_PORT = 465
# 邮箱账号
MAIL_USERNAME = '2037259841@qq.com'
# 授权码
MAIL_PASSWORD = 'brbcqwepazsecfdd'
# 邮箱账号
MAIL_DEFAULT_SENDER = '2037259841@qq.com'

REDIS_URL = "redis://localhost:6379/0"
