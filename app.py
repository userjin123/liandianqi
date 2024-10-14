import time
import threading
from pynput import mouse

clicking = False  # 连点器的状态


def click_mouse():
    mouse_controller = mouse.Controller()
    while True:
        if clicking:
            try:
                mouse_controller.press(mouse.Button.x2)  # 模拟按下事件
                mouse_controller.release(mouse.Button.x2)
            except Exception as e:
                print(f"点击时发生错误: {e}")
            time.sleep(0.1)  # 点击间隔时间
        else:
            time.sleep(0.01)  # 如果没有点击，则减少CPU占用


def on_click(x, y, button, pressed):
    global clicking
    if button == mouse.Button.left:  # 点击鼠标左键触发连点器
        if pressed:
            print("按下鼠标左键")
            clicking = True  # 当鼠标左键按下时，启动连点器
        else:
            clicking = False  # 当手动释放鼠标左键时，停止连点器


# 创建鼠标监听器
with mouse.Listener(on_click=on_click) as listener:
    click_thread = threading.Thread(target=click_mouse)  # 启动连点器线程
    click_thread.daemon = True
    click_thread.start()
    try:
        while True:  # 保持主线程运行
            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()  # 停止监听器
        click_thread.join()  # 程序中断时，关闭连点器线程
