def recreate_table(cursor):
    # 使用新创建的数据库
    cursor.execute("USE javcrawer")

    # 检查表是否存在，如果存在则删除
    drop_table(cursor, "actor")
    drop_table(cursor, "works")

    # 创建 'spider' 和 'actor' 表
    create_works_table(cursor)
    create_actor_table(cursor)

def create_works_table(cursor):
    cursor.execute("""
    CREATE TABLE works(
        id INT AUTO_INCREMENT PRIMARY KEY,
        serial_number VARCHAR(255) UNIQUE,
        title TEXT,
        actor_id TEXT,
        release_date DATE,
        comments INT,
        reviews INT,
        preview TEXT,
        link TEXT,
        maker VARCHAR(255),
        length INT,
        director VARCHAR(255),
        label VARCHAR(255),
        user_rating FLOAT,
        genres TEXT,  -- 新添加的字段
        cast TEXT,     -- 新添加的字段
        magnet_link TEXT
    )
    """)
    print(f"create table: works")


def create_actor_table(cursor):
    cursor.execute("""
    CREATE TABLE actor(
        id INT AUTO_INCREMENT PRIMARY KEY,
        actor_id VARCHAR(255) UNIQUE,
        actor_name TEXT
    )
    """)
    print(f"create table: actor")


def init_db(cursor, db_name):
    """
    :param db_name:database name
    :return:
    """

    # 检查数据库是否存在
    db_exists = cursor.execute("SHOW DATABASES LIKE %s", db_name)
    if not db_exists:
        # 如果数据库不存在，则创建数据库
        print(f"database: {db_name} not exists.")
        create_db(cursor, db_name)
        print(f"create database: {db_name}")
    else:
        drop_database(cursor, db_name)
        print(f"drop database: {db_name}")
        create_db(cursor, db_name)
        print(f"create database: {db_name}")
    cursor.execute(f"USE {db_name}")
    recreate_table(cursor)


def create_db(cursor, db_name):
    """
    :param db_name:database name
    :param cursor:db cursor
    :return:
    """

    # 检查数据库是否存在
    db_exists = cursor.execute("SHOW DATABASES LIKE %s", db_name)
    if not db_exists:
        # 如果数据库不存在，则创建数据库
        cursor.execute(f"CREATE DATABASE {db_name};")
    else:
        print(f"Database: {db_name} already exists!")


def drop_database(cursor, db_name):
    """
    :param db_name:database name
    :return:
    """
    # 删除数据库
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")


def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"drop table: {table_name}")
