# import atexit
import json
import logging
import os
import io
import time

import selenium.common.exceptions as Exceptions
import undetected_chromedriver as uc
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def getCookies(cookiesFilePath: str) -> list:
    remapper = {"lax": "Lax", "strict": "Strict", "no_restriction": "None", "unspecified": "None", None: "None"}
    with open(cookiesFilePath, "r", encoding="utf-8") as cookiesFile:
        cookies = json.load(cookiesFile)
    for i in range(len(cookies)):
        cookies[i]["sameSite"] = remapper.get(cookies[i]["sameSite"], "None")
    return cookies


class ucClient:
    browser: uc.Chrome = None
    canvas_element: uc.WebElement = None
    width: int = None
    height: int = None

    def click_element(self, by: str, vaule: str, timeout: int = 5, maximum_times=1, index: int = 0) -> bool:
        try:
            for _ in range(maximum_times):
                button_to_skip = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located((by, vaule))
                )
                self.browser.find_elements(by, vaule)[index].click()
                logging.info(f"Passed {vaule}")
            return True
        except Exceptions.TimeoutException:
            logging.info(f"Skipped {vaule}")
            return False
        except Exception as exp:
            logging.error(f"Something unexpected happened when passing {vaule}: {exp}")
            return False

    # @atexit.register
    # def save_cookie(self):
    #     cookies = self.browser.get_cookies()
    #     with open("cookie.json", "w", encoding="utf-8") as f:
    #         json.dump(cookies, f, ensure_ascii=False, indent=4)
    #         logging.info("Saved cookies to cookie.json")

    def click(self, x: int, y: int):
        action = (ActionChains(self.browser).move_to_element(self.canvas_element).
                  move_by_offset(int(x - self.width / 2), int(y - self.height / 2)).click())
        action.perform()

    def drag(self, start_x, start_y, end_x, end_y):
        action = (ActionChains(self.browser).move_to_element(self.canvas_element).
                  move_by_offset(int(start_x - self.width / 2), int(start_y - self.height / 2)).click_and_hold())
        action.move_by_offset(int(end_x - start_x), int(end_y - start_y)).release()
        action.perform()

    def screenshot(self) -> Image.Image:
        return Image.open(io.BytesIO(self.canvas_element.screenshot_as_png)).resize((1920, 1080))

    def __init__(self, height=432, width=768):
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
            level=logging.WARNING
        )
        self.width = width
        self.height = height

        options = uc.ChromeOptions()
        # options.add_argument(
        #     "--User-Agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) "
        #     "Chrome/135.0.0.0 Mobile Safari/537.36")
        self.browser = uc.Chrome(use_subprocess=False, options=options)
        self.browser.set_window_size(width + 40, height + 95)
        self.browser.get("https://sr.mihoyo.com/cloud/#/")

        self.browser.delete_all_cookies()
        if os.path.exists("cookie.json"):
            cookies = getCookies("cookie.json")
            for cookie in cookies:
                if cookie["name"] == "__Host-next-auth.csrf-token":
                    continue
                self.browser.add_cookie(cookie)

        # skip guides
        self.click_element(By.XPATH, "//button[//div[//span[text()='下次再说']]]")
        self.click_element(By.XPATH, "//button[//div[//span[text()='我知道了']]]")
        self.click_element(By.CLASS_NAME, "guide-close-btn")
        self.click_element(By.CLASS_NAME, "clg-card__close-btn")

        # start game
        if not self.click_element(By.CLASS_NAME, "wel-card__content--start", timeout=30):
            print("没有找到开始按钮")
            raise Exception("没有找到开始按钮")

        # adjust the canvas size
        time.sleep(10)
        self.browser.execute_script(f"canvasElement = document.getElementById("
                                    f"'canvas-player');canvasElement.style.aspectRatio='16/9';canvasElement.style.height='{height}px';canvasElement.style.width='{width}px';")

        # skip guide
        if self.click_element(By.XPATH, "//div[text()='下一步（1/3）']", timeout=10, index=0):
            self.click_element(By.XPATH, "//div[text()='下一步（2/3）']", index=1)
            self.click_element(By.XPATH, "//div[text()='我知道了（3/3）']", index=2)

        # accept agreement
        self.click_element(By.XPATH, "//button[//div[//span[text()='接受']]]", timeout=10, index=-1)

        self.canvas_element = self.browser.find_element(By.ID, "canvas-player")
        pass
