import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

BOT_TOKEN=os.getenv('BOT_TOKEN','').strip()
MINI_APP_URL=os.getenv('MINI_APP_URL','').strip()
PORT=int(os.getenv('PORT','10000'))
SUPPORT_URL='https://t.me/marketaisupport'
if not BOT_TOKEN: raise RuntimeError('BOT_TOKEN is not set')
if not MINI_APP_URL: raise RuntimeError('MINI_APP_URL is not set')
if not MINI_APP_URL.startswith('https://'): raise RuntimeError('MINI_APP_URL must start with https://')
dp=Dispatcher()

def kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⚡ Открыть AI Comfort Signal',web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text='📖 Как работает?',callback_data='how'),InlineKeyboardButton(text='📊 Возможности',callback_data='features')],
        [InlineKeyboardButton(text='💬 Поддержка',url=SUPPORT_URL),InlineKeyboardButton(text='ⓘ О боте',callback_data='about')]])

def back(): return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️ Назад',callback_data='back')]])
START='''🚀 <b>AI Comfort Signal</b>\n\nТвой персональный центр анализа рынка.\n\nПолучай структурированный сигнал <b>CALL / PUT / WAIT</b> и открывай Mini App прямо из Telegram.\n\n⚡ Нажми кнопку ниже, чтобы начать.'''
@dp.message(Command('start'))
async def start(m:Message): await m.answer(START,reply_markup=kb(),parse_mode='HTML')
@dp.message(Command('help'))
async def help_(m:Message): await m.answer('📖 <b>Помощь</b>\n\nОткрой приложение кнопкой ниже.\n\nЕсли есть проблема — используй «💬 Поддержка».',reply_markup=kb(),parse_mode='HTML')
@dp.message(Command('support'))
async def support(m:Message): await m.answer('💬 <b>Поддержка</b>\n\nНапиши в поддержку:',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='💬 Написать в поддержку',url=SUPPORT_URL)],[InlineKeyboardButton(text='⬅️ В меню',callback_data='back')]]),parse_mode='HTML')
@dp.message(Command('about'))
async def about_cmd(m:Message): await m.answer('ⓘ <b>AI Comfort Signal</b>\n\nTelegram Mini App для анализа рынка.\n\nНе является финансовой гарантией или инвестиционной рекомендацией.',reply_markup=back(),parse_mode='HTML')
@dp.callback_query(F.data=='how')
async def how(c:CallbackQuery): await c.message.edit_text('📖 <b>Как работает</b>\n\n1️⃣ Выбираешь актив и таймфрейм.\n2️⃣ Приложение анализирует доступные данные.\n3️⃣ Формируется CALL / PUT / WAIT.\n4️⃣ Можно посмотреть факторы и аналитику.\n\n⚠️ Это аналитическая оценка, а не гарантия результата.',reply_markup=back(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='features')
async def features(c:CallbackQuery): await c.message.edit_text('📊 <b>Возможности</b>\n\n• ⚡ CALL / PUT / WAIT\n• 📈 Технический анализ\n• 🔎 Мульти-таймфрейм анализ\n• 📊 История и статистика\n• 🤖 AI-инструменты\n• 📱 Telegram Mini App',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⚡ Открыть приложение',web_app=WebAppInfo(url=MINI_APP_URL))],[InlineKeyboardButton(text='⬅️ Назад',callback_data='back')]]),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='about')
async def about(c:CallbackQuery): await c.message.edit_text('ⓘ <b>О боте</b>\n\n<b>AI Comfort Signal</b> — интерфейс для анализа рыночных данных и формирования аналитических сигналов.\n\nНе является финансовой гарантией или инвестиционной рекомендацией.',reply_markup=back(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='back')
async def back_(c:CallbackQuery): await c.message.edit_text(START,reply_markup=kb(),parse_mode='HTML'); await c.answer()
async def health(request): return web.Response(text='AI Comfort Signal bot is running')
async def web_server():
    app=web.Application(); app.router.add_get('/',health); app.router.add_get('/health',health)
    runner=web.AppRunner(app); await runner.setup(); await web.TCPSite(runner,'0.0.0.0',PORT).start()
    print(f'🌐 Health server started on port {PORT}',flush=True)
async def main():
    bot=Bot(BOT_TOKEN); await web_server(); print('🤖 AI Comfort Signal bot started',flush=True)
    try: await dp.start_polling(bot)
    finally: await bot.session.close()
if __name__=='__main__': asyncio.run(main())
