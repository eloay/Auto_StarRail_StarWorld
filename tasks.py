import random
import time
from enum import Enum

import cv2
import numpy as np

import control
from control import Pox, get_real_pox
from picture import screenshot, pic_match, split_pic


def task0():  # 结算
    control.left_click(*get_real_pox(Pox(964, 916, val=0.0)))
    time.sleep(5)
    control.left_click(*get_real_pox(Pox(992, 905, val=0.0)))


def task1(point: Pox):  # 帕姆快送
    all_point = [[1457, 377],
                 [1615, 719],
                 [1278, 714],
                 [1032, 876],
                 [631, 625],
                 [483, 763],
                 [345, 507],
                 [797, 230],
                 [1174, 249]]

    print("正在收集帕姆快送中...")
    for i in all_point:
        control.drag(*get_real_pox(point), *get_real_pox(Pox(i[0], i[1],0.0)))


def task2():  # 来宾事件
    control.left_click(*get_real_pox(Pox(796, 742, 0.0)))
    time.sleep(3)
    control.left_click(*get_real_pox(Pox(1638, 830, 0.0)))
    time.sleep(3)
    control.left_click(*get_real_pox(Pox(1616, 965, 0.0)))
    time.sleep(7)
    control.left_click(*get_real_pox(Pox(1749, 961, 0.0)))
    time.sleep(0.5)


def task4():  # 薅鸟毛
    control.left_click(*get_real_pox(Pox(1319, 915, 0.0)))
    time.sleep(2)
    start_time = time.time()
    while start_time + 10 > time.time():
        control.left_click(*get_real_pox(Pox(912, 765, 0.0)), duration=0)
    time.sleep(3)


def task5():  # 误触管理恢复
    control.left_click(*get_real_pox(Pox(1773, 85, 0.0)))


def task6():  # 新一轮开启失败恢复
    control.left_click(*get_real_pox(Pox(991, 902, 0.0)))


def task3(point: Pox):
    control.left_click(*get_real_pox(Pox(point.x, point.y, 0.0)))


def task7(disable_glod=False, disable_diamonds=False):  # 抽卡&角色升级
    # 打开抽卡页面
    control.left_click(*get_real_pox(Pox(1663, 948, 0.0)))
    time.sleep(2)

    while True:  # 抽炫彩
        img = np.array(screenshot())
        t7 = pic_match(big_img=split_pic(img, (1277, 739), (1277 + 224, 739 + 35)),
                       template=cv2.imread("img/c7.png"))
        if t7.val > 0.8 and t7.val != 1.0:
            gacha(1386)
        else:
            break

    time.sleep(2)

    if not disable_glod:
        while True:  # 抽贵金
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (872, 742), (869 + 210, 742 + 32)),
                           template=cv2.imread("img/c7_4.png"))
            if t7.val > 0.8 and t7.val != 1.0:
                gacha(983)
            else:
                break
        time.sleep(2)

    if not disable_diamonds:
        while True:  # 使用钻石抽卡或单次抽卡
            img = np.array(screenshot())
            t7 = pic_match(big_img=split_pic(img, (1387, 801), (1387 + 119, 801 + 36)),
                           template=cv2.imread("img/c7_5.png"))
            if t7.val > 0.8 and t7.val != 1.0:
                gacha(1386)
            else:
                break
        time.sleep(2)

    while True:  # 避免抽卡无法退出
        img = np.array(screenshot())
        t7 = pic_match(big_img=split_pic(img, (99, 64), (99 + 58, 64 + 33)), template=cv2.imread("img/c7_3.png"))
        if t7.val > 0.7 and t7.val != 1.0:
            control.left_click(*get_real_pox(Pox(1860, 66, 0.0)))
            time.sleep(0.5)
        else:
            break

    time.sleep(2)
    control.left_click(*get_real_pox(Pox(1849, 803, 0.0)))  # 一键收取
    time.sleep(1)
    control.left_click(*get_real_pox(Pox(1796, 940, 0.0)))  # 会场管理
    time.sleep(1)

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
    while True:  # 循环升级角色直到没有升级
        for point in random.sample(all_points, len(all_points)):  # 随机打乱升级顺序
            control.left_click(*get_real_pox(Pox(point[0], point[1], 0.0)))
            time.sleep(0.2)
            if not upgrade():
                break
        break

    time.sleep(2)

    while True:  # 避免无法退出升级页面
        img = np.array(screenshot())
        t7 = pic_match(big_img=split_pic(img, (1574, 0), (1919, 142)), template=cv2.imread("img/exit0.png"))
        if t7.val > 0.7 and t7.val != 1.0:
            control.left_click(*get_real_pox(Pox(1760, 86, 0.0)))
            time.sleep(0.5)
        else:
            break


def gacha(poll_x: int):  # 抽卡
    control.left_click(*get_real_pox(Pox(poll_x, 819, 0.0)))
    time.sleep(2)
    control.left_click(*get_real_pox(Pox(1809, 65, 0.0)))
    time.sleep(3)
    control.left_click(*get_real_pox(Pox(1809, 65, 0.0)))
    time.sleep(2)


def upgrade():  # 升级角色
    img = np.array(screenshot())
    t7 = pic_match(big_img=split_pic(img, (1347, 856), (1347 + 314, 856 + 46)),
                   template=cv2.imread("img/c7_2.png"))
    if t7.val > 0.6 and t7.val != 1.0:
        control.left_click(*get_real_pox(Pox(1502, 876, 0.0)))
        return True
    else:
        return False


class Task(Enum):
    task0 = 0x0  # 结算
    task1 = 0x01  # 帕姆快送
    task2 = 0x02  # 来宾事件
    task3 = 0x03  # 特殊来宾 暂未实现
    task4 = 0x04  # 薅鸟毛
    task5 = 0x05  # 误触管理恢复
    task6 = 0x06  # 新一轮开启失败恢复
    task7 = 0x07  # 抽卡&角色升级
