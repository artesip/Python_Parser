import Keyboards
from Config import Token
from aiogram.filters import CommandStart
from aiogram import F, Router, Dispatcher, Bot, html
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Request import parce_site, deleting_all_parsed, get_all_brands, get_items_by_filter_brand

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(Token)

brand_dict = dict()


@router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer('Добро пожаловать!', reply_markup=Keyboards.main_keyboard)


@router.message(F.text == Keyboards.PARSE_OFFERS)
async def site_parse(message: Message):
    await message.answer("Парсинг начался, примерное время 7 мин")
    await message.answer(await parce_site())


@router.message(F.text == Keyboards.DELETE_OFFERS)
async def delete_db(message: Message):
    await message.answer(await deleting_all_parsed())


@router.message(F.text == Keyboards.MENU)
async def menu(message: Message):
    await message.answer("Меню: ", reply_markup=Keyboards.menu_keyboard)


@dp.callback_query(lambda c: c.data.startswith('brand_page_'))
async def show_brand_page(callback: CallbackQuery):
    page_number = int(callback.data.split('_')[2])
    await show_brands(callback.from_user.id, page_number)


@dp.callback_query(lambda c: c.data == 'search_brand')
async def menu(callback: CallbackQuery):
    await show_brands(callback.from_user.id, page_number=0)


@dp.callback_query(lambda c: c.data.startswith('fbrand_'))
async def menu(callback: CallbackQuery):
    data = {
        "name": "<N/A>",
        "new_price": "<N/A>",
        "old_price": "<N/A>"
    }
    brand_str = brand_dict.get(int(callback.data.split('_')[1]))
    cursor_items = await get_items_by_filter_brand(brand_str)
    for elem in cursor_items.fetchall():
        data['name'] = elem[1]
        data['new_price'] = elem[2]
        data['old_price'] = elem[3]
        await bot.send_message(callback.from_user.id, "Вот что я нашёл:\n" +
                               f"Имя товара: {html.quote(data['name'])}\n"
                               f"Цена со скидкой: {html.quote(data['new_price'])}\n"
                               f"Цена без скидки: {html.quote(data['old_price'])}")


async def show_brands(user_id, page_number):
    brand_dict.clear()

    brands_per_page = 4
    start_index = page_number * brands_per_page
    end_index = start_index + brands_per_page

    all_brands = await get_all_brands()
    current_page_brands = all_brands[start_index:end_index]

    my_inline_keyboard = []
    for i, elem in enumerate(current_page_brands):
        brand_dict[i] = elem[2:-3]
        my_inline_keyboard.append([InlineKeyboardButton(text=elem[2:-3], callback_data=f'fbrand_{i}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)

    if end_index < len(all_brands):
        next_button = [InlineKeyboardButton(text="Next", callback_data=f'brand_page_{page_number + 1}')]
        keyboard.inline_keyboard.append(next_button)

    await bot.send_message(user_id, text="Бренды: ", reply_markup=keyboard)
