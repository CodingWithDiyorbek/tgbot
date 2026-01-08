import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = "7800458629:AAHgUCk1V6gfqXGPYPeyFvoADW9YEhBmLvc"
ADMIN_ID = 7211735988 

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

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Iltimos, ism va familiyangizni kiriting:")
    await state.set_state(Murojaat.ism_familiya)

@dp.message(Murojaat.ism_familiya)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    builder = ReplyKeyboardBuilder()
    for f in filiallar:
        builder.add(types.KeyboardButton(text=f))
    builder.adjust(2)
    await message.answer(f"Rahmat, {message.text}. Endi filialni tanlang:", 
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(Murojaat.filial)

@dp.message(Murojaat.filial)
async def get_filial(message: types.Message, state: FSMContext):
    if message.text not in filiallar:
        await message.answer("Iltimos, tugmalardan birini tanlang!")
        return
    await state.update_data(tanlangan_filial=message.text)
    await message.answer("Endi muammoni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Murojaat.muammo)

@dp.message(Murojaat.muammo)
async def get_muammo(message: types.Message, state: FSMContext):
    global murojaat_soni
    murojaat_soni += 1
    
    user_data = await state.get_data()
    hisobot = (
        f"🚨 MUROJAAT #{murojaat_soni}\n\n"
        f"👤 Ism: {user_data['ism']}\n"
        f"📍 Filial: {user_data['tanlangan_filial']}\n"
        f"📝 Muammo: {message.text}"
    )
    await bot.send_message(ADMIN_ID, hisobot)
    await message.answer("Murojaatingiz yuborildi. Rahmat!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())