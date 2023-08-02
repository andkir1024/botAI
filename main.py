from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from processorMenu import *
from kbs import *

 
bot = Bot(token=mainConst.API_TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage)
dp.middleware.setup(LoggingMiddleware())
menu = processorMenu("config_ru.jsonc")
 
@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message) -> None:
   await msg.answer('Text', reply_markup=kb.get_kb(menu, msg))


@dp.message_handler(commands=['test'])
async def cmd_cancel(msg: types.Message) -> None:
    await msg.answer('Canceled', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    pass
   #  if not argument:
   #      await state.reset_state()
   #      return await message.reply(MESSAGES['state_reset'])

   #  if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
   #      return await message.reply(MESSAGES['invalid_key'].format(key=argument))

   #  await state.set_state(TestStates.all()[int(argument)])
   #  await message.reply(MESSAGES['state_change'], reply=False)
         
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#    await menu.doMenu(message)
   # await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
 
@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)