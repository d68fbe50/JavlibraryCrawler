"""
动作和操作代码：负责具体的功能实现，如数据库操作、爬虫启动等
"""

import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME
from preview_download import download_preview as pdown
import dbop.mysql_op as mysql_op


class CrawlerActions:
    def __init__(self, app):
        self.app = app

    def db_init(self):
        self.app.log("正在初始化数据库...")
        # ...[数据库初始化代码]...
        try:
            connection = pymysql.connect(**MYSQL_CONFIG)
            cursor = connection.cursor()
            mysql_op.init_db(cursor, MYSQL_DBNAME)
            self.app.log("数据库初始化成功！")
        except pymysql.err.OperationalError as e:
            self.app.log("错误: 请先配置数据库信息！")

    def start_crawl(self):
        self.app.log("开始爬取...")

        # 你的爬虫启动代码...
        process = CrawlerProcess(get_project_settings())
        process.crawl(WorksSpider)
        process.start()
        self.app.log("爬取完成！请重启此程序")

    def download_preview(self):
        self.app.log("开始下载预览图...")

        # 你的预览图下载代码...
        start_date = "2023-08-01"
        end_date = "2023-12-19"
        pdown.download(start_date, end_date)
        self.app.log("预览图下载完成！")
