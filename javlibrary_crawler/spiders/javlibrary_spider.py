import pymysql
import scrapy
from javlibrary_crawler.items import WorkSpider

from javlibrary_crawler.arguments import ids


class JavlibrarySpider(scrapy.Spider):
    name = "javlibrary"
    base_url_template = 'https://www.javlibrary.com/cn/vl_star.php?list&mode=&s={actor_id}&page={page}'
    items_dict = {}

    # 从MySQL数据库获取所有的actor_id
    def get_all_actor_ids(self):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Lindesong7758?',
            database='javcraw'
        )

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # 使用DictCursor
                sql = "SELECT actor_id FROM actor"
                cursor.execute(sql)
                result = cursor.fetchall()
                return [item['actor_id'] for item in result]
        finally:
            connection.close()

    def start_requests(self):
        actor_ids = ids
        # print("Starting requests for actor_ids:", actor_ids)  # 打印开始请求的actor_ids

        for actor_id in actor_ids:
            yield scrapy.Request(url=self.base_url_template.format(actor_id=actor_id, page=1),
                                 callback=self.parse_pagination,
                                 meta={'base_url': self.base_url_template.format(actor_id=actor_id, page='{}')})

    def parse_pagination(self, response):
        # 先解析当前页的数据（第一页）
        for item in self.parse_page_data(response):
            yield item

        base_url = response.meta['base_url']
        # 解析最后一页的数字
        last_page_num = int(response.xpath('//a[@class="page last"]/@href').re(r'page=(\d+)')[0])

        # 使用for循环生成每一页的URL，并使用parse方法爬取数据
        for page in range(2, last_page_num + 1):
            yield scrapy.Request(url=base_url.format(page), callback=self.parse)

    def parse(self, response):
        for item in self.parse_page_data(response):
            yield item

    def parse_preview(self, response):
        # print(response.text)

        item = WorkSpider()
        item['actor_id'] = response.meta['actor_id']

        # ID 或 serial_number
        serial_number_result = response.xpath('//div[@id="video_id"]/table//td[@class="text"]/text()').get()
        item['serial_number'] = serial_number_result.strip() if serial_number_result else None

        # title
        title_result = response.xpath('//div[@id="video_title"]/h3[@class="post-title text"]/a/text()').get()
        item['title'] = title_result.strip() if title_result else None

        # Release Date
        release_date_result = response.xpath('//div[@id="video_date"]/table//td[@class="text"]/text()').get()
        item['release_date'] = release_date_result.strip() if release_date_result else None

        # Length
        length_text_result = response.xpath('//div[@id="video_length"]/table//td/span[@class="text"]/text()').get()
        item['length'] = int(length_text_result.strip()) if length_text_result else None

        # Director
        director_result = response.xpath('//div[@id="video_director"]//td[@class="text"]/text()').get()
        item[
            'director'] = director_result.strip() if director_result else "Unknown"

        # Maker
        maker_result = response.xpath('//div[@id="video_maker"]//td[@class="text"]/span[@class="maker"]/a/text()').get()
        item['maker'] = maker_result.strip() if maker_result else "Unknown"

        # Label
        label_result = response.xpath('//div[@id="video_label"]//td[@class="text"]/span[@class="label"]/a/text()').get()
        item['label'] = label_result.strip() if label_result else "Unknown"

        # User Rating
        rating_text_result = response.xpath(
            '//div[@id="video_review"]/table//td[@class="text"]/span[@class="score"]/text()').get()
        if rating_text_result:
            rating_text = rating_text_result.strip()
            item['user_rating'] = float(rating_text.replace('(', '').replace(')', ''))
        else:
            item['user_rating'] = None

        # Genre(s)
        genres = response.xpath('//div[@id="video_genres"]/table//td[@class="text"]/span/a/text()').getall()
        item['genres'] = ', '.join(genres)

        # Cast
        cast_result = response.xpath('//div[@id="video_cast"]/table//td[@class="text"]/span/span/a/text()').getall()
        item['cast'] = ', '.join(cast_result)

        # Link (如果需要的话，这里是完整的URL)
        item['link'] = response.url

        # 从response中提取图片的src
        preview_result = response.xpath('//div[@id="video_jacket"]/img/@src').get()
        item['preview'] = preview_result.strip() if preview_result else None

        # Initialize comments and reviews to 0 as they weren't extracted in the example provided
        item['comments'] = response.meta['comments']
        item['reviews'] = response.meta['reviews']

        yield item

    def parse_page_data(self, response):
        global comments, reviews
        actor_id = response.url.split('&s=')[1].split('&')[0]

        for row in response.xpath('//table[@class="videotextlist"]/tr[not(contains(@class, "header"))]'):
            td_elements = row.xpath('./td/text()').getall()
            if len(td_elements) >= 4:
                comments = int(td_elements[2])  # 这会得到1
                reviews = int(td_elements[3])  # 这会得到0
            link = row.xpath('.//td[@class="title"]/div[@class="video"]/a/@href').get()
            absolute_link = response.urljoin(link)
            yield scrapy.Request(url=absolute_link, callback=self.parse_preview,
                                 meta={'actor_id': actor_id, 'comments': comments, 'reviews': reviews}, )
