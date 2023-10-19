from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Optional
import pymysql
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from contextlib import contextmanager

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

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "070011",
    "database": "javcrawer"
}


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
    works_data = fetch_data_from_db("SELECT * FROM works ORDER BY release_date DESC")
    for work in works_data:
        work["release_date"] = work["release_date"].strftime('%Y-%m-%d')
    return [Work(**work) for work in works_data]


@app.post("/api/get_works_by_date/")
async def get_works_by_date(date_range: DateRange):
    start_date = date_range.start_date
    end_date = date_range.end_date
    query = "SELECT * FROM works WHERE release_date BETWEEN %s AND %s ORDER BY release_date DESC"
    works = fetch_data_from_db(query, (start_date, end_date))
    return {"works": works}


@app.get("/display/")
def display_works(request: Request):
    works = get_works()
    return templates.TemplateResponse("display.html", {"request": request, "works": works})


@app.get("/by_date/")
def display_by_date(request: Request):
    works = get_works()
    return templates.TemplateResponse("fliter_by_date.html", {"request": request, "works": works})


@app.get("/by_casts/")
def filter_by_casts(request: Request):
    return templates.TemplateResponse("filter_by_casts.html", {"request": request})


# @app.get("/api/casts/")
# def fetch_all_casts():
#     casts_data = fetch_data_from_db("SELECT DISTINCT cast FROM works;")
#     return {"casts": [cast["cast"] for cast in casts_data]}

@app.post("/api/works_by_cast/")
async def get_works_by_cast(actor_id_filter: ActorIDFilter):
    try:
        with pymysql.connect(**db_config) as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM works WHERE actor_id IN %s"
            cursor.execute(query, (tuple(actor_id_filter.actor_ids),))
            works_data = cursor.fetchall()

            for work in works_data:
                work["release_date"] = work["release_date"].strftime('%Y-%m-%d')
            return {"works": [Work(**work) for work in works_data]}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
