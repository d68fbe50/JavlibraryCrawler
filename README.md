# Javlibrary 爬虫

## 介绍

`Javlibrary 爬虫` 是一个使用 Scrapy 框架的项目，用于从 [JavLibrary](https://www.javlibrary.com/)
网站提取日本成人视频数据。该项目可以获取演员信息、作品详情、评分、评论数、导演、制片商和标签等信息。

## [数据库结构](https://dbdiagram.io/)

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

### 确保环境

- 确保已安装所需的依赖项，如 `Scrapy` 和 `pymysql`。
- 确保能够科学上网，如果遇到 403 错误，请尝试更换不同地区的代理节点。测试时，韩国（Korea）和台湾（Taiwan）的节点可行。
- 不要在 GitHub Actions 中设置自动任务，因为 JavLibrary 禁止 GitHub 相关 IP 访问。

### 配置参数

- 修改 `config.arguments` 文件中的相关设置以满足你的需求。
  - 填入你想要爬取的演员的 ID，例如 `https://www.javlibrary.com/cn/vl_star.php?list&mode=&s=ae5q6&page=1`
    中的 `ae5q6` 就是演员的 ID。
  - `reference里提供了json格式的演员数据供参考`
- 通过修改`javlibrary_crawer.settings.ITEM_PIPELINES`选择要保存到哪个数据库中
  - 如果是redis：修改 `config.database_config` 中关于 Redis 服务器的配置。
  - 如果是mysql: 修改 `config.database_config` 中关于 Mysql 服务器的配置。

### 使用以下命令启动爬虫：

```bash
python main.py
```

### 爬取的数据将保存到数据库中。

## 注意事项

1. 在使用爬虫之前，请确保你有合适的权限访问目标网站。
2. 频繁地爬取可能导致你的 IP 被封锁，建议在 `settings.py` 中设置适当的延迟。
3. 请遵守网站的 `robots.txt` 文件和相关法律法规。

## 贡献

欢迎提交问题和拉取请求，一起完善此项目。

## 许可证

本项目使用 MIT 许可证，详情请查看 [LICENSE](LICENSE) 文件。

---

希望这个 README 文件能帮助你理解和使用这个项目。如果你需要进一步的帮助或有任何建议，请随时告诉我。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=desonglll/javlibrary_crawler&type=Date)](https://star-history.com/#desonglll/javlibrary_crawler&Date)
