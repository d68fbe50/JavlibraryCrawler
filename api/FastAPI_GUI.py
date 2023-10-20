import tkinter as tk
import subprocess
from tkinter import scrolledtext

from fast import app  # 导入FastAPI应用实例


class APIInfo:
    def __init__(self, path, method, description):
        self.path = path
        self.method = method
        self.description = description

    def __str__(self):
        return f"{self.method} {self.path} - {self.description}"


class FastAPIGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # 计算屏幕宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 计算窗口的位置，使其位于屏幕中心
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # 设置窗口的位置
        self.geometry(f'600x400+{int(x)}+{int(y)}')

        self.title("FastAPI GUI")

        self.server_status = tk.StringVar()
        self.server_status.set("服务器已停止")

        self.status_label = tk.Label(self, textvariable=self.server_status)
        self.status_label.pack(pady=20)

        self.toggle_button = tk.Button(self, text="启动服务器", command=self.toggle_server)
        self.toggle_button.pack(pady=20)

        # 初始化服务器进程为None
        self.server_process = None

        self.api_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=10)
        self.api_display.pack(pady=20)
        self.refresh_api_info()

    def refresh_api_info(self):
        api_infos = self.extract_api_info_from_app()
        for api_info in api_infos:
            self.api_display.insert(tk.END, str(api_info) + '\n')

    def extract_api_info_from_app(self):
        api_infos = []
        for route in app.routes:
            description = route.endpoint.__doc__.strip() if route.endpoint.__doc__ else "无描述"  # 使用docstring作为描述
            for method in route.methods:
                api_infos.append(APIInfo(route.path, method, description))
        return api_infos

    def toggle_server(self):
        if self.server_process:
            # 结束服务器进程
            self.server_process.terminate()
            self.server_process = None
            self.server_status.set("服务器已停止")
            self.toggle_button.config(text="启动服务器")
        else:
            # 在一个新子进程中启动服务器
            self.server_process = subprocess.Popen(["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8000"])
            self.server_status.set("服务器正在运行...")
            self.toggle_button.config(text="停止服务器")


if __name__ == "__main__":
    gui = FastAPIGUI()
    gui.mainloop()
