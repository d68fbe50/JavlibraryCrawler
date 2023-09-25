import pymysql
import sqlite3
from javlibrary_crawler.arguments import db_path

import pandas as pd


class ExcelExportPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        print("xxxx" * 100)
        df.to_excel('output.xlsx', index=False)


class MySQLPipeline:
    def recreate_table(self):
        with self.connection.cursor() as cursor:
            # 使用新创建的数据库
            cursor.execute("USE javcraw")

            # 检查'spider'表是否存在，如果存在则删除
            cursor.execute("DROP TABLE IF EXISTS spider")
            cursor.execute("DROP TABLE IF EXISTS actor")

            # 创建 'spider' 和 'actor' 表
            self.create_spider_table(cursor)
            self.create_actor_table(cursor)

    def create_spider_table(self, cursor):
        cursor.execute("""
        CREATE TABLE spider (
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
            cast TEXT     -- 新添加的字段
        )
        """)

    def create_actor_table(self, cursor):
        cursor.execute("""
        CREATE TABLE actor(
            id INT AUTO_INCREMENT PRIMARY KEY,
            actor_id VARCHAR(255) UNIQUE,
            actor_name TEXT
        )
        """)

    def open_spider(self, spider):
        # 连接到MySQL数据库
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Lindesong7758?',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # 需要更改表的结构或者重新创建表
        # self.recreate_table()

    def process_item(self, item, spider):
        """
        对每个提取的item进行处理的方法。
        该方法根据spider的名称将数据保存到相应的数据库表中。
        """
        with self.connection.cursor() as cursor:
            # 如果是 ActorSpider，将数据保存到 'actor' 表
            if spider.name == 'actor_spider':
                cursor.execute("""
                INSERT INTO actor(actor_id, actor_name) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE 
                actor_name = VALUES(actor_name)
                """, (item['actor_id'], item.get('actor_name', '')))
            # 如果是 JavlibrarySpider，将数据保存到 'spider' 表
            if spider.name == 'javlibrary':
                cursor.execute("""
                    INSERT INTO spider (title, actor_id, serial_number, release_date, comments, reviews, link, preview, maker, length, director, label, user_rating, genres, cast) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    actor_id = VALUES(actor_id),
                    release_date = VALUES(release_date),
                    comments = VALUES(comments),
                    reviews = VALUES(reviews),
                    link = VALUES(link),
                    preview = VALUES(preview),
                    maker = VALUES(maker),
                    length = VALUES(length),
                    director = VALUES(director),
                    label = VALUES(label),
                    user_rating = VALUES(user_rating),
                    genres = VALUES(genres),
                    cast = VALUES(cast)
                """, (
                    item['title'],
                    item.get('actor_id', ''),
                    item['serial_number'],
                    item['release_date'],
                    item['comments'],
                    item['reviews'],
                    item['link'],
                    item['preview'],
                    item['maker'],
                    item['length'],
                    item['director'],
                    item['label'],
                    item['user_rating'],
                    item['genres'],
                    item['cast']
                ))

            # 提交数据到数据库
            self.connection.commit()

        return item

    def close_spider(self, spider):
        """
        当spider关闭时执行的方法。
        该方法用于关闭数据库连接。
        """
        self.connection.close()


class SQLitePipeline:
    def recreate_table(self):
        cursor = self.connection.cursor()
        # 删除存在的'spider'和'actor'表
        cursor.execute("DROP TABLE IF EXISTS spider")
        cursor.execute("DROP TABLE IF EXISTS actor")

        # 创建 'spider' 和 'actor' 表
        self.create_spider_table(cursor)
        self.create_actor_table(cursor)

    def create_spider_table(self, cursor):
        cursor.execute("""
        CREATE TABLE spider (
            id INTEGER PRIMARY KEY,
            serial_number TEXT UNIQUE,
            title TEXT,
            actor_id TEXT,
            release_date TEXT,
            comments INTEGER,
            reviews INTEGER,
            preview TEXT,
            link TEXT,
            maker TEXT,
            length INTEGER,
            director TEXT,
            label TEXT,
            user_rating REAL,
            genres TEXT,
            cast TEXT
        )
        """)

    def create_actor_table(self, cursor):
        cursor.execute("""
        CREATE TABLE actor(
            id INTEGER PRIMARY KEY,
            actor_id TEXT UNIQUE,
            actor_name TEXT
        )
        """)

    def open_spider(self, spider):
        self.connection = sqlite3.connect(db_path)
        # 需要更改表的结构或者重新创建表
        # self.recreate_table()

    def process_item(self, item, spider):
        """
        对每个提取的item进行处理的方法。
        该方法根据spider的名称将数据保存到相应的数据库表中。
        """
        cursor = self.connection.cursor()

        # 如果是 ActorSpider，将数据保存到 'actor' 表
        if spider.name == 'actor_spider':
            cursor.execute("""
            INSERT OR IGNORE INTO actor(actor_id, actor_name) 
            VALUES (?, ?)
            """, (item['actor_id'], item.get('actor_name', '')))

        # 如果是 JavlibrarySpider，将数据保存到 'spider' 表
        if spider.name == 'javlibrary':
            cursor.execute("""
                INSERT OR REPLACE INTO spider (title, actor_id, serial_number, release_date, comments, reviews, link, preview, maker, length, director, label, user_rating, genres, cast) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['title'],
                item.get('actor_id', ''),
                item['serial_number'],
                item['release_date'],
                item['comments'],
                item['reviews'],
                item['link'],
                item['preview'],
                item['maker'],
                item['length'],
                item['director'],
                item['label'],
                item['user_rating'],
                item['genres'],
                item['cast']
            ))

        self.connection.commit()
        return item

    def close_spider(self, spider):
        """
        当spider关闭时执行的方法。
        该方法用于关闭数据库连接。
        """
        self.connection.close()
