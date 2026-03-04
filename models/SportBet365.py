import time
import re
from models.DataManager import DataManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from models.Logger import Logger

class SportBet365:
    def __init__(self, webdriver, websiteName: str, bil_num = 1):
        self.webdriver = webdriver
        self.websiteName = websiteName
        self.betAmount = 20
        self.pinId = None
        self.profit = None
        self.bil_num = bil_num
    
    def __parse_money(self, s: str) -> float:
        num = re.search(r"[\d.,]+", s).group()

        last_dot = num.rfind(".")
        last_comma = num.rfind(",")

        if last_dot > last_comma:
            num = num.replace(",", "")
        else:
            num = num.replace(".", "").replace(",", ".")

        return float(num)

    def get_bet_data(self):
        Logger.info("Aguardando a seleção de times!")

        input("\033[94mPressione ENTER quando selecionar os times...\033[0m")
    
        _input = self.webdriver.execute_script(
            "return document.getElementById('valorApostado')"
        )
        _input.clear()
        _input.send_keys(self.betAmount)
        _input.send_keys(Keys.TAB)

        time.sleep(4)

        self.webdriver.execute_script("document.getElementById('btnApostar')?.click()")

        time.sleep(3)

        self.pinId = self.webdriver.execute_script("""
            const container = document.getElementById('swal2-html-container');

            const h3Text = container.querySelector('h3')?.textContent || null;
            return h3Text;
        """)

        self.webdriver.get(f"https://sportbet365.site/acompanhar?c={self.pinId}")
        WebDriverWait(self.webdriver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        Logger.info("Aguardando o print!")

        input("\033[94mPressione ENTER quando salvar o print...\033[0m")

        raw_profit = self.webdriver.execute_script("""
            const value = [...document.querySelectorAll('span.tag-t1')]
            .find(span => span.textContent.trim() === 'Possível retorno')
            ?.parentElement.querySelector('#txtPremio')
            ?.textContent
            .trim() || null;

            return value;
        """)
        self.profit = self.__parse_money(raw_profit)

        time.sleep(1)

        manager = DataManager()
        manager.add({
            "code": self.pinId,
            "customer": self.websiteName,
            "betAmount": self.betAmount,
            "profit": self.profit,
            "print": f"{self.websiteName}{self.bil_num}.png"
        })
