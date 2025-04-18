from dataclasses import dataclass

import pyautogui
import pygetwindow as gw

from ucClient import ucClient

CloudGameClient: ucClient = None


def left_click(x, y, duration=0.1):
    if not CloudGameClient:
        try:
            pyautogui.click(x, y, duration=duration)
            print(f"鼠标点击 ({x}, {y})")
        except Exception as e:
            print(f"鼠标点击出错：{e}")
    else:
        CloudGameClient.click(x, y)


def drag(start_x, start_y, end_x, end_y, duration=0.1):
    if not CloudGameClient:
        try:
            pyautogui.mouseDown(start_x, start_y)
            pyautogui.moveTo(end_x, end_y, duration=duration)
            pyautogui.mouseUp()
            print(f"鼠标点击并移动 ({start_x}, {start_y}) -> ({end_x}, {end_y})")
        except Exception as e:
            print(f"鼠标移动出错：{e}")
    else:
        CloudGameClient.drag(start_x, start_y, end_x, end_y)


@dataclass
class Pox:
    x: int
    y: int
    val: float

    def __init__(self, x: int, y: int, val: float):
        self.x = x
        self.y = y
        self.val = val

    def __iter__(self):
        return iter([self.x, self.y])


def get_real_pox(pox: Pox):
    # return pox
    dev = 1920, 1080
    this_dev = get_this_dev_size()
    result = Pox(pox.x / dev[0] * this_dev[0],
                 pox.y / dev[1] * this_dev[1],
                 pox.val)
    print(f"原：{pox.x},{pox.y} 目标：{result.x},{result.y}")
    return result


def get_this_dev_size() -> list:
    if not CloudGameClient:
        if not hasattr(get_this_dev_size, "_size"):
            try:
                window = gw.getWindowsWithTitle("崩坏：星穹铁道")[0]
                left, top, width, height = window.left, window.top, window.width, window.height
                img = pyautogui.screenshot(region=(left, top, width, height)).size
            except IndexError as e:
                print("请先启动游戏在启动本程序")
                raise e
            if img is not False:
                get_this_dev_size._size = img
        return getattr(get_this_dev_size, "_size", None)
    else:
        return [CloudGameClient.width, CloudGameClient.height]
