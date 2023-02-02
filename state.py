from aiogram import types, Bot, executor, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

Api_token = "5848576908:AAEvfKWN-AgsHFNkFLltNWkRiHAPE18DijQ"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=Api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

class Data(StatesGroup):
    name = State()
    surname = State()
    phone_number = State()

@dp.message_handler(commands=['start'])
async def start(message:types.Message, state=FSMContext):
    username = message.from_user.full_name
    logging.info(message)
    await message.answer(f"🎤Salom {username}.\n\n🎉Botimizga Xush Kelibsiz")
    await message.answer("👋Ismingizni kiriting👋: ")
    await state.set_state(Data.name)

@dp.message_handler(state=Data.name)
async def name(message:types.Message, state=FSMContext):
    name_input = message.text
    await state.update_data(
        {'name': name_input}
    )

    await message.answer("👋Familyangizni kiriting👋: ")
    await Data.next()

@dp.message_handler(state=Data.surname)
async def number(message:types.Message, state=FSMContext):
    surname = message.text
    await state.update_data(
        {'surname': surname}
    )

    await message.answer("📞Tel raqamingizni kiriting:\n\n📞+998 *** ** ** ")
    await Data.next()

@dp.message_handler(state=Data.phone_number)
async def number(message:types.Message, state=FSMContext):
    phone = message.text

    await state.update_data(
        {'phone_number': phone}
    )

    data = await state.get_data(Data)
    
    name = data.get('name')
    surname = data.get('surname')
    number = data.get('phone_number')

    await message.answer(f"🧩Ismiz: {name}\n\n🏄‍♂️Familiyangiz: {surname}\n\n📞Tel raqamingiz: {number}")

    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)