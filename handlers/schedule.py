from aiogram import Router, types
from aiogram.filters import Command

from schedule_parser import schedule_calendar

router = Router()


@router.message(Command('Schedule'))
async def schedule(message: types.Message):
    # await message.answer(schedule_calendar(), parse_mode='MarkdownV2')
    await message.answer(text=f"`{schedule_calendar()}`", parse_mode='MarkdownV2')
