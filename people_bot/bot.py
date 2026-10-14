import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database import PeopleDB

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
db = PeopleDB()

DATA_FILE = "test.json"


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт! Я бот для роботи з даними про людей.")


@dp.message(Command("load"))
async def load(message: Message):
    try:
        db.load(DATA_FILE)
    except FileNotFoundError:
        await message.answer("Файл не знайдено")
        return
    await message.answer(f"Завантажено записів: {len(db.people)}")


@dp.message(Command("save"))
async def save(message: Message):
    db.save(DATA_FILE)
    await message.answer(f"Збережено записів: {len(db.people)}")


@dp.message(Command("search"))
async def search(message: Message):
    query = message.text.removeprefix("/search").strip()
    if not query:
        await message.answer("Напишіть рядок для пошуку, наприклад: /search євген")
        return
    results = db.search(query)
    if not results:
        await message.answer("Нікого не знайдено")
        return
    await message.answer("\n\n".join(str(p) for p in results))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())