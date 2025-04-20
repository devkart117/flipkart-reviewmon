import os

import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


WEB_DRIVER_WAIT_TIMEOUT = 10


def _driver_wrapper(f):
    def wrapper(*args, **kwargs):
        driver: webdriver.Chrome = f(*args, **kwargs)

        driver.maximize_window()
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        return driver
    
    return wrapper


def _get_chrome_options():
    chrome_options = uc.ChromeOptions()

    chrome_options.add_argument(f"--user-data-dir={os.path.join(os.getcwd(), 'user_data_dir')}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--headless=new")

    return chrome_options


@_driver_wrapper
def get_chromedriver_without_proxy() -> webdriver.Chrome:
    chrome_options = _get_chrome_options()
    driver = uc.Chrome(options=chrome_options, driver_executable_path=ChromeDriverManager().install())
    return driver