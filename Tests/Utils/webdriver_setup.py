

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver():
    ## headless mode
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(service= Service("C:/Users/A_R_T/AppData/Local/Drivers/chromedriver-win64/chromedriver.exe"), options=chrome_options)

    driver = webdriver.Chrome(service=Service("C:/Users/A_R_T/AppData/Local/Drivers/chromedriver-win64/chromedriver.exe"))
    driver.maximize_window()
    return driver

def open_url(driver, url):
    driver.get(url)