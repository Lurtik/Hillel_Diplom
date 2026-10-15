import asyncio
import os


from database import PeopleDB
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
db = PeopleDB()
DATA_FILENAME = "person.json"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        """Привіт! 👋
        Я бот для роботи з даними про людей.
    
        Що я вмію:
        /load — завантажити записи з файлу
        /add — додати людину
        /search — знайти людей за ім'ям, прізвищем або по батькові
        /save — зберегти записи у файл
    
        Приклад пошуку: /search євген"""
    )

@dp.message(Command("search"))
async def cmd_search(message: Message):
    query = message.text.removeprefix("/search").strip()
    if not query:
        await message.answer("Напишіть рядок для пошуку, наприклад: /search євген")
        return
    results = db.search(query)
    if not results:
        await message.answer("Нікого не знайдено")
        return
    text = "\n".join(str(p) for p in results)
    await message.answer(text)

@dp.message(Command("load"))
async def cmd_load(message: Message):
    try:
        db.load(DATA_FILENAME)
    except FileNotFoundError:
        await message.answer("Файл не знайдено")
        return
    await message.answer(f"Завантажено записів: {len(db.people)}")

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")