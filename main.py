import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from javlibrary_crawler.spiders.magnet_spider import MagnetSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
import dbop.mysql_op as mysql_op
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME
from preview_download import download_preview as pdown
from config import arguments


def main():
    # 创建一个CrawlerProcess
    process = CrawlerProcess(get_project_settings())

    # 当WorksSpider爬虫关闭时，启动MagnetSpider
    def on_spider_closed(spider, reason):
        if spider.name == arguments.works_spidername:  # 这里假设你的WorksSpider的名字是'works_spider'
            process.crawl(MagnetSpider)

    dispatcher.connect(on_spider_closed, signal=signals.spider_closed)

    # 先启动WorksSpider
    process.crawl(WorksSpider)

    # 开始事件循环
    process.start()


def db_init():
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()
    mysql_op.init_db(cursor, MYSQL_DBNAME)


def download_preview(start_date, end_date):
    pdown.download(start_date, end_date)


if __name__ == "__main__":
    # 是否初始化数据库
    db_init()
    main()
    # 下载预览图
    # 你可以在这里定义所需的日期范围
    # start_date = "2023-08-01"
    # end_date = "2023-12-19"
    # download_preview(start_date, end_date)
    pass
