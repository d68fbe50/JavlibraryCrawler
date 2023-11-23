import scrapy
from scrapy.crawler import CrawlerProcess
import pymysql
from config.database_config import MYSQL_CONFIG
from javlibrary_crawler.items import MagnetItem
from config import database_config as db


class MagnetSpider(scrapy.Spider):
    name = "magnet_spider"
    base_url = "https://u3c3.com/?search2=eelja3lfea&search={}"
    custom_settings = {
        'ITEM_PIPELINES': {
            'javlibrary_crawler.pipelines.MySQLPipeline': 1,
        },
    }

    def __init__(self, *args, **kwargs):
        super(MagnetSpider, self).__init__(*args, **kwargs)

        self.connection = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"use {db.MYSQL_DBNAME}")
        self.cursor.execute("SELECT serial_number FROM works")
        self.serial_numbers = [item['serial_number'] for item in self.cursor.fetchall()]

    def start_requests(self):
        for serial_number in self.serial_numbers:
            yield scrapy.Request(url=self.base_url.format(serial_number), callback=self.parse,
                                 meta={'serial_number': serial_number})

    def parse(self, response):
        for row in response.css('tr.default'):
            # 提取每个td里的数据
            tds = row.css('td')
            serial_number = response.meta['serial_number']

            # 提取MagnetLink
            magnet_link = tds[2].css('.fa.fa-fw.fa-magnet').xpath('..').xpath('@href').get()

            # 提取Pikpak链接
            pikpak_link = tds[5].css('a[href^="https://mypikpak.com/drive/"]::attr(href)').get()

            # 提取Size值
            size = tds[3].css('::text').get().strip()

            # 提取上传日期
            upload_date = tds[4].css('::text').get().strip()

            # 构造结果
            item = MagnetItem()
            item['SerialNumber'] = serial_number
            item['MagnetLink'] = magnet_link
            item['Pikpak'] = pikpak_link
            item['Size'] = size
            item['UploadDate'] = upload_date

            yield item

    # 关闭数据库连接
    def closed(self, reason):
        self.cursor.close()
        self.connection.close()


# 运行爬虫
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MagnetSpider)
    process.start()
