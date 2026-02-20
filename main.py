from webdriver import Webdriver
from utils import WEBSITES
from models.Logger import Logger
from models.SAWebsite import SAWebsite
from models.B2XWebsite import B2XWebsite
from models.CentralBet import CentralBet
from models.SymBet import SymBet
from models.SportBet365 import SportBet365
from models.BR365 import BR365Bet
from selenium.webdriver.support.ui import WebDriverWait

with open("dados.json", "w", encoding="utf-8") as f:
    pass

def get_bet_data(webdriver):
    if not webdriver:
        return None

for website in WEBSITES:
    bil_count = int(input(f"Quantos bilhetes para o site {website['name']}? "))

    driver = Webdriver('').getDriver()

    for bil in range(bil_count):
        Logger.debug(f"Iniciando a extração do bilhete {bil + 1} do site {website['name']}")

        driver.get(website['link'])

        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        Logger.info("Aguardando a seleção de times!")

        input("\033[94mPressione ENTER quando selecionar os times e salvar o print...\033[0m")

        if 'isSA' in website and website['isSA']:
            sa = SAWebsite(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            sa.get_bet_data()

        if website['name'] == 'B2X':
            b2x = B2XWebsite(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            b2x.get_bet_data()

        if website['name'] == 'CENTRAL BET':
            cb = CentralBet(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            cb.get_bet_data()

        if website['name'] == 'SYMBET':
            sb = SymBet(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            sb.get_bet_data()

        if website['name'] == 'SPORTBET365':
            s365 = SportBet365(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            s365.get_bet_data()

        if website['name'] == '365BR':
            b365 = BR365Bet(webdriver=driver, websiteName=website['name'], bil_num=bil+1)
            b365.get_bet_data()

    driver.close()

Logger.success(f"FINALIZADO COM SUCESSO!")
