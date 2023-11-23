import re

import scrapy
from javlibrary_crawler.items import WorkSpider
from config import arguments
from config.arguments import ids as ids


class WorksSpider(scrapy.Spider):
    name = arguments.works_spidername
    base_url_template = (
        "https://www.javlibrary.com/cn/vl_star.php?list&mode=2&s={actor_id}&page={page}"
    )
    items_dict = {}
    custom_settings = {
        'ITEM_PIPELINES': {
            'javlibrary_crawler.pipelines.MySQLPipeline': 1,
        },
    }

    def __init__(self):
        super(WorksSpider, self).__init__()
        # 禁用控制台输出
        # logging.getLogger("scrapy").setLevel(logging.CRITICAL)

    def start_requests(self):
        actor_ids = ids

        for actor_id in actor_ids:
            yield scrapy.Request(
                url=self.base_url_template.format(actor_id=actor_id, page=1),
                callback=self.parse_pagination,
                meta={
                    "base_url": self.base_url_template.format(
                        actor_id=actor_id, page="{}"
                    ),
                },
            )

    def parse_pagination(self, response):
        # 先解析当前页的数据（第一页）
        for item in self.parse_page_data(response):
            yield item

        base_url = response.meta["base_url"]
        # 解析最后一页的数字
        last_page = response.xpath('//a[@class="page last"]/@href').re(r"page=(\d+)")
        last_page_num = int(last_page[0] if last_page else 1)

        # 使用for循环生成每一页的URL，并使用parse方法爬取数据
        for page in range(2, last_page_num + 1 if arguments.recent is -1 else arguments.recent):
            yield scrapy.Request(url=base_url.format(page), callback=self.parse)

    def parse(self, response):
        for item in self.parse_page_data(response):
            yield item

    def parse_preview(self, response):

        item = WorkSpider()
        item["actor_id"] = response.meta["actor_id"]

        # ID 或 serial_number
        serial_number_result = response.xpath(
            '//div[@id="video_id"]/table//td[@class="text"]/text()'
        ).get()
        item["serial_number"] = (
            serial_number_result.strip() if serial_number_result else None
        )

        # title
        title_result = response.xpath(
            '//div[@id="video_title"]/h3[@class="post-title text"]/a/text()'
        ).get()
        item["title"] = title_result.strip() if title_result else None

        # Release Date
        release_date_result = response.xpath(
            '//div[@id="video_date"]/table//td[@class="text"]/text()'
        ).get()
        item["release_date"] = (
            release_date_result.strip() if release_date_result else None
        )

        # Length
        length_text_result = response.xpath(
            '//div[@id="video_length"]/table//td/span[@class="text"]/text()'
        ).get()
        item["length"] = int(length_text_result.strip()) if length_text_result else None

        # Director
        director_result = response.xpath(
            '//div[@id="video_director"]//td[@class="text"]/text()'
        ).get()
        item["director"] = director_result.strip() if director_result else "Unknown"

        # Maker
        maker_result = response.xpath(
            '//div[@id="video_maker"]//td[@class="text"]/span[@class="maker"]/a/text()'
        ).get()
        item["maker"] = maker_result.strip() if maker_result else "Unknown"

        # Label
        label_result = response.xpath(
            '//div[@id="video_label"]//td[@class="text"]/span[@class="label"]/a/text()'
        ).get()
        item["label"] = label_result.strip() if label_result else "Unknown"

        # User Rating
        rating_text_result = response.xpath(
            '//div[@id="video_review"]/table//td[@class="text"]/span[@class="score"]/text()'
        ).get()
        if rating_text_result:
            rating_text = rating_text_result.strip()
            item["user_rating"] = float(rating_text.replace("(", "").replace(")", ""))
        else:
            item["user_rating"] = None

        # Genre(s)
        genres = response.xpath(
            '//div[@id="video_genres"]/table//td[@class="text"]/span/a/text()'
        ).getall()
        item["genres"] = ", ".join(genres)

        # Cast
        cast_result = response.xpath(
            '//div[@id="video_cast"]/table//td[@class="text"]/span/span/a/text()'
        ).getall()
        item["cast"] = ", ".join(cast_result)

        # Link (如果需要的话，这里是完整的URL)
        item["link"] = response.url

        # 从response中提取图片的src
        preview_result = response.xpath('//div[@id="video_jacket"]/img/@src').get()
        item["preview"] = preview_result.strip() if preview_result else None

        # Initialize comments and reviews to 0 as they weren't extracted in the example provided
        item["comments"] = response.meta["comments"]
        item["reviews"] = response.meta["reviews"]

        # Online MissAV
        item["online_missav"] = "https://missav.com/dm44/cn/" + serial_number_result

        yield item

    def parse_magnet(self, response):
        # 提取item["serial_number"]
        item = response.meta['item']
        serial_number = item["serial_number"]
        magnet_spider_url = response.meta['magnet_spider_url']
        print(magnet_spider_url)
        # 从响应文本中提取所有带有magnet链接的内容
        print(response.text)
        magnet_links = re.findall(r'magnet:\?xt=urn:btih[^\'"\s]+', response.text)
        print(magnet_links)
        # 处理提取到的链接
        yield item
        pass

    def parse_magnet_spider(self, response):
        item = response.meta['item']

        # 从响应文本中提取所有带有magnet链接的内容
        magnet_links = re.findall(r'magnet:\?xt=urn:btih[^\'"\s]+', response.text)

        # 处理提取到的链接
        for magnet_link in magnet_links:
            item['magnet_link'] = magnet_link
            yield item

    def parse_page_data(self, response):
        global comments, reviews
        actor_id = response.url.split("&s=")[1].split("&")[0]

        for row in response.xpath(
                '//table[@class="videotextlist"]/tr[not(contains(@class, "header"))]'
        ):
            td_elements = row.xpath("./td/text()").getall()
            if len(td_elements) >= 4:
                comments = int(td_elements[2])  # 这会得到1
                reviews = int(td_elements[3])  # 这会得到0
            # 生成每个作品的链接
            link = row.xpath('.//td[@class="title"]/div[@class="video"]/a/@href').get()
            absolute_link = response.urljoin(link)
            # 生成作品评论区链接
            # match = re.search(r"\?(.*)", link).group(0)
            # comment_page = "https://www.javlibrary.com/cn/videocomments.php" + match
            # 获取每个作品的id后缀链接
            yield scrapy.Request(
                url=absolute_link,
                callback=self.parse_preview,
                meta={"actor_id": actor_id, "comments": comments, "reviews": reviews},
            )
