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
from kbs import *
 
bot = Bot(token=mainConst.API_TOKEN)
# storage=MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())

menu = processorMenu("config_ru.jsonc")

class UserState(StatesGroup):
    name = State()
    address = State()
     
@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message) -> None:
   kb, title = kbs.get_kb(menu, msg)
   
   if kb is not None:
      await msg.answer(title, reply_markup=kb)

@dp.message_handler(commands=['test'])
async def cmd_cancel(msg: types.Message) -> None:
     await msg.answer('Canceled', reply_markup=types.ReplyKeyboardRemove())

# test stasrt
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
# test end
        
@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
 
@dp.message_handler()
async def echo(message: types.Message):
   # res = requests.post('https://httpbin.org/post', data={'st3': 'jim hopper'})
   # print(res.text)
   # okDesk.findEquipmentByInvetoryId("5956")
   menu.writeMsg(message)

   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)