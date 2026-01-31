import time
import re
from models.DataManager import DataManager
from selenium.webdriver.common.keys import Keys

class BR365Bet:
    def __init__(self, webdriver, websiteName: str):
        self.webdriver = webdriver
        self.websiteName = websiteName
        self.betAmount = 20
        self.pinId = None
        self.profit = None
    
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
        input = self.webdriver.execute_script(
            """return document.querySelectorAll("[role='spinbutton']")[0]"""
        )
        input.clear()
        input.send_keys(self.betAmount)
        input.send_keys(Keys.TAB)

        time.sleep(2)

        raw_profit = self.webdriver.execute_script(
        """
            const netValue = [...document.querySelectorAll('div')]
                .find(el => el.textContent.trim() === 'Ret. líquido:')
                ?.parentElement
                .querySelector('.p-button-label')
                ?.textContent
                .trim() || null;

            return netValue;
        """)
        self.profit = self.__parse_money(raw_profit)

        nameInput = self.webdriver.execute_script("""
            const nameInput = [...document.querySelectorAll('div.font-semibold')]
            .find(el => el.textContent.replace('*', '').trim().startsWith('Nome'))
            ?.parentElement
            .querySelector('input[type="text"]') || null;

            return nameInput;
        """)
        nameInput.send_keys("Palpite Diário")

        self.webdriver.execute_script('document.getElementById("concluir").click()')

        time.sleep(2)

        saveButton = self.webdriver.execute_script("""
            const saveButton = [...document.querySelectorAll('button')]
            .find(btn => btn.textContent.trim() === 'Salvar') || null;

            return saveButton;
        """)
        saveButton.click()

        time.sleep(3)

        self.pinId = self.webdriver.execute_script("""
            const code = document
            .querySelector('#swal2-html-container strong')
            ?.textContent.trim() || null;

            return code;
        """)

        manager = DataManager()
        manager.add({
            "code": self.pinId,
            "customer": self.websiteName,
            "betAmount": self.betAmount,
            "profit": self.profit,
            "print": f"{self.websiteName}.png"
        })
