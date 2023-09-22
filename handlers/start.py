from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='/Results'),
            types.KeyboardButton(text='/Drivers'),
            types.KeyboardButton(text='/Constructor'),
            types.KeyboardButton(text='/Schedule'),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=f'Hello, {message.from_user.full_name}', reply_markup=keyboard)
