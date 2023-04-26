from aiogram import Bot, Dispatcher, executor, types
from Token import Token_API


bot = Bot(Token_API)
disp = Dispatcher(bot)


async def on_startup(_):
    print('Бот: вкл')


@disp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(disp, on_startup=on_startup)



























import requests
from Token import Token_API
from pprint import pprint

BASE_URL = 'https://api.telegram.org/bot'


while True:
    def get_updates():
        r = requests.get(f'{BASE_URL}{Token_API}/getUpdates')
        pprint(r.json())

    get_updates()


# {'ok': True,
#  'result': [{'message': {'chat': {'first_name': 'Артём',
#                                   'id': 1302634380,
#                                   'last_name': '(диванный эксперт)',
#                                   'type': 'private',
#                                   'username': 'X105BBX'},
#                          'date': 1681060283,
#                          'entities': [{'length': 3,
#                                        'offset': 0,
#                                        'type': 'bot_command'}],
#                          'from': {'first_name': 'Артём',
#                                   'id': 1302634380,
#                                   'is_bot': False,
#                                   'language_code': 'ru',
#                                   'last_name': '(диванный эксперт)',
#                                   'username': 'X105BBX'},
#                          'message_id': 614,
#                          'text': '/rp 10а'}
