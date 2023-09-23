from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.javlibrary_spider import JavlibrarySpider
from javlibrary_crawler.spiders.actor_spider import ActorSpider


def main():
    process = CrawlerProcess(get_project_settings())
    # process.crawl(ActorSpider)
    process.crawl(JavlibrarySpider)
    process.start()


if __name__ == '__main__':
    main()
