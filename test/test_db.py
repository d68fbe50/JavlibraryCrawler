import pymysql
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME


def connect_mysql():
    # 连接到MySQL数据库
    connection = pymysql.connect(**MYSQL_CONFIG)
    try:
        cursor = connection.cursor()
        db_exist = cursor.execute("SHOW DATABASES LIKE %s", MYSQL_DBNAME)
        if not db_exist:
            cursor.execute("create database javcrawer;")
        cursor.execute("use javcrawer")

    finally:
        connection.close()


if __name__ == "__main__":
    connect_mysql()
