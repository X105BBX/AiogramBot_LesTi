from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
from aiogram import Bot, Dispatcher, executor, types
from Openpyxl_func import *
from Token import Token_API
from datetime import date
import calendar
import time

bot = Bot(Token_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот: вкл')


@dp.message_handler(commands='start')
async def is_start(message: Message):
    await bot.send_message(message.chat.id,
                           text=f'Привет, {message.from_user.first_name} {message.from_user.last_name}! '
                                f'Добро пожаловать в бота LesTi 📋')
    await message.delete()


@dp.message_handler(content_types='document')
async def xl(message: Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'{message.document.file_name}')
    await message.answer_document(message.document.file_id)


@dp.message_handler(commands='thr-')
async def tcr_remove(message: Message):
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    if day == 'Monday':
        the_right_day = 'Вторник'
    elif day == 'Tuesday':
        the_right_day = 'Среда'
    elif day == 'Wednesday':
        the_right_day = 'Четверг'
    elif day == 'Thursday':
        the_right_day = 'Пятница'
    else:
        the_right_day = 'Понедельник'
    full_name = message.get_args()
    action = WithoutTeacher(full_name, the_right_day)
    if action is True:
        await bot.send_message(message.chat.id, text='Расписание успешно изменено')
    else:
        await bot.send_message(message.chat.id, text='Произошла ошибка, возможно вы неправильно написали ')
    await message.delete()


@dp.message_handler(commands='tt')
async def tt(message: types.Message):
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    if day == 'Monday':
        the_right_day = 'Вторник'
    elif day == 'Tuesday':
        the_right_day = 'Среда'
    elif day == 'Wednesday':
        the_right_day = 'Четверг'
    elif day == 'Thursday':
        the_right_day = 'Пятница'
    else:
        the_right_day = 'Понедельник'
    the_right_class = message.get_args()
    output = LesPlan(the_right_class, the_right_day)
    await bot.send_message(message.chat.id, text=output)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
