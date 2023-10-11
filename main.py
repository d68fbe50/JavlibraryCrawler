import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from javlibrary_crawler.spiders.actors_spider import ActorsSpider

from tqdm import tqdm


def main():
    print("hello")
    process = CrawlerProcess(get_project_settings())
    process.crawl(WorksSpider)
    # process.crawl(ActorsSpider)
    # download_preview.download()
    process.start()

    pass


if __name__ == "__main__":
    main()
    pass
