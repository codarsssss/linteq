from aiogram import Bot
from aiogram.dispatcher import Dispatcher


TG_KEY = '6099136830:AAGxdrlY2MlJkxcmnsf91DIIY2MOM6rO4mM'
CHAT_ID = '-676751431'


bot = Bot(token=TG_KEY)
dp = Dispatcher(bot)


async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        await print(e)
