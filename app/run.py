from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.handlers import (
    main_menu,
    ddos_handler,
    deepseek_handler,
    sqlmap_handler,
    support_handler,
    premium_handler,
    osint_handler  # Добавлен новый обработчик
)
from app.config import Config
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    config = Config()
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    dp.include_router(main_menu.router)
    dp.include_router(ddos_handler.router)
    dp.include_router(deepseek_handler.router)
    dp.include_router(sqlmap_handler.router)
    dp.include_router(support_handler.router)
    dp.include_router(premium_handler.router)
    dp.include_router(osint_handler.router)  # Добавлен OSINT

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())