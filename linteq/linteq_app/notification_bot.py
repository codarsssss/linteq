from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from linteq.secret import TG_KEY, CHAT_ID


bot = Bot(token=TG_KEY)
dp = Dispatcher(bot)


async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(e)
