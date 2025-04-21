from typing import Iterable

import cv2
import pyautogui
import pygetwindow as gw
import win32gui

import control
from control import Pox


def pic_match(big_img, template):
    res = cv2.matchTemplate(big_img, template, cv2.TM_CCOEFF_NORMED)
    h, w = template.shape[:2]
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    return Pox(center_x, center_y, max_val)


def split_pic(pic, pox1: Iterable, pox2: Iterable):
    a, b = pox1
    c, d = pox2
    return pic[b:d, a:c]


def screenshot():
    if not control.CloudGameClient:
        window = gw.getWindowsWithTitle("崩坏：星穹铁道")[0]
        if window and window.visible:
            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "崩坏：星穹铁道":
                print("截图失败....可能是游戏在后台，请手动切换一下...")
                return False
            left, top, width, height = window.left, window.top, window.width, window.height
            return pyautogui.screenshot(region=(left, top, width, height)).resize((1920, 1080))
        else:
            print("请打开游戏...")
            return None
    else:
        return control.CloudGameClient.screenshot()
