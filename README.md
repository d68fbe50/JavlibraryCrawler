# Javlibrary Crawler

## 介绍

`Javlibrary Crawler` 是一个用于从[JavLibrary](https://www.javlibrary.com/)网站提取日本成人视频数据的 Scrapy 爬虫项目。项目能够获取演员信息、作品详情、评分、评论数、导演、制片商和标签等信息。

## 目录结构

```
.
├── README.md                           - 本说明文件
├── javlibrary_crawler                  - 主要爬虫代码目录
│   ├── __init__.py                     - 初始化文件
│   ├── arguments.py                   - 参数文件
│   ├── download_preview.py            - 下载预览脚本
│   ├── items.py                       - Scrapy items定义文件
│   ├── javcraw.db                     - SQLite数据库文件
│   ├── main.py                        - 主脚本文件
│   ├── middlewares.py                 - Scrapy中间件文件
│   ├── output.json                    - 输出的JSON数据文件
│   ├── pipelines.py                   - 数据处理管道文件
│   ├── run_spider.py                  - 爬虫启动脚本
│   ├── settings.py                    - Scrapy设置文件
│   └── spiders                        - 爬虫脚本目录
│       ├── __init__.py                - 初始化文件
│       ├── actor_spider.py            - 演员数据爬虫
│       └── javlibrary_spider.py       - 主要数据爬虫
└── scrapy.cfg                         - Scrapy配置文件
```

## 使用方法

1. 确保你已经安装了所有必要的依赖，例如`Scrapy`和`pymysql`。

2. 修改`settings.py`文件中的相关设置，以适应你的需求。

3. 使用以下命令启动爬虫：

```bash
$ python javlibrary_crawler/run_spider.py
```

4. 爬取的数据将保存到`javcraw.db` SQLite数据库文件中。

## 注意事项

1. 在使用爬虫之前，请确保你有合适的权限访问目标网站。
2. 频繁的爬取可能导致你的IP被封锁，建议在`settings.py`中设置适当的延迟。
3. 请遵守网站的`robots.txt`文件和相关法律法规。

## 贡献

欢迎提交问题和拉取请求，一同完善此项目。

## 许可证

本项目使用MIT许可证，详情请查看[LICENSE](LICENSE)文件。

---

希望这个README文件能帮助你理解和使用这个项目。如果你需要进一步的帮助或有任何建议，随时告诉我。