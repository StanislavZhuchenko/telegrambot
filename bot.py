import asyncio
import logging
import json
from random import randint

from test import get_gp_results, dict_of_round_name

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F

from secret import token

from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher()


# with open('f1_2023.json', 'r') as f:
#     current_results = json.load(f)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/GP"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=f"Hello, {message.from_user.full_name}", reply_markup=keyboard)




@dp.message(Command("GP"))
async def all_grandprix(message: types.Message):
    builder = InlineKeyboardBuilder()
    for element in dict_of_round_name:
        builder.add(types.InlineKeyboardButton(
            text=f"{dict_of_round_name[element]}",
            callback_data=f"{element}")
        )
    builder.adjust(3)

    await message.answer(
        "Choice GP",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.in_(dict_of_round_name))
async def current_grandprix(callback: types.CallbackQuery):
    text_for_button = (
        'Race result', 'Qualifying',
        'Fastest lap', 'Practice 3',
        'Pit stop summary', 'Practice 2',
        'Starting grid', 'Practice 1'
    )

    builder = InlineKeyboardBuilder()
    for text in text_for_button:
        builder.add(types.InlineKeyboardButton(
            text=f"{text}",
            callback_data=f"{text}, {callback.data}"
        ))
    builder.adjust(2)

    await callback.message.answer(str(dict_of_round_name[callback.data]), reply_markup=builder.as_markup())


@dp.callback_query(F.data.contains('Race result'))
async def result_of_grandprix(callback: types.CallbackQuery):
    number_of_gp = int(callback.data.split(',')[1])
    await callback.message.answer(get_gp_results(number_of_gp))



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
