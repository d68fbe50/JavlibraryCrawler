# Javlibrary Crawler

## 介绍

`Javlibrary Crawler` 是一个用于从[JavLibrary](https://www.javlibrary.com/)网站提取日本成人视频数据的 Scrapy
爬虫项目。项目能够获取演员信息、作品详情、评分、评论数、导演、制片商和标签等信息。

## [数据库结构](https://dbdiagram.io/d)

```db
Table movies {
  id integer [primary key, increment]
  serial_number varchar(255) [unique]
  title text
  actor_id text
  release_date date
  comments integer
  reviews integer
  preview text
  link text
  maker varchar(255)
  length integer
  director varchar(255)
  label varchar(255)
  user_rating float
  genres text  
  cast text   
}

Table actors{
  actor_id text
  actor_name text
}

Ref: movies.actor_id > actors.actor_id
Ref: movies.cast > actors.actor_name
```

## 使用方法

1. 确保你已经安装了所有必要的依赖，例如`Scrapy`和`pymysql`。

2. 修改`arguments.py`文件中的相关设置，以适应你的需求。

3. 使用以下命令启动爬虫：

```bash
python main.py
```

4. 爬取的数据将保存到`Redis`数据库中。

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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=desonglll/my-awesome-stars&type=Date)](https://star-history.com/#desonglll/my-awesome-stars&Date)
