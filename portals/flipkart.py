import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions.product import ProductUnavailable


def get_review_information(driver: webdriver.Chrome, product_link: str):

    driver.get(product_link)

    rating_info = {
        'overall': 'NA',
        5: 'NA',
        4: 'NA',
        3: 'NA',
        2: 'NA',
        1: 'NA'
    }

    try:
        overall_stars = driver.find_element(By.CLASS_NAME, 'ipqd2A').get_attribute('innerText').strip()
    except:
        raise ProductUnavailable(product_link)

    ratings_and_reviews_divs = driver.find_elements(By.CLASS_NAME, 'j-aW8Z')

    ratings = ratings_and_reviews_divs[0].get_attribute('innerText').strip()
    reviews = ratings_and_reviews_divs[1].get_attribute('innerText').strip()

    overall = f'{overall_stars} - {ratings} {reviews}'

    count_divs = driver.find_elements(By.CLASS_NAME, 'BArk-j')
    five_star = count_divs[0].get_attribute('innerText').strip()
    four_star = count_divs[1].get_attribute('innerText').strip()
    three_star = count_divs[2].get_attribute('innerText').strip()
    two_star = count_divs[3].get_attribute('innerText').strip()
    one_star = count_divs[4].get_attribute('innerText').strip()

    rating_info = {
        'overall': overall,
        5: five_star,
        4: four_star,
        3: three_star,
        2: two_star,
        1: one_star
    }

    return rating_info