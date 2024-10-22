import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    url = "https://api.imgflip.com/get_memes"
    memes_json = requests.get(url).json()
    number_of_memes = len(memes_json['data']['memes'])
    random_number = random.randint(0, number_of_memes - 1)
    meme_url = memes_json['data']['memes'][random_number]['url']
    meme_name = memes_json['data']['memes'][random_number]['name']
    await message.answer_photo(meme_url, caption=meme_name)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
