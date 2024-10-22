import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import aiohttp
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения случайного факта из API SpaceX
async def get_random_spacex_fact():
    url = "https://api.spacexdata.com/v4/history"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()  # Получаем список всех событий
                random_event = random.choice(data)  # Выбираем случайное событие
                return random_event
            else:
                return None

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    event = await get_random_spacex_fact()  # Получаем случайный факт

    if event:
        # Формируем сообщение с информацией о событии
        title = event['title']
        details = event['details']
        date = event['event_date_utc']
        article = event['links'].get('article', 'Нет ссылки')

        fact_message = f"🚀 **{title}**\n\nДата: {date}\n\n{details}\n\n[Читать подробнее]({article})"
        await message.answer(fact_message, parse_mode="Markdown", disable_web_page_preview=False)
    else:
        await message.answer("Не удалось получить данные о событиях. Попробуйте позже.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
