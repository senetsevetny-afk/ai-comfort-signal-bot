import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MINI_APP_URL = os.getenv("MINI_APP_URL", "").strip()
SUPPORT_URL = "https://t.me/marketaisupport"


def app_button():
    return InlineKeyboardButton(
        text="⚡ Открыть AI Comfort Signal",
        web_app=WebAppInfo(url=MINI_APP_URL),
    )


def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [app_button()],
        [
            InlineKeyboardButton(text="📖 Как работает?", callback_data="how_it_works"),
            InlineKeyboardButton(text="📊 Возможности", callback_data="features"),
        ],
        [
            InlineKeyboardButton(text="💬 Поддержка", url=SUPPORT_URL),
            InlineKeyboardButton(text="ⓘ О боте", callback_data="about_bot"),
        ],
    ])


def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [app_button()],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_start")],
    ])


START_TEXT = """
🤖 <b>AI Comfort Signal</b>

Добро пожаловать!

Здесь ты можешь анализировать рынок, изучать сигналы и отслеживать собственную статистику. 📊

🧠 AI-анализ
🎯 Рыночные сигналы
🧭 MTF-анализ
📈 Графики
🔍 Backtest
📚 История
🛡️ Контроль риска
📊 Аналитика

💡 Не обещаем лёгких денег.
Даём инструменты, данные и возможность выстроить свой подход к рынку.

🚀 <b>Начни с первого анализа.</b>
"""

HOW_TEXT = """
📖 <b>Как работает AI Comfort Signal?</b>

1️⃣ Выбираешь рынок и актив.
2️⃣ Выбираешь таймфрейм.
3️⃣ Запускаешь анализ.
4️⃣ Система проверяет доступные технические факторы.
5️⃣ Получаешь результат: 🟢 CALL / 🔴 PUT / 🔵 WAIT

⚠️ Сигнал не является гарантией результата. Рынок может двигаться иначе.
"""

FEATURES_TEXT = """
📊 <b>Возможности AI Comfort Signal</b>

🎯 Сигналы
🧭 MTF-анализ
📈 Live Chart
🔍 Backtest
📚 История
📊 Аналитика
🧠 AI Assistant
🛡️ Риск и лимиты

⚡ Всё основное находится внутри Mini App.
"""

ABOUT_TEXT = """
ⓘ <b>AI Comfort Signal</b>

Ваш интеллектуальный помощник для анализа рынка.

Приложение объединяет рыночные данные, технический анализ, сигналы, статистику и инструменты контроля риска в одном Telegram Mini App.

🚀 Меньше хаоса — больше структуры при работе с рынком.

⚠️ Приложение не гарантирует прибыль и не является финансовой рекомендацией.
"""


async def start_handler(message: Message):
    await message.answer(START_TEXT, reply_markup=start_keyboard(), parse_mode="HTML")


async def help_handler(message: Message):
    await message.answer(HOW_TEXT, reply_markup=back_keyboard(), parse_mode="HTML")


async def support_handler(message: Message):
    await message.answer(
        "💬 <b>Нужна помощь?</b>\n\nМы постараемся разобраться вместе.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Открыть чат поддержки", url=SUPPORT_URL)],
            [app_button()],
        ]),
        parse_mode="HTML",
    )


async def about_handler(message: Message):
    await message.answer(ABOUT_TEXT, reply_markup=back_keyboard(), parse_mode="HTML")


async def how_callback(callback: CallbackQuery):
    await callback.message.edit_text(HOW_TEXT, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()


async def features_callback(callback: CallbackQuery):
    await callback.message.edit_text(FEATURES_TEXT, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()


async def about_callback(callback: CallbackQuery):
    await callback.message.edit_text(ABOUT_TEXT, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()


async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(START_TEXT, reply_markup=start_keyboard(), parse_mode="HTML")
    await callback.answer()


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN.")
    if not MINI_APP_URL:
        raise RuntimeError("Не задан MINI_APP_URL.")
    if not MINI_APP_URL.startswith("https://"):
        raise RuntimeError("MINI_APP_URL должен начинаться с https://")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(help_handler, Command("help"))
    dp.message.register(support_handler, Command("support"))
    dp.message.register(about_handler, Command("about"))

    dp.callback_query.register(how_callback, F.data == "how_it_works")
    dp.callback_query.register(features_callback, F.data == "features")
    dp.callback_query.register(about_callback, F.data == "about_bot")
    dp.callback_query.register(back_callback, F.data == "back_start")

    print("🤖 AI Comfort Signal bot started")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
