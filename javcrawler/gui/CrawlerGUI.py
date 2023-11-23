import os
import sys
import tkinter as tk
from tkinter import scrolledtext

"""
GUI界面代码：负责界面显示和布局
"""


class CrawlerGUI(tk.Tk):
    def __init__(self, actions):
        super().__init__()
        self.actions = actions
        # 计算屏幕宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 计算窗口的位置，使其位于屏幕中心
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # 设置窗口的位置
        self.geometry(f'600x400+{int(x)}+{int(y)}')
        self.title("JAVLibrary Crawler")

        # 创建控件并绑定操作
        self.init_db_button = tk.Button(self, text="初始化数据库", command=actions.db_init)
        self.init_db_button.pack(pady=10)

        self.start_crawl_button = tk.Button(self, text="开始爬取", command=actions.start_crawl)
        self.start_crawl_button.pack(pady=10)

        self.download_preview_button = tk.Button(self, text="下载预览图", command=actions.download_preview)
        self.download_preview_button.pack(pady=10)

        # 添加重新启动按钮
        self.restart_button = tk.Button(self, text="重新启动", command=self.restart_program)
        self.restart_button.pack(pady=10)

        self.log_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=10)
        self.log_display.pack(pady=10)

    def log(self, msg):
        self.log_display.insert(tk.END, msg + '\n')
        self.log_display.see(tk.END)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
