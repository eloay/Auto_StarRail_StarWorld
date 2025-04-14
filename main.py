from dataclasses import dataclass
from enum import Enum

from PIL.Image import Image
import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
import win32gui


@dataclass
class pox_result:
    x: int
    y: int
    val: float

    def __iter__(self):
        return iter([self.x, self.y])


def get_real_pox(pox: pox_result):
    dev = 1920, 1080
    this_dev = pyautogui.size().width, pyautogui.size().height
    return pox_result(pox.x / dev[0] * this_dev[0], pox.y / dev[1] * this_dev[1], pox.val)


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


def screenshot():
    window = gw.getWindowsWithTitle("崩坏：星穹铁道")[0]  # 替换成你目标窗口的标题
    if window and window.visible:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "崩坏：星穹铁道":
            print("截图失败")
            return False
        left, top, width, height = window.left, window.top, window.width, window.height
        return pyautogui.screenshot(region=(left, top, width, height))
    else:
        print("请打开游戏")
        return False


class control:
    @staticmethod
    def mouse_down(x, y):
        pyautogui.mouseDown(x, y)

    @staticmethod
    def mouse_up():
        pyautogui.mouseUp()

    @staticmethod
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


class photo_tool:
    @staticmethod
    def difference_blend(img1: Image, img2: Image):
        def pil_to_cv(img):
            """PIL → OpenCV"""
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

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
        control.mouse_down(964, 916)
        control.mouse_up()
        time.sleep(5)
        control.mouse_down(992, 905)
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
            control.mouse_down(x, y)
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
            control.mouse_down(*get_real_pox(pox_result(912, 765, 0.0)))
            control.mouse_up()
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


def get_task(img: Image):
    @dataclass
    class get_task_result:
        task_num: task
        pox: pox_result

    a, c = map(int, get_real_pox(pox_result(715, 1258, 0.0)))
    b, d = map(int, get_real_pox(pox_result(834, 951, 0.0)))
    t6 = pic_match(big_img=img[b:d, a:c], template=cv2.imread("img/start.png"))  # 可信度大约为7
    if t6.val > 0.65 and t6.val != 1.0:
        # print(111)
        return get_task_result(task.task6, t6)

    a, c = map(int, get_real_pox(pox_result(1574, 1919, 0.0)))
    b, d = map(int, get_real_pox(pox_result(0, 142, 0.0)))
    t5 = pic_match(big_img=img[b:d, a:c], template=cv2.imread("img/exit0.png"))  # 可信度大约为7
    if t5.val > 0.7 and t5.val != 1.0:
        return get_task_result(task.task5, t5)

    a, c = map(int, get_real_pox(pox_result(883, 1038, 0.0)))
    b, d = map(int, get_real_pox(pox_result(235, 273, 0.0)))
    t0 = pic_match(big_img=img[b:d, a:c], template=cv2.imread("img/0.png"))  # 可信度大约为7
    if t0.val > 0.6 and t0.val != 1.0:
        return get_task_result(task.task0, t0)

    t = pic_match(big_img=img, template=cv2.imread("img/a.png"))  # 可信度大约为7
    if t.val > 0.5 and t.val != 1.0:
        return get_task_result(task.task1, t)
    a, c = get_real_pox(pox_result(700, 850, 0.0))
    b, d = get_real_pox(pox_result(700, 850, 0.0))
    a, b, c, d = map(int, [a, b, c, d])
    t2 = pic_match(big_img=img[b:d, a:c], template=cv2.imread("img/b.png"))  # 可信度大约为8
    # print("task2", t2)
    if t2.val > 0.5 and t2.val != 1.0:
        return get_task_result(task.task2, t2)

    # all_point = [[1505, 786, 1630, 910], [1244, 388, 1398, 521],
    #              [632, 667, 755, 774], [1347, 662, 1554, 820],
    #              [78, 496, 258, 642], [536, 251, 699, 394], [301, 539, 462, 630]
    #     , ]
    #
    # for i in all_point:
    #     a, c = map(int, get_real_pox(pox_result(i[0], i[2], 0.0)))
    #     b, d = map(int, get_real_pox(pox_result(i[1], i[3], 0.0)))
    #     cv2.imwrite(f"test/{i[0]}.jpg",img[b:d, a:c])
    #     for j in range(4):
    #         t3 = pic_match(big_img=img[b:d, a:c], template=cv2.imread(f"img/c{j + 1}.png"))
    #
    #         print(t3.x, t3.y, t3.val)
    #         if t3.val > 0.7 and t3.val != 1.0 and t3.val != 0.0:
    #             print(f"成功识别到pic{j + 1},位于{t3.x},{t3.y}")
    #             return get_task_result(task.task3, t3)

    a, c = map(int, get_real_pox(pox_result(1245, 1412, 0.0)))
    b, d = map(int, get_real_pox(pox_result(867, 990, 0.0)))
    # cv2.imwrite("1.png", img[b:d, a:c])
    t4 = pic_match(big_img=img[b:d, a:c], template=cv2.imread("img/d.png"))  # 可信度大约为8
    # print("task2", t2)
    if t4.val < 0.5 and t4.val != 1.0 and t4.val != 0.0:
        return get_task_result(task.task4, t4)


pyautogui.failSafeCheck()
if __name__ == '__main__':
    while True:
        time.sleep(2)
        # print("任务开始")
        pic = screenshot()
        if not pic:
            continue
        # print("识别中...")
        t = get_task(cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR))
        if t is None:
            print("未识别到任务...")
            continue
        print(f"识别到任务{t.task_num.name}")
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
