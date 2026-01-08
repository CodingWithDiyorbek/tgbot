import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN", "7800458629:AAHgUCk1V6gfqXGPYPeyFvoADW9YEhBmLvc")
ADMIN_ID = 6140962854

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

murojaat_soni = 0

class Murojaat(StatesGroup):
    ism_familiya = State()
    filial = State()
    muammo = State()

filiallar = [
    "Olmazor", "Chinoz", "Yangiyol", "Niyozbosh", 
    "Toshkent", "Samarqand", "Qozogiston", "Navoiy", 
    "Jizzax", "Termiz", "Qashqadaryo", "Surxondaryo"
]

@dp.message(Command("clear"))
async def clear_counter(message: types.Message):
    global murojaat_soni
    if message.from_user.id == ADMIN_ID:
        murojaat_soni = 0
        await message.answer("Hisoblagich nolga tushirildi.")

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Alaziz_ariza botiga xush kelibsiz.\nIsm va familiyangizni kiriting:")
    await state.set_state(Murojaat.ism_familiya)

@dp.message(Murojaat.ism_familiya)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    builder = ReplyKeyboardBuilder()
    for f in filiallar:
        builder.add(types.KeyboardButton(text=f))
    builder.adjust(2)
    await message.answer(f"Rahmat, {message.text}. Filialni tanlang:", 
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(Murojaat.filial)

@dp.message(Murojaat.filial)
async def get_filial(message: types.Message, state: FSMContext):
    if message.text not in filiallar:
        await message.answer("Tugmalardan birini tanlang!")
        return
    await state.update_data(tanlangan_filial=message.text)
    await message.answer("Muammoni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Murojaat.muammo)

@dp.message(Murojaat.muammo)
async def get_muammo(message: types.Message, state: FSMContext):
    global murojaat_soni
    murojaat_soni += 1
    user_data = await state.get_data()
    hisobot = (
        f"🚨 MUROJAAT #{murojaat_soni}\n\
