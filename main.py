import time

import cv2
import numpy as np
import pyautogui
import random
from PIL.Image import Image

import control
import tasks
from control import get_this_dev_size
from picture import split_pic, pic_match, screenshot
from tasks import Task
from ucClient import ucClient

task7_timer = 3600  # 任务7的定时器，默认3600秒（1小时）
task7_lastRun = -1  # 任务7的上次运行时间


def get_task(img: Image, debug_mode=False) -> tuple:
    global task7_lastRun  # 任务7的定时器

    if time.time() - task7_lastRun > task7_timer:
        task7_lastRun = time.time()  # 重置定时器
        return Task.task7, None

    start_pic_match = pic_match(big_img=split_pic(img, (715, 834), (1258, 951)),
                                template=cv2.imread("img/start.png"))  # 可信度大约为7
    if debug_mode:
        cv2.imwrite(f"debug/img_task6.jpg", split_pic(img, (715, 834), (1258, 951)))
    if start_pic_match.val > 0.65 and start_pic_match.val != 1.0:
        # 新一轮开启失败恢复
        return Task.task6, start_pic_match

    exit_management_pic_match = pic_match(big_img=split_pic(img, (1574, 0), (1919, 142)),
                                          template=cv2.imread("img/exit0.png"))  # 可信度大约为7
    if debug_mode:
        cv2.imwrite(f"debug/img_task5.jpg", split_pic(img, (1574, 0), (1919, 142)))
    if exit_management_pic_match.val > 0.7 and exit_management_pic_match.val != 1.0:
        # 误触管理恢复
        return Task.task5, exit_management_pic_match

    # 结算
    t0 = pic_match(big_img=split_pic(img, (883, 235), (1038, 273)), template=cv2.imread("img/0.png"))  # 可信度大约为7
    if debug_mode:
        cv2.imwrite(f"debug/img_task0.jpg", split_pic(img, (883, 235), (1038, 300)))
        print(f"当前可信度task0可信度{t0.val}")
    if t0.val > 0.6 and t0.val != 1.0:
        return Task.task0, t0

    # 帕姆快送
    t1 = pic_match(big_img=img, template=cv2.imread("img/a.png"))  # 可信度大约为7
    if t1.val > 0.5 and t1.val != 1.0:
        return Task.task1, t1

    # 来宾事件
    t2 = pic_match(big_img=split_pic(img, (700, 700), (850, 850)), template=cv2.imread("img/b.png"))  # 可信度大约为8
    if debug_mode:
        cv2.imwrite(f"debug/img_task2.jpg", split_pic(img, (700, 700), (850, 850)))
    if t2.val > 0.5 and t2.val != 1.0:
        return Task.task2, t2

    # 薅鸟毛
    t4 = pic_match(big_img=split_pic(img, (1245, 867), (1412, 990)), template=cv2.imread("img/d.png"))  # 可信度大约为8
    if debug_mode:
        cv2.imwrite(f"debug/img_task4.jpg", split_pic(img, (1245, 867), (1412, 990)))
    if t4.val < 0.5 and t4.val != 1.0 and t4.val != 0.0:
        return Task.task4, t4

    # 如果上面的都没有匹配到，20%的概率匹配到特殊来宾
    if random.random() <= 0.2:
        return Task.task3, None


pyautogui.failSafeCheck()
if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    import argparse

    parser = argparse.ArgumentParser(description='Auto StarWorld')
    parser.add_argument('--debug', action='store_true', help='debug模式')
    parser.add_argument('--timer-seconds', type=int, default=3600, help='定时器时间')
    parser.add_argument('--disable-glod', action='store_true', help='禁止自动抽取贵金邀约')
    parser.add_argument('--disable-common', action='store_true', help='禁止自动抽取标准邀约')
    parser.add_argument('--disable-use-diamonds', action='store_true', help='禁止使用钻石抽取')
    parser.add_argument('--cloudgame', action='store_true', help='使用云游戏')
    # args = parser.parse_args()
    args, _ = parser.parse_known_args()

    try:
        if args.cloudgame:
            print("云游戏模式: 正在启动云游戏......")
            print("云游戏模式: 请确保Chrome 135 已安装且被添加至系统PATH中，并添加cookie至cookie.json中")
            control.CloudGameClient = ucClient()
            print("云游戏模式: 已自动启动云游戏,请在云游戏中打开星铁World。")
            input("请在云游戏中打开星铁World,按Enter继续...")

        print(f"分辨率: {get_this_dev_size()}")

        task7_timer = args.timer_seconds  # 设置定时器时间
        task7_lastRun = time.time()

        while True:
            # 主循环
            time.sleep(2)
            pic = screenshot()
            if not pic:
                print("获取截图失败...")
                continue

            task = get_task(
                cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR),
                debug_mode=args.debug
            )
            if task is None:
                print("未识别到任务...")
                continue

            task_names = ["结算", "帕姆快送", "来宾事件", "特殊来宾", "薅鸟毛",
                          "误触管理恢复", "新一轮开启失败恢复", "抽卡&角色升级"]
            print(f"识别到任务{task_names[task[0].value]}")
            # print(f"DEBUG:识别到的位置：{(t.pox)}")

            match task[0]:
                case Task.task0:
                    tasks.task0()
                case Task.task1:
                    tasks.task1(task[1])
                case Task.task2:
                    tasks.task2()
                case Task.task3:
                    tasks.task3()
                case Task.task4:
                    tasks.task4()
                case Task.task5:
                    tasks.task5()
                case Task.task6:
                    tasks.task6()
                case Task.task7:
                    tasks.task7(
                        disable_common=args.disable_common,
                        disable_glod=args.disable_glod,
                        disable_diamonds=args.disable_use_diamonds
                    )
    except BaseException as e:
        import traceback

        print(f"发生异常：{e}")
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        raise e

    input()
