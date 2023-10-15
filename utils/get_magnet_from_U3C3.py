import json
from bs4 import BeautifulSoup

import requests


def get_html_text(text):
    url = f"https://u3c3.com/?search2=eelja3lfea&search={text}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def extract_html_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select('tr.default')
    result_list = []

    for row in rows:
        title_elem = row.select_one('a[title^="MIDE-"]')
        magnet_elem = row.select_one('.fa.fa-fw.fa-magnet')
        size_elem = row.select_one('.text-center:nth-of-type(1)')
        date_elem = row.select_one('.text-center:nth-of-type(2)')
        cloud_elem = row.select_one('a[href^="https://mypikpak.com"]')

        if title_elem and magnet_elem and size_elem and date_elem and cloud_elem:
            title = title_elem['title']
            magnet_link = magnet_elem.parent['href']
            size = size_elem.text.strip()
            date = date_elem.text.strip()
            cloud_link = cloud_elem['href']

            result_list.append({
                "Title": title,
                "MagnetLink": magnet_link,
                "Size": size,
                "Date": date,
                "CloudLink": cloud_link
            })

    json_output = json.dumps(result_list, indent=4, ensure_ascii=False)
    print(json_output)


def get_magnet_object(html_content):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到所有的<tr>标签
    rows = soup.select('tr.default')

    # 初始化一个空的列表来存储结果
    result_list = []

    for row in rows:
        title_tag = row.select_one('td:nth-child(2) a')
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = None

        magnet_icon = row.select_one('.fa.fa-fw.fa-magnet')
        if magnet_icon:
            magnet_link = magnet_icon.parent['href']
        else:
            magnet_link = None

        size_td = row.select_one('td.text-center:nth-child(4)')
        if size_td:
            size = size_td.get_text(strip=True)
        else:
            size = None

        date_td = row.select_one('td.text-center:nth-child(5)')
        if date_td:
            upload_date = date_td.get_text(strip=True)
        else:
            upload_date = None

        mypikpak_link = row.select_one('a[href*="https://mypikpak.com/drive/url-checker"]')
        if mypikpak_link:
            mypikpak_url = mypikpak_link['href']
        else:
            mypikpak_url = None

        result_list.append({
            "Title": title,
            "MagnetLink": magnet_link,
            "Size": size,
            "UploadDate": upload_date,
            "MypikpakURL": mypikpak_url
        })
    return result_list


def size_to_float(size_str):
    size_str = size_str.lower()
    if 'gb' in size_str:
        return float(size_str.replace('gb', '').strip())
    elif 'mb' in size_str:
        return float(size_str.replace('mb', '').strip()) / 1024
    elif 'kb' in size_str:
        return float(size_str.replace('kb', '').strip()) / (1024 ** 2)
    else:  # 如果Size值有其他格式，您可以在这里继续添加
        return 0.0


def get_magnet(text):
    html_text = get_html_text(text)
    if html_text:
        obj = get_magnet_object(html_text)
        if obj:
            return obj
        else:
            print("Magnet链接对象获取失败")
    else:
        print("无法获取HTML文本")


def get_maxSize_obj(lists):
    return max(lists, key=lambda x: size_to_float(x['Size']))


def fliter_by_size(lists, min_size, max_size):
    # 过滤出给定大小范围内的对象
    filtered_list = [item for item in lists if min_size <= size_to_float(item['Size']) <= max_size]
    if filtered_list:
        return filtered_list
    return None


if __name__ == "__main__":
    magnet = get_magnet("MIDE-960")
    max_size_obj = fliter_by_size(magnet, 3, 4)
    print(magnet[0]["Title"])
    print(type(magnet))
    for i in max_size_obj:
        print(i["Size"], i["Title"])
    pass
