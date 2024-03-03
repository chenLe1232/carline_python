from peewee import *
from playhouse.db_url import connect
from playhouse.migrate import *
from jobs import *
import os

# 连接数据库
# 为了安全 账号密码写在环境变量中 从环境变量中获取账号密码
password = os.environ.get('MyPASSWORD1')
table_name = os.environ.get('MYSQL_TABLE_NAME')
host = os.environ.get('MYSQL_HOST')
port = os.environ.get('MYSQL_PORT')
user_name = os.environ.get('MYSQL_USER_NAME')
print(f'mysql://{user_name}:{password}@{host}:{port}/{table_name}')
if not password:
    raise ValueError('MYSQL_PASSWORD is not set')
if not password:
    raise ValueError('MYSQL_PASSWORD is not set')
db = connect(f'mysql://{user_name}:{password}@{host}:{port}/{table_name}')


class User(Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(null=True)  # 添加 email 属性
    # status, running, success, failed wait
    status = CharField(default='wait')

    class Meta:
        database = db  # 这个模型使用 "db" 作为数据库连接
        db_table = 'users'  # 指定数据库中的表名


# 创建一个 migrator 对象
migrator = MySQLMigrator(db)

# 定义要添加的字段
email_field = CharField(null=True)

# 判断字段是否存在 不存在则添加 存在则不做任何操作
if not User.table_exists():
    db.create_tables([User])

# 获取 'users' 表中所有的列
columns = [column.name for column in db.get_columns('users')]

# 如果 'email' 列不存在，添加 'email' 列
if 'email' not in columns:
    migrate(
        migrator.add_column('users', 'email', email_field)
    )

# 如果 'status' 列不存在，添加 'status' 列 并且设置默认值为 'wait'
if 'status' not in columns:
    migrate(
        migrator.add_column('users', 'status', CharField(default='wait'))
    )
