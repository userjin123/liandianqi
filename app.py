
import time
import threading
from pynput import mouse

# 使用线程安全的 Event 替代布尔变量
clicking_event = threading.Event()
exit_event = threading.Event()  # 用于安全退出


def click_mouse():
    mouse_controller = mouse.Controller()
    while not exit_event.is_set():
        if clicking_event.is_set():
            try:
                mouse_controller.press(mouse.Button.x2)
                time.sleep(0.05)  # 按下持续时间
                mouse_controller.release(mouse.Button.x2)
            except Exception as e:
                print(f"点击异常: {e}")
                clicking_event.clear()  # 异常时自动停止
            time.sleep(0.05)  # 点击间隔（可调节频率）
        else:
            time.sleep(0.01)  # 空闲时低负载等待


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            print("连点模式启动")
            clicking_event.set()  # 原子操作设置状态
        else:
            print("连点模式停止")
            clicking_event.clear()  # 原子操作清除状态


# 改进版主程序
with mouse.Listener(on_click=on_click) as listener:
    click_thread = threading.Thread(target=click_mouse)
    click_thread.daemon = True
    click_thread.start()

    try:
        while not exit_event.is_set():
            time.sleep(0.5)  # 主线程检查间隔
    except KeyboardInterrupt:
        print("\n正在安全退出...")
    finally:
        exit_event.set()
        clicking_event.clear()
        listener.stop()
        click_thread.join(timeout=1)
        print("程序已安全终止")
