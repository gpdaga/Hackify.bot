import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from app.handlers import router

load_dotenv()

async def main():
    bot_token = os.getenv("TG_TOKEN")
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    print('бот запущен')
    asyncio.run(main())