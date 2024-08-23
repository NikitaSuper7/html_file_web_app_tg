from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import asyncio
import logging
import sys
from PIL import Image
from aiogram.types.web_app_info import WebAppInfo
dp = Dispatcher()
@dp.message(Command('start'))
async def start(message: types.Message):  # async так как все функции в Aiogramm асинхронны
    # await bot.send_message(message.chat.id, "Hello") 1-ый способ отправки сообщений
    # await чтобы действие выполнялось асинхронно
    btn1 = types.KeyboardButton(text="открыть веб страницу", web_app=WebAppInfo(url="https://sky.pro/"))
    markup = types.ReplyKeyboardMarkup(keyboard=[[btn1]])
    await message.answer("Привет друг", reply_markup=markup)

    # await message.answer("Hello Nikita") # просто сообщение
    # await message.reply("Hello") # Ответ на сообщение


# чтобы бот не останавливался
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token='7232330201:AAHZTFneecWM8P77WDuZu2InRB-bNX72j-0')

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
