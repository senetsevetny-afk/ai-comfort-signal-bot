import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MINI_APP_URL = os.getenv("MINI_APP_URL", "").strip()
PORT = int(os.getenv("PORT", "10000"))

SUPPORT_URL = "https://t.me/marketaisupport"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
if not MINI_APP_URL:
    raise RuntimeError("MINI_APP_URL is not set")
if not MINI_APP_URL.startswith("https://"):
    raise RuntimeError("MINI_APP_URL must start with https://")

dp = Dispatcher()


# ---------- Keyboards ----------

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⚡ ОТКРЫТЬ AI COMFORT SIGNAL",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )],
        [
            InlineKeyboardButton(text="📖 Как это работает?", callback_data="how_works"),
            InlineKeyboardButton(text="📊 Возможности", callback_data="features"),
        ],
        [
            InlineKeyboardButton(text="💬 Поддержка", url=SUPPORT_URL),
            InlineKeyboardButton(text="ⓘ О боте", callback_data="about"),
        ],
    ])


def intro_keyboard(page: int) -> InlineKeyboardMarkup:
    rows = []

    if page < 3:
        rows.append([
            InlineKeyboardButton(text="Далее →", callback_data=f"intro_next_{page + 1}")
        ])
    else:
        rows.append([
            InlineKeyboardButton(
                text="⚡ ОТКРЫТЬ AI COMFORT SIGNAL",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ])

    if page > 1:
        rows.append([
            InlineKeyboardButton(text="← Назад", callback_data=f"intro_prev_{page - 1}")
        ])

    if page == 3:
        rows.append([
            InlineKeyboardButton(text="📊 Все возможности", callback_data="features"),
            InlineKeyboardButton(text="ⓘ О боте", callback_data="about"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def section_keyboard(back_callback="back_main") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Открыть приложение",
                              web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="← Назад", callback_data=back_callback)],
    ])


# ---------- Text screens ----------

INTRO = {
    1: """👋 <b>Добро пожаловать!</b>

⚡ <b>AI Comfort Signal</b>

Интеллектуальный помощник
для анализа рынка.

Здесь ты можешь:
📊 анализировать активы
🎯 получать CALL / PUT / WAIT
🔎 изучать факторы сигнала
📈 смотреть MTF и аналитику
🤖 использовать AI-инструменты""",

    2: """🧠 <b>Что умеет AI Comfort Signal?</b>

⚡ <b>SIGNAL</b>
Структурированный анализ с направлением
CALL / PUT / WAIT.

📊 <b>MARKET</b>
Crypto, Forex и OTC.

🔎 <b>MTF</b>
Сравнение нескольких таймфреймов
для более полного контекста.

📈 <b>ANALYTICS</b>
История, статистика и результаты
предыдущих сигналов.""",

    3: """🚀 <b>Как это работает?</b>

1️⃣ Выбираешь актив
2️⃣ Выбираешь таймфрейм
3️⃣ Запускаешь анализ
4️⃣ Получаешь CALL / PUT / WAIT
5️⃣ Изучаешь факторы и статистику

🤖 Внутри также доступны AI-инструменты,
технический анализ и дополнительные
рыночные данные.

✨ <b>Всё собрано в одном Mini App.</b>""",
}

HOW_WORKS = """📖 <b>Как это работает?</b>

<b>1. Выбор рынка</b>
Выбираешь Crypto, Forex или OTC.

<b>2. Выбор актива</b>
Выбираешь интересующий инструмент.

<b>3. Таймфрейм</b>
Определяешь период анализа.

<b>4. Сигнал</b>
Получаешь CALL / PUT / WAIT и
разбор основных факторов.

<b>5. Дополнительный анализ</b>
Можно изучить MTF, историю,
статистику и другие доступные данные.

⚠️ Сигнал является аналитическим
инструментом и не гарантирует результат."""

FEATURES = """📊 <b>Возможности AI Comfort Signal</b>

⚡ <b>Signals</b>
CALL / PUT / WAIT

📈 <b>Technical Analysis</b>
Тренд, импульс и технические факторы.

🔎 <b>MTF</b>
Сравнение нескольких таймфреймов.

📊 <b>Analytics</b>
История и статистика сигналов.

📡 <b>Market</b>
Crypto, Forex и OTC.

🤖 <b>AI Assistant</b>
Дополнительный AI-анализ.

🛡️ <b>Risk & Session</b>
Инструменты контроля сессии и риска."""

ABOUT = """ⓘ <b>AI Comfort Signal</b>

Telegram Mini App для анализа рыночных
данных и формирования структурированных
аналитических сигналов.

Приложение объединяет рыночный анализ,
технические факторы, MTF, историю,
аналитику и AI-инструменты.

⚠️ AI Comfort Signal не является
инвестиционной рекомендацией и не
гарантирует финансовый результат."""


# ---------- Handlers ----------

async def send_intro(message: Message, page: int = 1):
    await message.answer(
        INTRO[page],
        reply_markup=intro_keyboard(page),
        parse_mode="HTML",
    )


@dp.message(Command("start"))
async def start_handler(message: Message):
    # One message at a time: Telegram chat stays clean.
    await send_intro(message, 1)


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        HOW_WORKS,
        reply_markup=section_keyboard(),
        parse_mode="HTML",
    )


@dp.message(Command("support"))
async def support_handler(message: Message):
    await message.answer(
        "💬 <b>Поддержка</b>\n\n"
        "Если у тебя есть вопрос или проблема,\n"
        "напиши в поддержку.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Написать в поддержку", url=SUPPORT_URL)],
            [InlineKeyboardButton(text="← Назад", callback_data="back_main")],
        ]),
        parse_mode="HTML",
    )


@dp.message(Command("about"))
async def about_handler(message: Message):
    await message.answer(ABOUT, reply_markup=section_keyboard(), parse_mode="HTML")


@dp.callback_query(F.data.startswith("intro_next_"))
async def intro_next(callback: CallbackQuery):
    page = int(callback.data.rsplit("_", 1)[1])
    await callback.message.edit_text(
        INTRO[page],
        reply_markup=intro_keyboard(page),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("intro_prev_"))
async def intro_prev(callback: CallbackQuery):
    page = int(callback.data.rsplit("_", 1)[1])
    await callback.message.edit_text(
        INTRO[page],
        reply_markup=intro_keyboard(page),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "how_works")
async def how_works(callback: CallbackQuery):
    await callback.message.edit_text(
        HOW_WORKS,
        reply_markup=section_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "features")
async def features(callback: CallbackQuery):
    await callback.message.edit_text(
        FEATURES,
        reply_markup=section_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.edit_text(
        ABOUT,
        reply_markup=section_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        INTRO[3],
        reply_markup=intro_keyboard(3),
        parse_mode="HTML",
    )
    await callback.answer()


# ---------- Render health server ----------

async def health(request: web.Request):
    return web.Response(text="AI Comfort Signal bot is running")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"🌐 Health server started on port {PORT}", flush=True)


async def main():
    bot = Bot(token=BOT_TOKEN)

    await start_web_server()
    print("🤖 AI Comfort Signal bot started", flush=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
