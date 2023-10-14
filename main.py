import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from javlibrary_crawler.spiders.actors_spider import ActorsSpider
import dbop.mysql_op as mysql_op
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME
from preview_download import download_preview as pdown


def main():
    print("hello")
    process = CrawlerProcess(get_project_settings())
    process.crawl(WorksSpider)
    # process.crawl(ActorsSpider)
    # download_preview.download()
    process.start()

    pass


def db_init():
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()
    mysql_op.init_db(cursor, MYSQL_DBNAME)


def download_preview():
    # 你可以在这里定义所需的日期范围
    start_date = "2023-08-01"
    end_date = "2023-12-19"
    pdown.download(start_date, end_date)


if __name__ == "__main__":
    # 初始化数据库
    db_init()
    main()
    # 下载预览图
    download_preview()
    pass
