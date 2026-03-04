from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import re 
from urllib.parse import urlparse, parse_qs
from models.DataManager import DataManager
from models.Logger import Logger

class B2XWebsite:
    def __init__(self, webdriver, websiteName: str, bil_num = 1):
        self.webdriver = webdriver
        self.websiteName = websiteName
        self.betAmount = 20
        self.pinId = None
        self.profit = None
        self.bil_num = bil_num
        
    def __parse_link(self, url: str) -> str:
        query = parse_qs(urlparse(url).query)
        code = query.get("bscode", [None])[0]
    
        return code
    
    def __parse_money(self, s: str) -> float:
        num = re.search(r"[\d.,]+", s).group()

        last_dot = num.rfind(".")
        last_comma = num.rfind(",")

        if last_dot > last_comma:
            num = num.replace(",", "")
        else:
            num = num.replace(".", "").replace(",", ".")

        return float(num)

    def save_screenshot(self):
        wait = WebDriverWait(self.webdriver, 10)

        iframe = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        self.webdriver.switch_to.frame(iframe)
        
        time.sleep(1)

        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", f"{self.websiteName}.png")
        
        wait = WebDriverWait(self.webdriver, 20)
        
        element = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "betslip_fe_AllBetsContainerSecondary_allBets__container")
            )
        )

        element.screenshot(path)

        return path

    def set_bet_value(self, value):
        wait = WebDriverWait(self.webdriver, 10)

        input_el = wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "betslip_fe_CounterSecondary_input")
            )
        )

        input_el.clear()
        time.sleep(1)
        el = self.webdriver.find_element(By.CLASS_NAME, "betslip_fe_CounterSecondary_input")
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)

        time.sleep(1)

        raw_profit = self.webdriver.execute_script("return document.getElementsByClassName('betslip_fe_AmountBlockSecondary_totalReturnContainer')[0].textContent")

        profit = self.__parse_money(raw_profit)
        self.profit = profit

    def get_link(self):
        self.webdriver.execute_script("document.getElementsByClassName('sportsbook-Button')[1].click()")
        time.sleep(2)
        link = pyperclip.paste()
        code = self.__parse_link(url=link)
        if code:
            self.pinId = code

    def get_bet_data(self):        
        Logger.info("Aguardando a seleção de times!")

        input("\033[94mPressione ENTER quando selecionar os times e salvar o print...\033[0m")
        
        self.set_bet_value(self.betAmount)
        self.get_link()

        manager = DataManager()
        manager.add({
            "code": self.pinId,
            "customer": self.websiteName,
            "betAmount": self.betAmount,
            "profit": self.profit,
            "print": f"{self.websiteName}{self.bil_num}.png"
        })
