import tkinter as tk
from tkinter import messagebox, scrolledtext
import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javlibrary_crawler.spiders.works_spider import WorksSpider
from javlibrary_crawler.spiders.magnet_spider import MagnetSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
import dbop.mysql_op as mysql_op
from config.database_config import MYSQL_CONFIG, MYSQL_DBNAME
from preview_download import download_preview as pdown
from config import arguments
