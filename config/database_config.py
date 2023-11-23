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
    "host": "localhost",
    "user": "root",
    "password": "070011",
    "charset": "utf8mb4",
    "database": MYSQL_DBNAME,
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_redis_config():
    """
    获取Redis服务器的配置参数。

    Returns:
        dict: 包含Redis服务器配置参数的字典。
    """
    return REDIS_CONFIG


def get_mysql_config():
    """
    获取Mysql服务器的配置参数。

    Returns:
        dict: 包含Mysql服务器配置参数的字典。
    """
    return MYSQL_CONFIG


if __name__ == "__main__":
    # 调用重新创建表的函数
    pass
