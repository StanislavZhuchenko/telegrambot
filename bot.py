import asyncio
import logging
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F

from secret import token

from aiogram.utils.keyboard import InlineKeyboardBuilder

from parser import find_all_races_of_year, current_race_results, formatted_summary_of_year, summary_results_of_year, \
    pretty_event_results, event_results

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='/Results'),
            types.KeyboardButton(text='/Drivers'),
            types.KeyboardButton(text='/Teams'),
            types.KeyboardButton(text='/Schedule'),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=f'Hello, {message.from_user.full_name}', reply_markup=keyboard)


@dp.message(Command('Results'))
async def results(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=str(datetime.date.today().year),
        callback_data='Current_year_results'
    ))
    builder.add(types.InlineKeyboardButton(
        text=f'Archive 1950-{datetime.date.today().year - 1}',
        callback_data='Archive_results'
    ))
    builder.adjust(2)
    await message.answer('Make a choice', reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'Current_year_results')
async def current_year_results(callback: types.CallbackQuery, year=str(datetime.date.today().year)):
    all_done_races_of_year = summary_results_of_year(year)
    # year = str(datetime.date.today().year)
    builder = InlineKeyboardBuilder()
    for race in all_done_races_of_year:
        builder.add(types.InlineKeyboardButton(
            text=race,
            callback_data=f'{race}, {year}'
        ))

    builder.adjust(2)

    results = formatted_summary_of_year(all_done_races_of_year)
    await callback.message.answer(
        results,
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == 'Archive_results')
async def choice_a_year(callback: types.CallbackQuery):
    await callback.message.answer(f'Enter year between 1950 and {datetime.date.today().year - 1}')


@dp.message(F.text.regexp(r'[1|2][9|0][\d]{2}$'))
async def archive_results(message: types.Message):
    year = message.text
    all_done_races_of_year = summary_results_of_year(year)
    # year = str(datetime.date.today().year)
    builder = InlineKeyboardBuilder()
    for race in all_done_races_of_year:
        builder.add(types.InlineKeyboardButton(
            text=race,
            callback_data=f'{race}, {year}'
        ))
    builder.adjust(2)
    results = formatted_summary_of_year(all_done_races_of_year)
    await message.answer(
        results,
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.regexp(r'\D+\,\s\d{4}$'))
async def current_gp_result(callback: types.CallbackQuery):
    d = callback.data.split(', ')
    race = d[0]
    year = d[1]
    result = current_race_results(race=race, year=year)
    race_results = result[0]
    events = result[1]

    builder = InlineKeyboardBuilder()
    for event in events:
        builder.add(types.InlineKeyboardButton(
            text=f"{event}",
            callback_data=f"{race}, {year}, {event}")
        )

    builder.adjust(2)
    await callback.message.answer(race_results, reply_markup=builder.as_markup())


@dp.callback_query()
async def result_of_event(callback: types.CallbackQuery):
    callback_list = callback.data.split(', ')
    race = callback_list[0]
    year = callback_list[1]
    event = callback_list[2]
    results = pretty_event_results(event_results(race, year, event))
    await callback.message.answer(results)

#
# @dp.message(Command("GP"))
# async def all_grandprix(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     for element in dict_of_round_name:
#         builder.add(types.InlineKeyboardButton(
#             text=f"{dict_of_round_name[element]}",
#             callback_data=f"{element}")
#         )
#     builder.adjust(3)
#
#     await message.answer(
#         "Choice GP",
#         reply_markup=builder.as_markup()
#     )
#
#
# @dp.callback_query(F.data.in_(dict_of_round_name))
# async def current_grandprix(callback: types.CallbackQuery):
#     text_for_button = (
#         'Race result', 'Qualifying',
#         'Fastest lap', 'Practice 3',
#         'Pit stop summary', 'Practice 2',
#         'Starting grid', 'Practice 1'
#     )
#
#     builder = InlineKeyboardBuilder()
#     for text in text_for_button:
#         builder.add(types.InlineKeyboardButton(
#             text=f"{text}",
#             callback_data=f"{text}, {callback.data}"
#         ))
#     builder.adjust(2)
#
#     await callback.message.answer(str(dict_of_round_name[callback.data]), reply_markup=builder.as_markup())
#
#
# @dp.callback_query(F.data.contains('Race result'))
# async def result_of_grandprix(callback: types.CallbackQuery):
#     number_of_gp = int(callback.data.split(',')[1])
#     await callback.message.answer(get_gp_results(number_of_gp))
#


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
