import pymysql
def init_mysql():
    # 连接参数
    host_name = 'localhost'
    port_num = 3306
    user_name = 'root'
    password = 'Lindesong7758?'

    # 建立连接
    connection = pymysql.connect(host=host_name, port=port_num, user=user_name, password=password)
    cursor = connection.cursor()

    # 查询数据库
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    database_exists = any(db == ('javcraw',) for db in databases)

    # 检查是否存在 javcraw 数据库
    if not database_exists:
        # 如果不存在，则创建
        print(database_exists)
        cursor.execute("CREATE DATABASE javcraw;")
        print("🎉 已成功创建 javcraw 数据库!")
    else:
        print("✨ javcraw 数据库已经存在!")
    cursor.close()
    connection.close()
