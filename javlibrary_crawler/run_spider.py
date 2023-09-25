import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.javlibrary_spider import JavlibrarySpider

from javlibrary_crawler.spiders.actor_spider import ActorSpider


def main():
    # 删除现有的 output.xlsx 文件
    if os.path.exists('output.xlsx'):
        os.remove('output.xlsx')
    process = CrawlerProcess(get_project_settings())
    # process.crawl(ActorSpider)
    process.crawl(JavlibrarySpider)
    process.start()


if __name__ == '__main__':
    main()
