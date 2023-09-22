import datetime
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from driver_standing import driverstandings
from imagecreator import pretty_image
from parser import pretty_event_results

router = Router()


@router.message(Command('Drivers'))
async def drivers_stands(message: types.Message):
    year = datetime.date.today().year
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=str(year),
        callback_data=f'Driver_standings, {year}'
    ))
    builder.add(types.InlineKeyboardButton(
        text=f'Archive 1950-{datetime.date.today().year - 1}',
        callback_data=f'Achieve_Driver_standings'
    ))
    builder.adjust(2)
    await message.answer('Make a choice', reply_markup=builder.as_markup())


@router.callback_query(F.data == "Achieve_Driver_standings")
async def archive_driver_standings(callback: types.CallbackQuery):
    await callback.message.answer(f'Driver standings \nEnter year between 1950 and {datetime.date.today().year - 1}\n'
                                  f'in format "drivers YEAR"')


@router.message(F.text.regexp(r'drivers [1|2][9|0][\d]{2}$'))
async def driver(message: types.Message):
    year = message.text.split(' ')[1]
    print(year)
    results = pretty_image(pretty_event_results(driverstandings(year=int(year))))
    text_file = BufferedInputFile(results, filename="results")
    await message.answer_photo(text_file)


@router.callback_query(F.data.regexp(r"Driver_standings, \d{4}$"))
async def drivers(callback: types.CallbackQuery):
    year = callback.data.split(', ')[1]
    results = pretty_image(pretty_event_results(driverstandings(year)))
    text_file = BufferedInputFile(results, filename="results")
    await callback.message.answer_photo(text_file)
