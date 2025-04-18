from dataclasses import dataclass
from enum import Enum
from typing import Iterable

import PIL.Image
import win32gui
from PIL.Image import Image
import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
import random
import threading

debug_mod = False
task7_timer = 3600  # 每1小时执行一次task7


def resize_to_standard(img, standard_width=1920, standard_height=1080):
    return cv2.resize(img, (standard_width, standard_height), interpolation=cv2.INTER_AREA)


def get_this_dev_size():
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


def screenshot():
    window = gw.getWindowsWithTitle("崩坏：星穹铁道")[0]
    if window and window.visible:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "崩坏：星穹铁道":
            print("截图失败....可能是游戏在后台，请手动切换一下...")
            return False
        left, top, width, height = window.left, window.top, window.width, window.height
        return pyautogui.screenshot(region=(left, top, width, height)).resize((1920, 1080))
    else:
        print("请打开游戏...")
        return False


@dataclass
class pox_result:
    x: int
    y: int
    val: float

    def __iter__(self):
        return iter([self.x, self.y])


def get_real_pox(pox: pox_result):
    # return pox
    dev =  1920,1080
    this_dev = get_this_dev_size()
    result = pox_result(pox.x / dev[0] * this_dev[0],
                        pox.y / dev[1] * this_dev[1],
                        pox.val)
    print(f"原：{pox.x},{pox.y}目标：{result.x},{result.y}")
    return result


def split_pic(pic, pox1: Iterable, pox2: Iterable):
    a, b = pox1
    c, d = pox2
    return pic[b:d, a:c]


def mouse_click(self, x, y):
    try:
        pyautogui.click(x, y)
        self.logger.debug(f"鼠标点击 ({x}, {y})")
    except Exception as e:
        self.logger.error(f"鼠标点击出错：{e}")


def pic_match(big_img, template):
    res = cv2.matchTemplate(big_img, template, cv2.TM_CCOEFF_NORMED)
    h, w = template.shape[:2]
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    return pox_result(center_x, center_y, max_val)


class control:
    @staticmethod
    def print_mode(func):
        def wrapper(*args, **kwargs):
            print(f"Positional arguments: {args}")
        return wrapper
    @staticmethod
    def click(x,y):
        pyautogui.click(x,y)
    @staticmethod
    # @print_mode
    def mouse_down(x, y):
        pyautogui.mouseDown(x, y)

    @staticmethod
    # @print_mode
    def mouse_up():
        pyautogui.mouseUp()

    @staticmethod
    # @print_mode
    def mouse_move(x, y):
        pyautogui.moveTo(x, y)


class task(Enum):
    task0 = 0x0  # 结算
    task1 = 0x01  # 帕姆快送
    task2 = 0x02  # 来宾事件
    task3 = 0x03  # 特殊来宾 暂未实现
    task4 = 0x04  # 薅鸟毛
    task5 = 0x05  # 误触管理恢复
    task6 = 0x06  # 新一轮开启失败恢复
    task7 = 0x07  # 抽卡&角色升级


