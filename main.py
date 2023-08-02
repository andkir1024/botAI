from aiogram import Bot, Dispatcher, executor, types
from processorMenu import *
 
# API_TOKEN = '6232440369:AAG-bS18nYh-cXVUWrMKham3mP6OTjTaw4k'
 
bot = Bot(token=mainConst.API_TOKEN)
dp = Dispatcher(bot)
menu = processorMenu("config_ru.jsonc")
 
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await menu.doMenu(message)
   # await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
 
@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)