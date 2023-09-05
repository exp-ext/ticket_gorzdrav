import logging
import os
import sys
import time
from typing import List

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filename='./main.log',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = os.getenv('URL')
RETRY_TIME = int(os.getenv('RETRY_TIME'))
DOCTORS = os.getenv('DOCTORS').split(',')


def send_message(message: str) -> None:
    """
    Отправляет сообщение в чат Telegram.

    ### Args:
        - message (`str`): Сообщение, которое необходимо отправить в чат.
    """
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}'
    try:
        response = requests.post(url)
        logger.info(f'Сообщение "{message}" успешно отправлено.')
    except Exception as error:
        logger.error(f'{response}. Дополнительно: {error}')


def check_gorzdrav(url: str) -> List[str]:
    """
    Проверяет доступность номерков в различных специальностях на веб-странице Gorzdrav.

    ### Args:
        - url (`str`): URL-адрес веб-страницы для проверки.

    ### Return:
        - response (`List[str]`): Список строк с информацией о доступности номерков в специальностях.
        Формат каждой строки: "Специальность - количество номерков".

    """

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # для Chrome
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    driver.implicitly_wait(15)
    specialties = driver.find_elements(By.CLASS_NAME, 'service-speciality')

    response = []

    for specialty in specialties:
        try:
            specialty_name = specialty.find_element(By.CLASS_NAME, 'service-speciality__title').text.strip()
            tickets = specialty.find_element(By.CLASS_NAME, 'service-speciality__tickets').text.strip()
            response.append(f'{specialty_name} -{tickets.replace("Доступных номерков:", "")}')
        except NoSuchElementException:
            pass
    driver.quit()
    return response


def main():
    """
    Основная функция для мониторинга данных на веб-странице Gorzdrav и отправки уведомлений в случае изменений.

    Функция бесконечно мониторит данные на веб-странице, сравнивая их с предыдущими данными,
    и отправляет уведомления в Telegram в случае обнаружения изменений.
    """
    previous_data = []

    while True:
        try:
            overwrite = False
            response = check_gorzdrav(URL)
            for item in response:
                if item not in previous_data:
                    if any(doctor in item for doctor in DOCTORS):
                        send_message(item)
                        overwrite = True
            if overwrite:
                previous_data = response
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
