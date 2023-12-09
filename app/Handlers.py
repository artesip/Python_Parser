import Keyboards
from Config import TOKEN
from Request import db
from aiogram.filters import CommandStart
from aiogram import F, Router, Dispatcher, Bot, html
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Request import parce_site, deleting_all_parsed, get_all_brands_x5, get_all_brands_magnit, \
    get_magnit_items_by_filter_brand, get_x5_items_by_filter_brand, get_2store_dicts, instert_id

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

brand_dict = dict()
dict_x5 = dict_magnit = None

BRAND_X5 = 'x5'
BRAND_MAGNIT = 'magnit'


@router.message(CommandStart())
async def bot_start(message: Message):
    await instert_id(message.from_user.id)
    await message.answer('Добро пожаловать!', reply_markup=Keyboards.main_keyboard)


@router.message(F.text == Keyboards.PARSE_OFFERS)
async def site_parse(message: Message):
    await message.answer("Парсинг начался, примерное время 12 мин")
    await message.answer(await parce_site())

async def site_parse_with_announcement():
    for elem in db.get_user_id_cursor().fetchall():
        await bot.send_message(elem[1], "Парсинг начался, примерное время 12 мин")
    answ = await parce_site()
    for elem in db.get_user_id_cursor().fetchall():
        await bot.send_message(elem[1], answ)


@router.message(F.text == Keyboards.DELETE_OFFERS)
async def delete_db(message: Message):
    await message.answer(await deleting_all_parsed())


@router.message(F.text == Keyboards.MENU)
async def menu(message: Message):
    await message.answer("Меню: ", reply_markup=Keyboards.menu_keyboard)


@dp.callback_query(lambda c: c.data.startswith('x5_brand_page_'))
async def show_brand_page(callback: CallbackQuery):
    page_number = int(callback.data.split('_')[3])
    await show_brands(callback.from_user.id, page_number, BRAND_X5)


@dp.callback_query(lambda c: c.data.startswith('magnit_brand_page_'))
async def show_brand_page(callback: CallbackQuery):
    page_number = int(callback.data.split('_')[3])
    await show_brands(callback.from_user.id, page_number, BRAND_MAGNIT)


@dp.callback_query(lambda c: c.data == 'search_brand_x5')
async def menu(callback: CallbackQuery):
    await show_brands(callback.from_user.id, 0, BRAND_X5)


@dp.callback_query(lambda c: c.data == 'search_brand_magnit')
async def menu(callback: CallbackQuery):
    await show_brands(callback.from_user.id, 0, BRAND_MAGNIT)


@dp.callback_query(lambda c: c.data.startswith('fbrand_'))
async def menu(callback: CallbackQuery):
    data = {
        "name": "<N/A>",
        "new_price": "<N/A>",
        "old_price": "<N/A>",
        "weight": "<N/A>",
        "made_in": "<N/A>"
    }
    brand_str = brand_dict.get(int(callback.data.split('_')[1]))
    site = callback.data.split('_')[2]

    cursor_items = None
    if site == BRAND_X5:
        cursor_items = await get_x5_items_by_filter_brand(brand_str)
    elif site == BRAND_MAGNIT:
        cursor_items = await get_magnit_items_by_filter_brand(brand_str)

    for elem in cursor_items.fetchall():
        data['name'] = elem[1]
        data['new_price'] = elem[2]
        data['old_price'] = elem[3]
        data['weight'] = elem[7]
        data['made_in'] = elem[5]
        await bot.send_message(callback.from_user.id, "Вот что я нашёл:\n" +
                               f"Имя товара: {html.quote(data['name'])}\n"
                               f"Цена со скидкой: {html.quote(data['new_price'])}\n"
                               f"Цена без скидки: {html.quote(data['old_price'])}\n"
                               f"Вес товара: {html.quote(data['weight'])}\n"
                               f"Страна изготовления: {html.quote(data['made_in'])}"
                               )


