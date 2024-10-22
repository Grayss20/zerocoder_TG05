import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import requests
import aiohttp
import os

from config import TOKEN, BACKGROUND_API_KEY  # Add your background removal API key here

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Step 1: Download the image from Telegram and send it to the background removal API
async def remove_background(image_url):
    # Step 2: Prepare the API request
    api_url = "https://api.hotpot.ai/remove-background"
    headers = {
        'Authorization': BACKGROUND_API_KEY
    }

    data = {
        'imageUrl': image_url,  # Image URL to send to the API
    }

    # Sending the request to the API
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=data) as response:
            if response.status == 200:
                # Save the result image
                result = await response.read()
                output_file = "edited_image.png"
                with open(output_file, "wb") as f:
                    f.write(result)
                return output_file
            else:
                print(f"Error: {response.status} - {await response.text()}")
                return None


@dp.message(F.photo)
async def handle_photo(message: Message):
    # Step 1: Download the user's photo
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Download the image from Telegram
    image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Step 2: Send the image to the background removal API
    edited_image = await remove_background(image_url)

    if edited_image:
        # Step 3: Send the edited image back to the user
        with open(edited_image, 'rb') as photo:
            await message.answer_photo(photo)
        os.remove(edited_image)  # Optionally, remove the image after sending it
    else:
        await message.answer("Извините, произошла ошибка при обработке изображения.")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для удаления фона с твоей фотографии. Просто отправь свою фото и я верну ее с прозрачным фоном."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
