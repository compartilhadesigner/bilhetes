import time
from selenium.webdriver.common.by import By
from models.DataManager import DataManager
from models.Logger import Logger

class SAWebsite:
    def __init__(self, webdriver, websiteName: str, bil_num = 1):
        self.webdriver = webdriver
        self.websiteName = websiteName
        self.betAmount = 20
        self.bil_num = bil_num

    def get_bet_data(self):
        Logger.info("Aguardando a seleção de times!")

        input("\033[94mPressione ENTER quando selecionar os times e salvar o print...\033[0m")
    
        driver = self.webdriver

        betslip_items = driver.find_elements(By.CLASS_NAME, "betslip-item")
        if not betslip_items:
            return None

        input_valor = driver.find_element(By.ID, "txtValorAposta")
        input_valor.clear()
        input_valor.send_keys(self.betAmount)

        time.sleep(1)

        profit = driver.execute_script("""
            const el = document.getElementById("lblPossivelRetorno");
            if (!el) return null;

            const raw = el.textContent.trim();

            return parseFloat(
                raw
                .replace(/[^\d,.-]/g, "") // remove R$, espaços, etc
                .replace(/\./g, "")       // remove separador de milhar
                .replace(",", ".")        // vírgula -> ponto
            );
        """)

        driver.execute_script("""
            const buttonFinish = document.getElementById("btnFinalizar");
            buttonFinish?.click()
        """)

        time.sleep(2)

        has_notification = driver.execute_script("""
            return document.getElementsByClassName("notification").length > 0;
        """)

        if has_notification:
            driver.execute_script("""
                document.getElementsByClassName("notification-header-close")[0]?.click();
            """)
            time.sleep(1)
            driver.execute_script("""
                const buttonFinish = document.getElementById("btnFinalizar");
                buttonFinish?.click();
            """)

        time.sleep(10)

        pinId = driver.execute_script("""
            const pinId = document.getElementById("pinId")
            return pinId.textContent;
        """)

        manager = DataManager()
        manager.add({
            "code": pinId,
            "customer": self.websiteName,
            "betAmount": self.betAmount,
            "profit": profit,
            "print": f"{self.websiteName}{self.bil_num}.png"
        })
