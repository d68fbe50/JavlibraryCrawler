import redis
from javlibrary_crawler.redis_config import REDIS_CONFIG


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
