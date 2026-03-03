from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

def capturar_screenshot_elemento(driver, seletor, tipo_seletor=By.CSS_SELECTOR, nome_arquivo="elemento.png"):
    """
    Captura screenshot de um elemento específico.
    
    Args:
        driver: Instância do WebDriver do Selenium
        seletor: String com o seletor do elemento (CSS, XPath, etc)
        tipo_seletor: Tipo do seletor (By.CSS_SELECTOR, By.XPATH, By.ID, etc)
        nome_arquivo: Nome do arquivo para salvar o screenshot
    
    Returns:
        str: Caminho do arquivo salvo
    """
    try:
        # Aguarda o elemento estar presente
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((tipo_seletor, seletor))
        )
        
        # Captura screenshot apenas do elemento
        elemento.screenshot(nome_arquivo)
        
        print(f"Screenshot salvo como: {nome_arquivo}")
        return nome_arquivo
        
    except Exception as e:
        print(f"Erro ao capturar screenshot: {e}")
        return None


def capturar_screenshot_elemento_cortado(driver, seletor, tipo_seletor=By.CSS_SELECTOR, nome_arquivo="elemento.png"):
    """
    Método alternativo: captura screenshot da página inteira e recorta o elemento.
    Útil para navegadores que não suportam element.screenshot()
    
    Args:
        driver: Instância do WebDriver do Selenium
        seletor: String com o seletor do elemento
        tipo_seletor: Tipo do seletor
        nome_arquivo: Nome do arquivo para salvar
    
    Returns:
        str: Caminho do arquivo salvo
    """
    try:
        # Aguarda o elemento estar presente
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((tipo_seletor, seletor))
        )
        
        # Captura screenshot da página inteira
        screenshot = driver.get_screenshot_as_png()
        
        # Obtém localização e tamanho do elemento
        location = elemento.location
        size = elemento.size
        
        # Abre a imagem com PIL
        img = Image.open(io.BytesIO(screenshot))
        
        # Recorta apenas o elemento
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        
        img_cortada = img.crop((left, top, right, bottom))
        img_cortada.save(nome_arquivo)
        
        print(f"Screenshot salvo como: {nome_arquivo}")
        return nome_arquivo
        
    except Exception as e:
        print(f"Erro ao capturar screenshot: {e}")
        return None
    
WEBSITES = [
  {
    "name": "JOGABET",
    "link": "https://jogabets.com.br/sistema_v2/usuarios/simulador/desktop/jogos.aspx?idesporte=102&idcampeonato=574908",
    "isSA": True,
  },
  {
    "name": "BBS",
    "link": "https://bbsesportes.com.br/sistema_v2/usuarios/simulador/desktop/jogos.aspx?idesporte=102&idcampeonato=574908",
    "isSA": True,
  },
  {
    "name": "NACIONAL",
    "link": "https://nacionalbet.app/sistema_v2/usuarios/simulador/desktop/Jogos.aspx?idesporte=102&idcampeonato=574908",
    "isSA": True,
  },
  {
    "name": "DS 365",
    "link": "https://dsesportes365.com/sistema_v2/usuarios/simulador/desktop/jogos.aspx?idesporte=102&idcampeonato=574908",
    "isSA": True,
  },
  {
    "name": "DS ESPORTES",
    "link": "https://dsesportes.bet/sistema_v2/usuarios/simulador/desktop/jogos.aspx?idesporte=102&idcampeonato=574908",
    "isSA": True,
  },
  # {
  #   "name": "B2X",
  #   "link": "https://b2x.bet.br/sports?tab=Early"
  # },
  # {
  #   "name": "365BR",
  #   "link": "https://b365br.com/#/"
  # },
  {
    "name": "CENTRAL BET",
    "link": "https://centralbet.site/v3/"
  },
  {
    "name": "SYMBET",
    "link": "https://symbet.vip/"
  },
  {
    "name": "SPORTBET365",
    "link": "https://sportbet365.site/v3/"
  }
]
