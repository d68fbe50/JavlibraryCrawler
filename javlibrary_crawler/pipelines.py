import redis
import pymysql
from config.database_config import REDIS_CONFIG, MYSQL_CONFIG, MYSQL_DBNAME
from config import arguments


class MySQLPipeline:
    def open_spider(self, spider):
        # 连接到MySQL数据库
        self.connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = self.connection.cursor()
        cursor.execute("use javcrawer")

    def process_item(self, item, spider):
        """
        对每个提取的item进行处理的方法。
        该方法根据spider的名称将数据保存到相应的数据库表中。
        """
        with self.connection.cursor() as cursor:
            # 如果是 ActorSpider，将数据保存到 'actor' 表
            if spider.name == arguments.actor_spidername:
                cursor.execute("""
                INSERT INTO actor(actor_id, actor_name) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE 
                actor_name = VALUES(actor_name)
                """, (item['actor_id'], item.get('actor_name', '')))
            # 如果是 JavlibrarySpider，将数据保存到 'spider' 表
            if spider.name == arguments.works_spidername:
                cursor.execute("""
                    INSERT INTO works(title, actor_id, serial_number, release_date, comments, reviews, link, preview, maker, length, director, label, user_rating, genres, cast) 
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


class RedisPipeline:
    def close_spider(self, spider):
        """
        当spider关闭时执行的方法。
        用于关闭Redis连接。
        """
        self.redis.close()

    def process_item(self, item, spider):
        """
        对每个提取的item进行处理的方法。
        根据spider的名称将数据保存到相应的Redis数据结构中。
        """
        if spider.name == "actors_spider":
            # 切换到 db1
            self.redis.select(1)
            # print(f"Save {item['actor_name']} to Redis...")
            self.redis.hmset(item["actor_id"], {"actor_name": item["actor_name"]})
        elif spider.name == "works_spider":
            # 切换到 db0
            self.redis.select(0)
            # print(f"Save {item['serial_number']} to Redis...")
            self.redis.hmset(
                item["serial_number"],
                {
                    "type": "work",
                    "title": str(item["title"]),
                    "actor_id": str(item.get("actor_id", "")),
                    "release_date": str(item["release_date"]),
                    "comments": str(item["comments"]),
                    "reviews": str(item["reviews"]),
                    "link": str(item["link"]),
                    "preview": str(item["preview"]),
                    "maker": str(item["maker"]),
                    "length": str(item["length"]),
                    "director": str(item["director"]),
                    "label": str(item["label"]),
                    "user_rating": str(item["user_rating"]),
                    "genres": str(item["genres"]),
                    "cast": str(item["cast"]),
                },
            )

        return item

    def open_spider(self, spider):
        # 连接到Redis数据库
        self.redis = redis.Redis(**REDIS_CONFIG)
