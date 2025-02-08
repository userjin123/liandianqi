import tkinter as tk
from tkinter import ttk
import time
import threading
from pynput import mouse


class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("鼠标连点器 v1.1")
        # 窗口大小
        self.root.geometry(f"{300}x{200}")
        # 线程控制事件
        self.listening_event = threading.Event()  # 监听开关
        self.clicking_event = threading.Event()  # 点击状态
        self.exit_event = threading.Event()  # 退出信号

        # 初始化UI
        self.create_widgets()

        # 启动监听线程
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

        # 启动点击线程
        self.click_thread = threading.Thread(target=self.click_worker)
        self.click_thread.daemon = True
        self.click_thread.start()

        # 窗口关闭处理
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)

    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 状态显示
        self.status_label = ttk.Label(
            main_frame,
            text="当前状态：暂停中",
            font=('Helvetica', 12)
        )
        self.status_label.pack(pady=10)

        # 控制按钮
        self.toggle_btn = ttk.Button(
            main_frame,
            text="启 动",
            command=self.toggle_listening,
            width=15
        )
        self.toggle_btn.pack(pady=5)

        # 退出按钮
        ttk.Button(
            main_frame,
            text="退 出",
            command=self.safe_exit,
            width=15
        ).pack(pady=5)

        # 版本信息
        ttk.Label(
            main_frame,
            text="祝您大杀特杀",
            foreground="gray"
        ).pack(side=tk.BOTTOM, pady=5)

    def toggle_listening(self):
        """切换监听状态"""
        if self.listening_event.is_set():
            self.listening_event.clear()
            self.clicking_event.clear()  # 停止当前点击
            self.update_ui(False)
        else:
            self.listening_event.set()
            self.update_ui(True)

    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击回调（仅在监听启用时生效）"""
        if self.listening_event.is_set() and button == mouse.Button.left:
            if pressed:
                self.clicking_event.set()
                self.root.after(0, self.update_status, "运行中")
            else:
                self.clicking_event.clear()
                self.root.after(0, self.update_status, "待机中")

    def update_ui(self, is_listening):
        """更新主界面状态"""
        state_text = "监听中" if is_listening else "暂停中"
        btn_text = "暂 停" if is_listening else "启 动"
        self.status_label.config(text=f"当前状态：{state_text}")
        self.toggle_btn.config(text=btn_text)

    def update_status(self, status):
        """更新运行状态"""
        self.status_label.config(text=f"当前状态：{status}")

    def click_worker(self):
        """执行点击的工作线程"""
        controller = mouse.Controller()
        while not self.exit_event.is_set():
            if self.clicking_event.is_set() and self.listening_event.is_set():
                try:
                    # 使用X2侧键进行点击（可根据需要修改）
                    controller.press(mouse.Button.x2)
                    time.sleep(0.05)
                    controller.release(mouse.Button.x2)
                except Exception as e:
                    print(f"点击错误: {e}")
                    self.root.after(0, self.update_status, "异常停止")
                    self.clicking_event.clear()
                time.sleep(0.05)  # 点击间隔
            else:
                time.sleep(0.01)

    def safe_exit(self):
        """安全退出程序"""
        self.exit_event.set()
        self.listening_event.clear()
        self.clicking_event.clear()
        self.mouse_listener.stop()
        self.click_thread.join(timeout=1)
        self.root.destroy()
        print("程序已安全退出")


if __name__ == "__main__":
    app = AutoClickerApp()
    app.root.mainloop()
