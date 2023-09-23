import pymysql
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# 数据库连接信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Lindesong7758?',
    'database': 'javcraw'
}


def get_image_links():
    # 创建数据库连接
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # 执行SQL查询
    cursor.execute("SELECT preview FROM spider")
    results = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    connection.close()

    # 返回所有的图片链接
    return [row[0] for row in results]


def download_image(link, folder='downloaded_images'):
    # 确保文件夹存在
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 从链接中获取图片名
    filename = os.path.join(folder, link.split('/')[-1])
    response = requests.get(link, stream=True)
    print(f"Download {link}")
    with open(filename, 'wb') as img_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                img_file.write(chunk)


def multi_threaded_download(links, folder='downloaded_images', max_threads=5):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for link in links:
            executor.submit(download_image, link, folder)


def download():
    print("开始下载预览图")
    links = get_image_links()
    multi_threaded_download(links)


if __name__ == '__main__':
    download()
