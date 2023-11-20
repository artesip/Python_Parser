from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

MENU = 'Меню'
PARSE_OFFERS = 'Спарсить с сайта скидки'
DELETE_OFFERS = 'Удалить все'
CHOOSE_SMTH_BELOW = 'Выберите пункт ниже: '
SEARCH_BY_NAME = 'Поиск по Бренду'

main_keyboard = ReplyKeyboardMarkup(keyboard=[

    [KeyboardButton(text=MENU)],
    [KeyboardButton(text=PARSE_OFFERS)],
    [KeyboardButton(text=DELETE_OFFERS)]

], resize_keyboard=True, input_field_placeholder=CHOOSE_SMTH_BELOW)

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text=SEARCH_BY_NAME, callback_data='search_brand')],
])
