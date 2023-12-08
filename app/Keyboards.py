from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

MENU = 'Меню'
PARSE_OFFERS = 'Спарсить с сайта скидки'
DELETE_OFFERS = 'Удалить все'
CHOOSE_SMTH_BELOW = 'Выберите пункт ниже: '
SEARCH_BY_BRAND_X5 = 'Поиск по Бренду в Пятерочке'
SEARCH_BY_BRAND_MAGNIT = 'Поиск по Бренду в Пятерочке'

main_keyboard = ReplyKeyboardMarkup(keyboard=[

    [KeyboardButton(text=MENU)],
    [KeyboardButton(text=PARSE_OFFERS)],
    [KeyboardButton(text=DELETE_OFFERS)]

], resize_keyboard=True, input_field_placeholder=CHOOSE_SMTH_BELOW)

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text=SEARCH_BY_BRAND_X5, callback_data='search_brand_x5')],
    [InlineKeyboardButton(text=SEARCH_BY_BRAND_MAGNIT, callback_data='search_brand_magnit')]
])
