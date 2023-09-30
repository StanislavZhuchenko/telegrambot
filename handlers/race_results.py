import datetime

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from imagecreator import pretty_image
from new_parser import new_event_results
from parser import formatted_summary_of_year, pretty_event_results, summary_results_of_year_2

flags1 = {"throttling_key": "default"}
flags2 = {"throttling_key": "year"}

router = Router()


@router.message(Command('Results'), flags=flags1)
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


@router.callback_query(F.data == 'Current_year_results')
async def current_year_results(callback: types.CallbackQuery, year=str(datetime.date.today().year)):
    # all_done_races_of_year = summary_results_of_year(year)
    all_done_races_of_year = summary_results_of_year_2(year)
    builder = InlineKeyboardBuilder()
    # for race in all_done_races_of_year:
    for race in all_done_races_of_year[1]:
        builder.add(types.InlineKeyboardButton(
            text=race,
            callback_data=f'{race}, {year}'
        ))

    builder.adjust(2)

    # results = formatted_summary_of_year(all_done_races_of_year)
    results = formatted_summary_of_year(all_done_races_of_year[0])
    await callback.message.answer(
        f'{year} RACE RESULTS:\n'+results,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == 'Archive_results')
async def choice_a_year(callback: types.CallbackQuery):
    await callback.message.answer(f'Enter year between 1950 and {datetime.date.today().year - 1}')


@router.message(F.text.regexp(r'[1|2][9|0][\d]{2}$'), flags=flags2)
async def archive_results(message: types.Message):
    year = message.text
    # all_done_races_of_year = summary_results_of_year(year)
    all_done_races_of_year = summary_results_of_year_2(year)[0]
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


@router.callback_query(F.data.regexp(r'.+\s\d{4}$'))
async def current_gp_result(callback: types.CallbackQuery):
    """
    Answer with image of results of GP and generate callback buttons with events of the race
    :param callback:
    :return:
    """
    d = callback.data.split(', ')
    race = d[0]
    year = d[1]
    event_res = new_event_results(race, year)
    events = event_res[3]
    # if gp doesn't consist a result yet
    if type(event_res) == str:
        await callback.message.answer(text=event_res)
    # if gp have already had a result
    else:
        if 'Race result' in events:
            events.pop('Race result')  # remove 'Race results' from events that don't duplicate already posted results
        result = pretty_image(pretty_event_results(event_res))
        photo_file = BufferedInputFile(result, filename="file.txt")

        builder = InlineKeyboardBuilder()
        for event in events:
            builder.add(types.InlineKeyboardButton(
                text=f"{event}",
                callback_data=f"{race}, {year}, {event}")
            )
        builder.adjust(2)
        await callback.message.answer_photo(photo_file, reply_markup=builder.as_markup(), caption=f"Results of {race} {year}")



@router.callback_query()
async def result_of_event(callback: types.CallbackQuery):
    callback_list = callback.data.split(', ')
    race = callback_list[0]
    year = callback_list[1]
    event = callback_list[2]
    res = pretty_image(pretty_event_results(new_event_results(race, year, event)))
    text_file = BufferedInputFile(res, filename="file.txt")
    await callback.message.answer_photo(text_file, caption=f"{event} in {race} {year}")