def pil_to_cv(img):
    """PIL → OpenCV"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


class photo_tool:
    @staticmethod
    def difference_blend(img1: Image, img2: Image):

        if isinstance(img1, Image):
            img1 = pil_to_cv(img1)
        if isinstance(img2, Image):
            img2 = pil_to_cv(img2)
        # 图像需为相同大小
        img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
        # 差值混合（类似 Photoshop 的 Difference 模式）
        diff = cv2.absdiff(img1, img2)
        return diff

    @staticmethod
    def extract_green_area(diff_img):
        # 转为 HSV
        hsv = cv2.cvtColor(diff_img, cv2.COLOR_BGR2HSV)
        h, s, v = 62, 132, 244
        # 绿色范围（你可以根据实际微调）
        lower_green = np.array([max(0, h - 15), max(0, s - 50), max(0, v - 40)])
        upper_green = np.array([min(179, h + 15), min(255, s + 50), min(255, v + 40)])

        # 掩码
        mask = cv2.inRange(hsv, lower_green, upper_green)
        return mask

    @staticmethod
    def find_largest_green_block(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # 找面积最大轮廓
        max_cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_cnt)
        center_x = x + w // 2
        center_y = y + h // 2
        return center_x, center_y

    def find_green_diff_area(self, img1, img2):
        diff = self.difference_blend(img1, img2)
        green_mask = self.extract_green_area(diff)
        rect = self.find_largest_green_block(green_mask)
        return rect


class do_task:
    @staticmethod
    def task0():
        control.mouse_down(*get_real_pox(pox_result(964, 916, val=0.0)))
        control.mouse_up()
        time.sleep(5)
        control.mouse_down(*get_real_pox(pox_result(992, 905, val=0.0)))
        control.mouse_up()

    @staticmethod
    def task1(point: pox_result):
        all_point = [[1457, 377],
                     [1615, 719],
                     [1278, 714],
                     [1032, 876],
                     [631, 625],
                     [483, 763],
                     [345, 507],
                     [797, 230],
                     [1174, 249], ]

        x = point.x
        y = point.y
        print("执行任务一中...")
        for i in all_point:
            control.mouse_down(*get_real_pox(pox_result(x, y, val=0.0)))
            control.mouse_move(*get_real_pox(pox_result(*i, val=0.0)))
            control.mouse_up()

    @staticmethod
    def task2():
        control.mouse_down(*get_real_pox(pox_result(796, 742, 0.0)))
        control.mouse_up()
        time.sleep(3)
        control.mouse_down(*get_real_pox(pox_result(1638, 830, 0.0)))
        control.mouse_up()
        time.sleep(3)
        control.mouse_down(*get_real_pox(pox_result(1616, 965, 0.0)))
        control.mouse_up()
        time.sleep(7)
        control.mouse_down(*get_real_pox(pox_result(1749, 961, 0.0)))
        control.mouse_up()
        time.sleep(.5)

    @staticmethod
    def task4():
        control.mouse_down(*get_real_pox(pox_result(1319, 915, 0.0)))
        control.mouse_up()
        time.sleep(2)
        t = time.time()
        while t + 10 > time.time():
            control.click(*get_real_pox(pox_result(912, 765, 0.0)))
        time.sleep(3)

    @staticmethod
    def task5():
        control.mouse_down(*get_real_pox(pox_result(1773, 85, 0.0)))
        control.mouse_up()

    @staticmethod
    def task6():
        control.mouse_down(*get_real_pox(pox_result(991, 902, 0.0)))
        control.mouse_up()

    @staticmethod
    def task3(point: pox_result):
        control.mouse_down(*get_real_pox(pox_result(point.x, point.y, 0.0)))
        control.mouse_up()

    @staticmethod
    def task7(): # 抽卡&角色升级
        control.mouse_down(*get_real_pox(pox_result(1663, 948, 0.0))) # 打开抽卡页面
        control.mouse_up()
        time.sleep(2)

        while True: # 抽炫彩
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (1277, 739), (1277+224, 739+35)), template=cv2.imread("img/c7.png"))
            if t7.val > 0.8 and t7.val != 1.0:
                control.mouse_down(*get_real_pox(pox_result(1386, 819, 0.0)))
                control.mouse_up()
                time.sleep(2)
                control.mouse_down(*get_real_pox(pox_result(1809, 65, 0.0)))
                control.mouse_up()
                time.sleep(4)
                control.mouse_down(*get_real_pox(pox_result(1809, 65, 0.0)))
                control.mouse_up()
                time.sleep(2)
            else:
                break

        time.sleep(2)

        while True: # 抽贵金
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (872, 742), (869+210, 742+32)), template=cv2.imread("img/c7_4.png"))
            if t7.val > 0.8 and t7.val != 1.0:
                control.mouse_down(*get_real_pox(pox_result(983, 819, 0.0)))
                control.mouse_up()
                time.sleep(2)
                control.mouse_down(*get_real_pox(pox_result(1809, 65, 0.0)))
                control.mouse_up()
                time.sleep(4)
                control.mouse_down(*get_real_pox(pox_result(1809, 65, 0.0)))
                control.mouse_up()
                time.sleep(2)
            else:
                break

        time.sleep(2)

        while True: # 避免抽卡无法退出
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (99, 64), (99+58, 64+33)), template=cv2.imread("img/c7_3.png"))
            if t7.val > 0.7 and t7.val != 1.0:
                control.mouse_down(*get_real_pox(pox_result(1860, 66, 0.0)))
                control.mouse_up()
                time.sleep(0.5)
            else:
                break

        time.sleep(2)
        control.mouse_down(*get_real_pox(pox_result(1849, 803, 0.0))) # 一键收取
        control.mouse_up()
        time.sleep(1)
        control.mouse_down(*get_real_pox(pox_result(1796, 940, 0.0))) # 会场管理
        control.mouse_up()
        time.sleep(1)

        def upgrade(): # 升级角色
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (1347, 856), (1347+314, 856+46)), template=cv2.imread("img/c7_2.png"))
            if t7.val > 0.6 and t7.val != 1.0:
                control.mouse_down(*get_real_pox(pox_result(1502, 876, 0.0)))
                control.mouse_up()
                return True
            else:
                return False

        all_points = [
            [512, 659],
            [695, 544],
            [440, 444],
            [821, 239],
            [1108, 258],
            [1380, 331],
            [1467, 606],
            [1220, 637],
            [1011, 747]
        ]
        while True: # 循环升级角色直到没有升级
            for point in random.sample(all_points, len(all_points)): # 随机打乱升级顺序
                control.mouse_down(*get_real_pox(pox_result(point[0], point[1], 0.0)))
                control.mouse_up()
                time.sleep(0.2)
                if not upgrade():
                    break
            break

        time.sleep(2)
        
        while True: # 避免无法退出升级页面
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (1574, 0), (1919, 142)), template=cv2.imread("img/exit0.png"))
            if t7.val > 0.7 and t7.val != 1.0:
                control.mouse_down(*get_real_pox(pox_result(1760, 86, 0.0)))
                control.mouse_up()
                time.sleep(0.5)
            else:
                break


def get_task(img: Image):
    global task7_timer # 任务7的定时器
    @dataclass
    class get_task_result:
        task_num: task
        pox: pox_result

    if task7_timer < 0:
        task7_timer = 3600 # 重置定时器
        return get_task_result(task.task7, None)

    t6 = pic_match(big_img=split_pic(img, (715, 834), (1258, 951)), template=cv2.imread("img/start.png"))  # 可信度大约为7
    if debug_mod:
        cv2.imwrite(f"debug/img_task6.jpg", split_pic(img, (715, 834), (1258, 951)))
    if t6.val > 0.65 and t6.val != 1.0:
        # print(111)
        return get_task_result(task.task6, t6)

    t5 = pic_match(big_img=split_pic(img, (1574, 0), (1919, 142)), template=cv2.imread("img/exit0.png"))  # 可信度大约为7
    if debug_mod:
        cv2.imwrite(f"debug/img_task5.jpg", split_pic(img, (1574, 0), (1919, 142)))
    if t5.val > 0.7 and t5.val != 1.0:
        return get_task_result(task.task5, t5)

    t0 = pic_match(big_img=split_pic(img, (883, 235), (1038, 273)), template=cv2.imread("img/0.png"))  # 可信度大约为7
    if debug_mod:
        cv2.imwrite(f"debug/img_task0.jpg", split_pic(img, (883, 235), (1038, 300)))
        print(f"当前可信度task0可信度{t0.val}")
    if t0.val > 0.6 and t0.val != 1.0:
        return get_task_result(task.task0, t0)

    t = pic_match(big_img=img, template=cv2.imread("img/a.png"))  # 可信度大约为7
    if t.val > 0.5 and t.val != 1.0:
        return get_task_result(task.task1, t)

    t2 = pic_match(big_img=split_pic(img, (700, 700), (850, 850)), template=cv2.imread("img/b.png"))  # 可信度大约为8
    if debug_mod:
        cv2.imwrite(f"debug/img_task2.jpg", split_pic(img, (700, 700), (850, 850)))
    if t2.val > 0.5 and t2.val != 1.0:
        return get_task_result(task.task2, t2)

    t4 = pic_match(big_img=split_pic(img, (1245, 867), (1412, 990)), template=cv2.imread("img/d.png"))  # 可信度大约为8
    if debug_mod:
        cv2.imwrite(f"debug/img_task4.jpg", split_pic(img, (1245, 867), (1412, 990)))
    if t4.val < 0.5 and t4.val != 1.0 and t4.val != 0.0:
        return get_task_result(task.task4, t4)

def timer(): # 定时器，用于定时任务7
    global task7_timer
    while True:
        time.sleep(1)
        task7_timer -= 1


pyautogui.failSafeCheck()
if __name__ == '__main__':
    print(f"分辨率{get_this_dev_size()}")

    threading.Thread(target=timer, daemon=True).start() # 启动定时器

    try:
        while True:
            time.sleep(2)
            pic = screenshot()
            if not pic:
                continue
            t = get_task(cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR))
            if t is None:
                print("未识别到任务...")
                continue
            print(f"识别到任务{t.task_num.name}")
            # print(f"DEBUG:识别到的位置：{(t.pox)}")
            match t.task_num:
                case task.task1:
                    do_task.task1(t.pox)
                case task.task2:
                    do_task.task2()
                case task.task0:
                    do_task.task0()
                case task.task4:
                    do_task.task4()
                case task.task5:
                    do_task.task5()
                case task.task6:
                    do_task.task6()
                case task.task3:
                    do_task.task3(t.pox)
                case task.task7:
                    do_task.task7()
    except BaseException as e:
        import traceback

        print(f"发生异常：{e}")
        with open("error.log", "w") as a:
            a.write(traceback.format_exc())
        raise e
