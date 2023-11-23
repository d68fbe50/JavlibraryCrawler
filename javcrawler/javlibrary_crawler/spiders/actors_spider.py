import scrapy
from javlibrary_crawler.items import ActorItem
from config import arguments
import string


class ActorsSpider(scrapy.Spider):
    name = arguments.actor_spidername
    base_url = 'https://www.javlibrary.com/en/star_list.php?prefix={prefix}&page={page}'

    def __init__(self, *args, **kwargs):
        super(ActorsSpider, self).__init__(*args, **kwargs)
        # 为每个大写字母生成起始URL
        self.start_urls = [self.base_url.format(prefix=letter, page=1) for letter in string.ascii_uppercase]

    def parse(self, response):
        # 解析演员数据
        for div in response.xpath('//div[@class="starbox"]/div[@class="searchitem"]'):
            item = ActorItem()
            item['actor_name'] = div.xpath('./a/text()').get()
            item['actor_id'] = div.xpath('@id').get()
            yield item

        # 解析最后一页的数字
        last_page_num = int(response.xpath('//a[@class="page last"]/@href').re(r'page=(\d+)')[0])

        # 获取当前字母的prefix和当前页码
        current_prefix = response.url.split('prefix=')[-1].split('&')[0]
        current_page = int(response.url.split('page=')[-1])

        # 如果当前页不是最后一页，则生成后续页面的请求
        if current_page < last_page_num:
            next_page = current_page + 1
            print(f"Current Page {current_page}, Total Page {last_page_num}")
            yield scrapy.Request(url=self.base_url.format(prefix=current_prefix, page=next_page), callback=self.parse)
