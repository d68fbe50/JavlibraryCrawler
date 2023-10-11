import requests


def main():
    url = "https://www.javbus.com/mide-702"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        # 替换为您的用户代理信息
        "Referer": "https://www.javbus.com/"  # 替换为合适的Referer
    }
    cookies = {
        "PHPSESSID": "qi3ofep9h1ufepeq7mcp7r0m83",
        # 添加更多的cookie...
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.text)

    pass


if __name__ == "__main__":
    main()
    pass
