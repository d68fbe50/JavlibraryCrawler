from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pymysql
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from contextlib import contextmanager
from config.database_config import MYSQL_CONFIG as db_config

# 指定模板路径

templates = Jinja2Templates(directory="templates")


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


class DateRange(BaseModel):
    start_date: str
    end_date: str


class ActorIDFilter(BaseModel):
    actor_ids: List[str]


# 创建FastAPI应用
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 用contextmanager创建数据库连接
@contextmanager
def get_db_connection():
    connection = pymysql.connect(**db_config)
    try:
        yield connection
    finally:
        connection.close()


def fetch_data_from_db(query, args=None):
    with get_db_connection() as conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, args)
        return cursor.fetchall()


@app.get("/api/works/", response_model=List[Work])
def get_works():
    """
    获取所有作品数据
    返回按发布日期降序排列的作品列表
    """
    # works_data = fetch_data_from_db("SELECT * FROM works ORDER BY release_date DESC")
    # works_data = fetch_data_from_db("SELECT * FROM works WHERE genres LIKE '%单体%' ORDER BY release_date DESC")
    works_data = fetch_data_from_db(
        "SELECT * FROM works WHERE genres LIKE '%单体%' AND genres NOT LIKE '%VR%' ORDER BY release_date DESC")

    for work in works_data:
        work["release_date"] = work["release_date"].strftime('%Y-%m-%d')
    return [Work(**work) for work in works_data]


@app.post("/api/get_works_by_date/")
async def get_works_by_date(date_range: DateRange):
    """
    根据日期范围获取作品数据
    输入：起始日期和结束日期
    返回：在这个日期范围内的作品
    """
    start_date = date_range.start_date
    end_date = date_range.end_date
    query = "SELECT * FROM works WHERE release_date BETWEEN %s AND %s ORDER BY release_date DESC"
    works = fetch_data_from_db(query, (start_date, end_date))
    return {"works": works}


@app.get("/")
def display_works(request: Request):
    works = get_works()
    return templates.TemplateResponse("display.html", {"request": request, "works": works})


@app.get("/by_date/")
def display_by_date(request: Request):
    """
    根据日期显示作品
    返回一个页面，用户可以选择日期来过滤作品
    """
    works = get_works()
    return templates.TemplateResponse("fliter_by_date.html", {"request": request, "works": works})


@app.get("/api/fetch_all_casts/")
def fetch_all_casts():
    """
    获取所有的演员（cast）
    返回所有在作品中出现过的独特的演员列表
    """
    casts_data = fetch_data_from_db("SELECT DISTINCT cast FROM works;")
    return {"casts": [cast["cast"] for cast in casts_data]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
