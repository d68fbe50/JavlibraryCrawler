import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from javlibrary_crawler.spiders.actors_spider import ActorsSpider
import dbop.mysql_op as mysql_op
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME


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


if __name__ == "__main__":
    # 初始化数据库
    db_init()
    main()
    pass
