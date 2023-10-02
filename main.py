import os

import javlibrary_crawler.run_spider
import javlibrary_crawler.download_preview
import javlibrary_crawler.pipelines
import javlibrary_crawler.initial as init


def main():
    print("hello")
    init.init_mysql()
    javlibrary_crawler.run_spider.main()
    # download_preview.download()
    pass


if __name__ == "__main__":
    main()
    # print(os.getcwd())
    pass
