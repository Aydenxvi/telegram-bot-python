import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F, types, Router 
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- CONFIGURATION ---
# Не забудьте обновить токен через /revoke в @BotFather, если еще не сделали этого!
BOT_TOKEN = "8463302670:AAECjdlF3bgfTkwqigzavnWyRVDAGB4Uwp8"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

router = Router()

# --- КЛАВИАТУРЫ (ГЛАВНОЕ МЕНЮ) ---
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🛍 Каталог")
    builder.button(text="📍 Информация и Местоположение")
    builder.button(text="📞 Контакты владельца")
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True)

# --- КЛАВИАТУРЫ (ИНЛАЙН ДЛЯ КАТАЛОГА) ---
def get_catalog_keyboard():
    builder = InlineKeyboardBuilder()
    # callback_data — это то, что бот тайно получит при нажатии на кнопку
    builder.button(text="👗 Женская одежда", callback_data="cat_women")
    builder.button(text="👔 Мужская одежда", callback_data="cat_men")
    builder.button(text="👜 Сумки и рюкзаки", callback_data="cat_bags")
    builder.button(text="💍 Аксессуары", callback_data="cat_acc")
    builder.adjust(2) # по 2 кнопки в ряд
    return builder.as_markup()

def get_back_to_catalog_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад в каталог", callback_data="back_to_catalog")
    return builder.as_markup()


# --- ОБРАБОТЧИКИ (HANDLERS) ---

@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    user_name = message.from_user.first_name
    welcome_text = (
        f"Bonjour, {html.bold(user_name)}! ✨\n\n"
        "Добро пожаловать! Вас встречает бот-ответчик магазина одежды «Лавка Стиля».\n"
        "У нас качественная одежда по доступной цене. Выберите, что вас интересует:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@router.message(F.text == "📍 Информация и Местоположение")
async def info_handler(message: types.Message):
    info_text = (
        f"{html.bold('📍 НАШ МАГАЗИН')}\n"
        "Seyit Avsar sokak, Bolu, Merkez\n\n"
        f"{html.bold('⏰ ГРАФИК РАБОТЫ')}\n"
        "Пн - Пт: 10:00 - 20:00 \n"
        "Сб - Вс: 11:00 - 18:00 \n\n"
        "Мы следим за вашим стилем! 🥂"
    )
    await message.answer(info_text, parse_mode="HTML")


@router.message(F.text == "📞 Контакты владельца")
async def contact_handler(message: types.Message):
    contact_text = (
        f"{html.bold('📞 СВЯЗЬ С НАМИ')}\n\n"
        "Наш персонал всегда готов ответить на ваши вопросы и помочь с выбором:\n\n"
        "👤 Владелец: @norowareshi\n"
        "📱 Телефон: +90 531 328 2530\n"
        "📧 Email: turgunbaevdooolot@gmail.com"
    )
    await message.answer(contact_text, parse_mode="HTML")


# 1. Нажатие на кнопку "🛍 Каталог" в главном меню
@router.message(F.text == "🛍 Каталог")
async def catalog_handler(message: types.Message):
    await message.answer(
        f"⬇️ {html.bold('Каталог товаров магазина «Лавка Стиля»')}\n"
        "Выберите интересующий вас раздел ниже:",
        reply_markup=get_catalog_keyboard(),
        parse_mode="HTML"
    )


# --- ОБРАБОТКА НАЖАТИЙ НА ИНЛАЙН-КНОПКИ (CALLBACK QUERIES) ---

# Если выбрали Женскую одежду
@router.callback_query(F.data == "cat_women")
async def process_women_catalog(callback: types.CallbackQuery):
    text = (
        f"{html.bold('👗 ЖЕНСКАЯ ОДЕЖДА')}\n\n"
        "• Летние платья и сарафаны — от 1500 руб.\n"
        "• Стильные классические костюмы — от 3500 руб.\n"
        "• Блузы и оверсайз рубашки — от 1200 руб.\n"
        "• Джинсы и юбки — от 1800 руб.\n\n"
        "Для заказа или примерки напишите владельцу: @norowareshi"
    )
    # edit_message_text красиво меняет текст старого сообщения, а не спамит новым
    await callback.message.edit_text(text, reply_markup=get_back_to_catalog_keyboard(), parse_mode="HTML")
    await callback.answer() # Закрывает анимацию часиков на кнопке

# Если выбрали Мужскую одежду
@router.callback_query(F.data == "cat_men")
async def process_men_catalog(callback: types.CallbackQuery):
    text = (
        f"{html.bold('👔 МУЖСКАЯ ОДЕЖДА')}\n\n"
        "• Рубашки (casual и классика) — от 1400 руб.\n"
        "• Футболки и поло премиум качества — от 900 руб.\n"
        "• Брюки, чиносы и джинсы — от 2200 руб.\n"
        "• Пиджаки и легкие куртки — от 4000 руб.\n\n"
        "По вопросам размеров пишите сюда: @norowareshi"
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_catalog_keyboard(), parse_mode="HTML")
    await callback.answer()

# Если выбрали Сумки
@router.callback_query(F.data == "cat_bags")
async def process_bags_catalog(callback: types.CallbackQuery):
    text = (
        f"{html.bold('👜 СУМКИ И РЮКЗАКИ')}\n\n"
        "• Кожаные женские сумки — от 2500 руб.\n"
        "• Городские рюкзаки — от 1900 руб.\n"
        "• Клатчи и вечерние сумочки — от 1300 руб.\n"
        "• Мужские портфели и барсетки — от 2800 ...\n\n"
        "Связь с нами: @norowareshi"
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_catalog_keyboard(), parse_mode="HTML")
    await callback.answer()

# Если выбрали Аксессуары
@router.callback_query(F.data == "cat_acc")
async def process_acc_catalog(callback: types.CallbackQuery):
    text = (
        f"{html.bold('💍 АКСЕССУАРЫ')}\n\n"
        "• Солнцезащитные очки — от 800 руб.\n"
        "• Кожаные ремни — от 1000 руб.\n"
        "• Наручные часы — от 3000 руб.\n"
        "• Качественная бижутерия — от 400 руб.\n\n"
        "Связь с нами: @norowareshi"
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_catalog_keyboard(), parse_mode="HTML")
    await callback.answer()

# Нажатие на кнопку "Назад в каталог"
@router.callback_query(F.data == "back_to_catalog")
async def process_back_to_catalog(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"⬇️ {html.bold('Каталог товаров магазина «Лавка Стиля»')}\n"
        "Выберите интересующий вас раздел ниже:",
        reply_markup=get_catalog_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(
        "Спасибо за ваше сообщение! 📩\n\n"
        "Менеджер изучит ваш запрос и ответит вам лично в ближайшее время."
    )

# --- MAIN BOILERPLATE ---
async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        sys.exit(0)
