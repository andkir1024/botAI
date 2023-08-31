# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from okDeskUtils import okDesk
from processorMenu import *
from commonData import *
from kbs import *
 
bot = Bot(token=mainConst.API_TOKEN)
# storage=MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())

menu = processorMenu("config_ru.jsonc")

class UserState(StatesGroup):
    name = State()
    address = State()

# Начаало
@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message) -> None:
   userCurrent = userDB(True)
   userInfo, isNew = userCurrent.getUserInfo(msg)

   if userInfo.phone is None:
      kb, title, current_menu = kbs.get_kb_phone(menu, msg)
   else:
      kb, title, current_menu = kbs.get_kb(menu, msg, userInfo, isNew)
   
   if kb is not None:
      userInfo.current_menu = current_menu
      userInfo.save()
      await msg.answer(title, reply_markup=kb)

# @dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.contacts)
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(msg: types.Message, state: FSMContext):
   userCurrent = userDB(True)
   userInfo, isNew = userCurrent.getUserInfo(msg)
   userInfo.phone = msg.contact.phone_number
   userInfo.save()
   await kbs.get_kb_by_idmenu(menu, msg, 'Registry')
   # await msg.answer(f"Ваш номер: {msg.contact.phone_number}", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['test'])
async def cmd_cancel(msg: types.Message) -> None:
   userCurrent = userDB(True)
   userInfo, isNew = userCurrent.getUserInfo(msg)
   # okDesk.findUserByPhone("+79218866929")
   # okDesk.findUserByPhone("9218866929")
   okDesk.createRequest("5956", userInfo, 'Application_for_rez_Guarantee_auto')
   # await msg.answer('Canceled', reply_markup=types.ReplyKeyboardRemove())

# регистрация ассистента
@dp.message_handler(commands=['reg'])
async def user_register(msg: types.Message):
   await kbs.get_kb_by_idmenu(menu, msg, 'Registry')

# включение режима информирования
@dp.message_handler(commands=['info'])
async def user_infoMode(msg: types.Message):
   await kbs.setInfoMode(msg)

# test stasrt
'''
@dp.message_handler(commands=['reg'])
async def user_register(message: types.Message):
    await message.answer("Введите своё имя")
    await UserState.name.set()
    
@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите ваш адрес.")
    await UserState.next() # либо же UserState.address.set()
    
@dp.message_handler(state=UserState.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['username']}\n"
                         f"Адрес: {data['address']}")

    await state.finish()
'''    
# test end
        
# @dp.message_handler(state='*', commands=['setstate'])
# async def process_setstate_command(message: types.Message):
#     argument = message.get_args()
#     state = dp.current_state(user=message.from_user.id)
 
@dp.message_handler()
async def echo(msg: types.Message):
   # res = requests.post('https://httpbin.org/post', data={'st3': 'jim hopper'})
   # print(res.text)
   # okDesk.findEquipmentByInvetoryId("5956")

   # userCurrent = userDB(True)
   # userInfo, isNew = userCurrent.getUserInfo(msg)
   # await kbs.get_next_kb(menu, msg, userInfo, isNew)

   # await bot.sendp.send_p.answer(msg.text)
   await kbs.get_next_kb(menu, msg, bot)
   
   # menu.writeMsg(msg)
   # await msg.answer(msg.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)