import redis
import pymysql
from config.database_config import REDIS_CONFIG, MYSQL_CONFIG
from config import arguments
from utils.get_magnet_from_U3C3 import fliter_by_size, size_to_float
from collections import defaultdict
from dbop import mysql_op as db


# from utils.get_magnet_from_U3C3 import get_magnet, fliter_by_size


class MySQLPipeline:
    def __init__(self):
        self.items_dict = defaultdict(list)

    def open_spider(self, spider):
        # 连接到MySQL数据库
        self.connection = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.connection.cursor()
        self.cursor.execute("use javcrawer")
        self.items_list = []

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
                # 定义列名的列表和对应的item键的列表
                columns = db.columns
                item_keys = db.item_keys

                # 使用列表解析生成插入和更新的SQL语句部分
                columns_str = ', '.join(columns)
                placeholders = ', '.join(['%s'] * len(columns))
                update_str = ', '.join([f"{col} = VALUES({col})" for col in columns])

                # 使用列表解析从item中获取数据
                values = [item.get(key, '') for key in item_keys]

                # 生成并执行SQL语句
                sql = f"""
                    INSERT INTO works({columns_str}) 
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE
                    {update_str}
                """
                cursor.execute(sql, values)
            if spider.name == arguments.magnet_spidername:
                serial_number = item['SerialNumber']
                self.items_dict[serial_number].append(item)
            # 提交数据到数据库
            self.connection.commit()
        return item

    def close_spider(self, spider):
        """
        当spider关闭时执行的方法。
        该方法用于关闭数据库连接。
        """
        # lists = self.items_list
        # ft = fliter_by_size(lists, 0, 5)
        # print(ft)
        # print("#" * 20)
        self.update_magnet()
        self.connection.close()

    def update_magnet(self):
        for serial_number, items in self.items_dict.items():
            # 取得大小范围内的magnet对象
            ft = self.fliter_by_size(items, arguments.magnet_file[0], arguments.magnet_file[1])
            if ft:
                max_ft = self.get_max_size_item(ft)
                # print(max_ft['SerialNumber'], max_ft["Size"], max_ft["MagnetLink"])
                self.cursor.execute("DESCRIBE works;")
                self.cursor.execute("""
                INSERT INTO works(serial_number, magnet_link)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                magnet_link=VALUES(magnet_link)
                """, (max_ft['SerialNumber'], max_ft["MagnetLink"]))
                # 提交更新
                self.connection.commit()
            else:
                print(f"{serial_number} None")

    def fliter_by_size(self, lists, min_size, max_size):
        # 过滤出给定大小范围内的对象
        filtered_list = [item for item in lists if min_size <= size_to_float(item['Size']) <= max_size]
        if filtered_list:
            return filtered_list
        return None

    def get_max_size_item(self, items):
        return max(items, key=lambda x: size_to_float(x['Size']))


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
