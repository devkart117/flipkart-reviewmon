#!venv/bin/python3

import time
import copy
import json
import utils.config as _
from datetime import datetime

from loguru import logger

from utils import (send_output_mail, 
                   send_email, 
                   send_error_mail, 
                   get_flipkart_data, 
                   save_data, 
                   get_chromedriver_without_proxy)

from exceptions.product import ProductUnavailable
from portals.flipkart import get_review_information


if __name__ == '__main__':

    logger.info('Starting script')

    send_email('Notification System <dev@kartikcodes.in>', ['dev.kartikaggarwal117@gmail.com'], 'Flipkart Reviewmon Execute!', 'Flipkart Reviewmon Script has started execution!', [])

    with open('data/latest.json', 'r') as f:
        latest_review_data = json.load(f)

    latest_date = latest_review_data.get('date') or 'NA'
    today_date = datetime.today().strftime('%d-%m-%y')

    output = []

    # Fetch Data
    try:
        logger.info('Loading data')
        flipkart_data = get_flipkart_data()
    except Exception as e:
        logger.error(e)
        send_error_mail('[Flipkart Reviewmon] Error while loading data from google sheet')

    driver = get_chromedriver_without_proxy()


    for index, entry in enumerate(flipkart_data):
        
        ID = entry['Id']
        SKU = entry['SKU']
        URL = entry['Url']

        if not isinstance(URL, str) or URL.strip() == '':
            logger.warning(f'[{index+1}/{len(flipkart_data)}] skipping fkipkart product, URL: {URL}')
            continue

        count = 0
        while True:
            try:
                scraped_info = get_review_information(driver, URL)
                break
            except ProductUnavailable:
                scraped_info = {
                    'overall': 'NA',
                    5: 'NA',
                    4: 'NA',
                    3: 'NA',
                    2: 'NA',
                    1: 'NA'
                }
                break
            except Exception:
                if count > 1:
                    scraped_info = {
                        'overall': 'NA',
                        5: 'NA',
                        4: 'NA',
                        3: 'NA',
                        2: 'NA',
                        1: 'NA'
                    }
                    break
                count += 1
                time.sleep(2)
                continue

        latest_product_info = latest_review_data.get(ID)
        if not latest_product_info:
            latest_product_info = {
                'overall': 'NA',
                "5": 'NA',
                "4": 'NA',
                "3": 'NA',
                "2": 'NA',
                "1": 'NA'
            }

        latest_product_info = copy.deepcopy(latest_product_info)

        new_info = {
            'ID': ID,
            'SKU': SKU,
            'URL': URL,
            f'Overall rating ({latest_date})': latest_product_info['overall'],
            f'Overall rating ({today_date})': scraped_info['overall'],
            f'5 star ratings ({latest_date})': latest_product_info["5"],
            f'5 star ratings ({today_date})': scraped_info[5],
            f'4 star ratings ({latest_date})': latest_product_info["4"],
            f'4 star ratings ({today_date})': scraped_info[4],
            f'3 star ratings ({latest_date})': latest_product_info["3"],
            f'3 star ratings ({today_date})': scraped_info[3],
            f'2 star ratings ({latest_date})': latest_product_info["2"],
            f'2 star ratings ({today_date})': scraped_info[2],
            f'1 star ratings ({latest_date})': latest_product_info["1"],
            f'1 star ratings ({today_date})': scraped_info[1],
        }

        output.append(new_info)

        latest_review_data[ID] = {
            'overall': scraped_info['overall'],
            1: scraped_info[1],
            2: scraped_info[2],
            3: scraped_info[3],
            4: scraped_info[4],
            5: scraped_info[5],
        }

        logger.debug(f'[{index+1}/{len(flipkart_data)}] Scraped review information: {URL} | {new_info}')


    driver.close()

    logger.info('Data scraping complete, saving...')

    save_data(output)

    logger.info('Emailing data...')

    send_output_mail()

    logger.info('Updating latest info...')

    latest_review_data['date'] = today_date

    with open('data/latest.json', 'w') as f:
        json.dump(latest_review_data, f, indent=4)

    logger.info('Script has run to completion!')
