from http import HTTPStatus
import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 30
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

MESSAGE = 'Ошибка при запросе к API'
NOT_HOMEWORKS = 'Нет ключа homeworks'
HOMEWORK_LIST = 'Список с домашками пуст'
HOMEWORK_STATUS = 'Ключа нет в словаре'
NOT_HOMEWORK_LIST = 'Ошибка типа данных в homework'
NOT_KEY = 'Отсутствует ключ'
STATUS = 'Отсутствует статус homeworks'
TYPE_HOMEWORK_LIST = 'Ошибка типа данных в homework_list'

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
)
logger = logging.getLogger(__name__)
logger.addHandler(
    logging.StreamHandler()
)


class TokenError(Exception):
    """Ошибка токенов."""


def send_message(bot, message):
    """Функция для отправки сообщения в чат Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(
            f'Сообщение в чат отправлено: {message}'
        )
        return True # Вот тут функция возвращает True при успешное отправке
# Я использую ее в Exception 
    except telegram.TelegramError as telegram_error:
        logger.error(
            f'Сообщение в чат не отправлено: {telegram_error}'
        )


def get_api_answer(current_timestamp):
    """Функция для запроса к эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    try:
        homework_status = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        if homework_status.status_code != HTTPStatus.OK:
            logger.error(MESSAGE)
            raise Exception(MESSAGE)
        return homework_status.json()
    except Exception as Error:
        logger.error(f'Ошибка {Error} при запросе к API')
        raise Exception(f'Ошибка {Error}')


def check_response(response):
    """Функция для проверки ответа API на корректность."""
    homework_list = response['homeworks']
    if not homework_list:
        logger.error(STATUS)
        raise LookupError(STATUS)
    if not isinstance(homework_list, list):
        logger.error(TYPE_HOMEWORK_LIST)
        raise TypeError(TYPE_HOMEWORK_LIST)
    if 'homeworks' not in response.keys():
        logger.error(NOT_KEY)
        raise KeyError(NOT_KEY)
    if not homework_list:
        logger.error(HOMEWORK_LIST)
        raise Exception(HOMEWORK_LIST)
    return homework_list[0]


def parse_status(homework):
    """Функция для проверки статуса о выполнении ДЗ."""
    if not isinstance(homework, dict):
        logger.error(NOT_HOMEWORK_LIST)
        raise KeyError(NOT_HOMEWORK_LIST)
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise Exception(f'homework_name отсутствует {homework_name}')
    if homework_status is None:
        raise Exception(f'homework_status отсутствует {homework_status}')
    if homework_status not in HOMEWORK_VERDICTES:
        logger.error(HOMEWORK_STATUS)
        raise KeyError(HOMEWORK_STATUS)
    verdict = HOMEWORK_VERDICTES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Функция для проверки доступности переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        raise TokenError('Ошибка токенов')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    last_message = ''
    previous_message = None
    while True:
        try:
            response = get_api_answer(current_timestamp)
            check = check_response(response)
            message = parse_status(check)
            if last_message != message:
                last_message = message
                send_message(bot, last_message)
                time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if message != previous_message and send_message(bot, message):
                # Функция же возвращает тру при успешной отправке, см. строку 60
                previous_message = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
