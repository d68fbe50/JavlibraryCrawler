
"""
ChatGPT提示词:
我已创建好基于pymysql的fastapi:(以下是已实现的代码)
# 数据模型
class Work(BaseModel):
    id: Optional[int]
    serial_number: Optional[str]
    title: Optional[str]
    actor_id: Optional[str]
    release_date: Optional[str]
    comments: Optional[int]
    reviews: Optional[int]
    preview: Optional[str]
    link: Optional[str]
    maker: Optional[str]
    length: Optional[int]
    director: Optional[str]
    label: Optional[str]
    user_rating: Optional[float]
    genres: Optional[str]
    cast: Optional[str]
    magnet_link: Optional[str]
    online_missav: Optional[str]
# 指定模板路径
templates = Jinja2Templates(directory="templates")

# 创建FastAPI应用
app = FastAPI()

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "070011",
    "database": "javcrawer"
}

你要帮我:
创建一个FastApi，从mysql的javcrawer数据库里获取works表。

api要实现的功能：
根据POST传入的起始日期和结束日期，从数据库里筛选出对应release_date的work对象放到列表格式的works并return。

以下是works表的结构：
mysql> describe works;
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| serial_number | varchar(255) | YES  | UNI | NULL    |                |
| title         | text         | YES  |     | NULL    |                |
| actor_id      | text         | YES  |     | NULL    |                |
| release_date  | date         | YES  |     | NULL    |                |
| comments      | int          | YES  |     | NULL    |                |
| reviews       | int          | YES  |     | NULL    |                |
| preview       | text         | YES  |     | NULL    |                |
| link          | text         | YES  |     | NULL    |                |
| maker         | varchar(255) | YES  |     | NULL    |                |
| length        | int          | YES  |     | NULL    |                |
| director      | varchar(255) | YES  |     | NULL    |                |
| label         | varchar(255) | YES  |     | NULL    |                |
| user_rating   | float        | YES  |     | NULL    |                |
| genres        | text         | YES  |     | NULL    |                |
| cast          | text         | YES  |     | NULL    |                |
| magnet_link   | text         | YES  |     | NULL    |                |
| online_missav | text         | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
18 rows in set (0.00 sec)
"""