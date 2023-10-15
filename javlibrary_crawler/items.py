# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkSpider(scrapy.Item):
    preview = scrapy.Field()
    title = scrapy.Field()
    actor_id = scrapy.Field()
    release_date = scrapy.Field()
    serial_number = scrapy.Field()
    comments = scrapy.Field()
    reviews = scrapy.Field()
    link = scrapy.Field()
    maker = scrapy.Field()
    id = scrapy.Field()
    length = scrapy.Field()
    director = scrapy.Field()
    label = scrapy.Field()
    user_rating = scrapy.Field()
    genres = scrapy.Field()
    cast = scrapy.Field()
    magnet = scrapy.Field()

    def parse(self, response):
        # 处理响应的逻辑
        pass


class ActorItem(scrapy.Item):
    actor_name = scrapy.Field()
    actor_id = scrapy.Field()

    def parse(self, response):
        # 处理响应的逻辑
        pass


# items.py


class MagnetItem(scrapy.Item):
    SerialNumber = scrapy.Field()
    MagnetLink = scrapy.Field()
    Pikpak = scrapy.Field()
    Size = scrapy.Field()
    UploadDate = scrapy.Field()
