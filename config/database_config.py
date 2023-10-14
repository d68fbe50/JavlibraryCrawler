import pymysql
import dbop.mysql_op as mysql_op

REDIS_CONFIG = {
    # 配置redis参数
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": "",
}

MYSQL_DBNAME = "javcrawer"
MYSQL_CONFIG = {
    "host": 'localhost',
    "user": 'root',
    "password": 'Lindesong7758?',
    "charset": 'utf8mb4',
    # "database": MYSQL_DBNAME,
    "cursorclass": pymysql.cursors.DictCursor
}

if __name__ == "__main__":
    # 调用重新创建表的函数
    # mysql_op.drop_database("javcrawer")
    mysql_op.init_db(MYSQL_DBNAME)
    pass
