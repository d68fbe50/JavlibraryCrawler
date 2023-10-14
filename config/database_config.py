import pymysql

# 以下是Redis服务器的设置
REDIS_CONFIG = {
    # 配置redis参数
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": "",
}

# 以下是Mysql服务器的设置
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
    pass
