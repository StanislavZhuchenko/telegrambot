import asyncio
import logging
import datetime
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.types import BufferedInputFile

from schedule_parser import schedule_calendar
from secret import token

from aiogram.utils.keyboard import InlineKeyboardBuilder

from parser import find_all_races_of_year, current_race_results, formatted_summary_of_year, summary_results_of_year, \
    pretty_event_results, event_results

from driver_standing import driverstandings
from imagecreator import pretty_image

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command('start'))
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
        f'{year} RACE RESULTS:\n'+results,
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == 'Archive_results')
async def choice_a_year(callback: types.CallbackQuery):
    await callback.message.answer(f'Enter year between 1950 and {datetime.date.today().year - 1}')


@dp.message(F.text.regexp(r'[1|2][9|0][\d]{2}$'))
async def archive_results(message: types.Message):
    year = message.text
    all_done_races_of_year = summary_results_of_year(year)
    builder = InlineKeyboardBuilder()
    for race in all_done_races_of_year:
        builder.add(types.InlineKeyboardButton(
            text=race,
            callback_data=f'{race}, {year}'
        ))
    builder.adjust(2)
    results = formatted_summary_of_year(all_done_races_of_year)
    await message.answer(
        f'{year} RACE RESULTS:\n'+results,
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
    if len(results) > 4096:
        await callback.message.answer(results[:4096])
        await callback.message.answer(results[4096:])
    await callback.message.answer(results)


@dp.message(Command('Schedule'))
async def schedule(message: types.Message):
    await message.answer(schedule_calendar())


@dp.message(Command('Drivers'))
async def drivers(message: types.Message):
    pretty_image(pretty_event_results(driverstandings(2023)))
    # time.sleep(5)
    with open('test.png', 'rb') as f:
        await message.answer_photo(
            BufferedInputFile(f.read(), filename='filename.png')
        )


from aiogram.types import URLInputFile

@dp.message(Command('images'))
async def upload_photo(message: types.Message):
 # Отправка файла по ссылке
    image_from_url = URLInputFile("https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/aston-martin.png.transform/3col-retina/image.png 2x", bot=bot)
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
