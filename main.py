import requests
import telegram
from random import randint
from time import sleep
from environs import Env


def get_comics(num: int) -> dict:
    url = f'https://xkcd.com/{num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_max_comic_num() -> int:
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def main():
    env = Env()
    env.read_env()
    token_tg = env.str('TG_TOKEN', None)
    chat_id = env.str('TG_CHAT_ID', None)

    if not token_tg or not chat_id:
        raise ValueError("Не указаны TG_TOKEN или TG_CHAT_ID.")

    bot = telegram.Bot(token_tg)

    try:
        max_num = get_max_comic_num()
        num = randint(1, max_num)
        comics = get_comics(num)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении комикса: {e}")
        return

    try:
        comment = comics['alt']
        photo_url = comics['img']
    except KeyError as e:
        print(f"Отсутствует ключ {e} в данных комикса.")
        return

    if not photo_url.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Пропущен комикс {num}: неподдерживаемый формат изображения.")

    try:
        bot.send_photo(chat_id=chat_id, photo=photo_url, caption=comment)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return


if __name__ == '__main__':
    main()
