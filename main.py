from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit


# Получение токена из переменной окружения
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Token missing")
bot = Bot(bot_token)
dispatch = Dispatcher(bot)

# Соотношение стран, доменов и эмодзи
country = {
    'Нидерланды': ['nl', '\U0001F1F3' + '\U0001F1F1'],
    'Франция': ['fr', '\U0001F1EB' + '\U0001F1F7'],
    'Испания': ['es', '\U0001F1EA' + '\U0001F1F8'],
    'РФ': ['ru', '\U0001F1F7' + '\U0001F1FA'],
    'Казахстан': ['kz', '\U0001F1F0' + '\U0001F1FF'],
    'Беларусь': ['by', '\U0001F1E7' + '\U0001F1FE']
}

# Список сайтов и доступных доменов
domains = {
    'YouTube': ['nl', 'fr', 'es', 'ru', 'kz', 'by'],
    'Yandex': ['fr', 'ru', 'kz', 'by'],
    'Google': ['nl', 'fr', 'es', 'ru', 'kz', 'by'],
    'Instagram': []
}


# Создание списка инлайн URL-кнопок
def get_url_keys(subdomain):
    buttons_list = list()
    for site, domain_list in domains.items():
        if subdomain in domain_list:
            button = types.InlineKeyboardButton(text=site, url='https://{}.{}'.format(site, subdomain))
            buttons_list.append(button)
        else:
            button = types.InlineKeyboardButton(text=site, url='https://{}.com'.format(site))
            buttons_list.append(button)
    return buttons_list


# Хэндлер запуска бота
@dispatch.message_handler(commands='start')
async def handle_start(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = country.keys()
    keyboard.add(*buttons)
    await msg.answer('Откуда ты?', reply_markup=keyboard)


# Хэндлер выбора страны
@dispatch.message_handler(content_types=types.ContentType.TEXT)
async def chosen_country(msg: types.Message):
    # Проверка существования такой страны в списке доступных
    if msg.text in country:
        subdomain = country[msg.text][0]
        emoji_сode = country[msg.text][1]
        answer = 'Вы выбрали страну {flag}'.format(flag=emoji_сode)
        buttons_list = get_url_keys(subdomain)
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        keyboard.add(*buttons_list)
        await msg.answer(answer, reply_markup=keyboard)
    else:
        await msg.answer('Я не знаю такой страны :(')


if __name__ == "__main__":
    executor.start_polling(dispatch)
