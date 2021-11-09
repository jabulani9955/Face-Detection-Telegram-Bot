import os
import time
import logging
import cv2

from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from preprocessing import resize_image
from postprocessing import restore_image
from model import get_predict

# Статический текст
START = """
    Привет, %s! \nЗагрузи фото и узнай, есть ли там кто-нибудь среди нас?
    LIST of commands:
        /start - restart
        /about - about
"""
ABOUT = "CCC - Свой Среди Своих"
STICKER = 'CAACAgIAAxkBAAEDH3ZhcPwuk8_ea46pVXd7kcKtuJaJCgACeSUAAp7OCwABlPU3foy-CJwhBA'


# Включаем логирование
logging.basicConfig(
    filename='log.log', 
    level=logging.INFO
)

# Загрузка токена через env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f'{user_id} запустил бота в {time.asctime()}')
    await message.reply(START % user_name)


@dp.message_handler(commands=['about'])
async def process_help_command(message: types.Message):
    await message.reply(ABOUT)


# Главная функция
@dp.message_handler(content_types=['photo'])
async def handle_photo_for_prediction(message):
    chat_id = message.chat.id

    # media_group_id is None means single photo at message
    if message.media_group_id is None:
        user_id = message.from_user.id
        message_id = message.message_id

        # Define input photo local path
        photo_name = './input/face_%s_%s.jpg' % (user_id, message_id)
        await message.photo[-1].download(photo_name) # extract photo for further procceses

        # Output photo local path
        resized_photo_name = './output/photo_%s_%s.jpg' % (user_id, message_id)

        # Отправка стикера во время предсказания
        await bot.send_sticker(user_id, STICKER)

        # YOLO predictions
        w, h = resize_image(photo_name, resized_photo_name)
        result, result_photo = get_predict(resized_photo_name)
        restore_image(result_photo, result_photo, w, h)
        await bot.send_photo(chat_id, photo=open(result_photo, 'rb'), caption=result)
    else:
        await message.reply("Пожалуйста, пришли одну фотографию, а не вот столько!")



if __name__ == '__main__':
    executor.start_polling(dp)