async def show_brands(user_id, page_number: int, site_brands: str):
    brand_dict.clear()

    brands_per_page = 4
    start_index = page_number * brands_per_page
    end_index = start_index + brands_per_page
    all_brands = list()
    if site_brands == BRAND_X5:
        all_brands = await get_all_brands_x5()
    elif site_brands == BRAND_MAGNIT:
        all_brands = await get_all_brands_magnit()
    current_page_brands = all_brands[start_index:end_index]

    my_inline_keyboard = []
    for i, elem in enumerate(current_page_brands):
        brand_dict[i] = elem[2:-3]
        my_inline_keyboard.append([InlineKeyboardButton(text=elem[2:-3], callback_data=f'fbrand_{i}_{site_brands}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)

    if end_index < len(all_brands):
        next_button = [
            InlineKeyboardButton(text="Следующие", callback_data=f'{site_brands}_brand_page_{page_number + 1}')]
        keyboard.inline_keyboard.append(next_button)

    await bot.send_message(user_id, text="Бренды: ", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == 'search_brand_all')
async def find_matches_brand_item(callback: CallbackQuery):
    await show_matches_brands(callback.from_user.id, 0)


async def show_matches_brands(user_id, page_number: int):
    global dict_x5
    global dict_magnit
    dict_x5, dict_magnit = await get_2store_dicts()
    x5_keys = dict_x5.keys()

    brands_per_page = 4
    start_index = page_number * brands_per_page
    end_index = start_index + brands_per_page

    my_inline_keyboard = []
    for elem in x5_keys:
        if elem in dict_magnit:
            my_inline_keyboard.append([InlineKeyboardButton(text=elem, callback_data=f'brand_search_{elem}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)
    '''
    if start_index == end_index:
        next_button = [
            InlineKeyboardButton(text="Следующие", callback_data=f'search_brand_page_{page_number + 1}')]
        keyboard.inline_keyboard.append(next_button)
'''
    await bot.send_message(user_id, text="Бренды: ", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith('search_brand_page_'))
async def show_brand_page(callback: CallbackQuery):
    page_number = int(callback.data.split('_')[3])
    await show_brands(callback.from_user.id, page_number, BRAND_MAGNIT)


@dp.callback_query(lambda c: c.data.startswith('brand_search_'))
async def print_items_with_matches_brand(callback: CallbackQuery):
    brand  = callback.data.split('_')[2]
    data = {
        "name": "<N/A>",
        "new_price": "<N/A>",
        "old_price": "<N/A>",
        "weight": "<N/A>",
        "made_in": "<N/A>"
    }

    for elem in dict_x5.get(brand):
        data['name'] = elem.name
        data['new_price'] = elem.price_now
        data['old_price'] = elem.price_old
        data['weight'] = elem.weight
        data['made_in'] = elem.made_in
        await bot.send_message(callback.from_user.id, "Вот что я нашёл в Пятерочке:\n" +
                               f"Имя товара: {html.quote(data['name'])}\n"
                               f"Цена со скидкой: {html.quote(data['new_price'])}\n"
                               f"Цена без скидки: {html.quote(data['old_price'])}\n"
                               f"Вес товара: {html.quote(data['weight'])}\n"
                               f"Страна изготовления: {html.quote(data['made_in'])}"
                               )
    for elem in dict_magnit.get(brand):
        data['name'] = elem.name
        data['new_price'] = elem.price_now
        data['old_price'] = elem.price_old
        data['weight'] = elem.weight
        data['made_in'] = elem.made_in
        await bot.send_message(callback.from_user.id, "Вот что я нашёл в Магните:\n" +
                               f"Имя товара: {html.quote(data['name'])}\n"
                               f"Цена со скидкой: {html.quote(data['new_price'])}\n"
                               f"Цена без скидки: {html.quote(data['old_price'])}\n"
                               f"Вес товара: {html.quote(data['weight'])}\n"
                               f"Страна изготовления: {html.quote(data['made_in'])}"
                               )