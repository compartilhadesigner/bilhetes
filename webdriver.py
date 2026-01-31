from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
import sys
from selenium.webdriver.chrome.service import Service

class Webdriver:
    def __init__(self, download_directory, disable_images=True) -> None:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('window-size=1024x768')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument("--log-level=3")        # Apenas FATAL
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--start-maximized")

        # if disable_images:
        #     chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_directory,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.automatic_downloads": 1
            },
        )

        # WINDOWS 
        self.driver = webdriver.Chrome(options=chrome_options)

    def getDriver(self):
        return self.driver
