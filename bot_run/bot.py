import asyncio
import logging
import sys

from os import getenv

from aiogram.fsm.storage.memory import MemoryStorage

from routers import router
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from middlewares.i18n import i18n

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv("ADMINS")
DB_URL = getenv("DB_URL")

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def notify_admins(bot: Bot, text: str):
    admins_list = ADMINS.split(",")
    for admin in admins_list:
        try:
            await bot.send_message(admin, text)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin}: {e}")


async def on_startup(bot: Bot):
    await notify_admins(bot, "🤖 Бот запущен!")


async def on_shutdown(bot: Bot):
    await notify_admins(bot, "🛑 Бот остановлен!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.delete_webhook(drop_pending_updates=True)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.outer_middleware(i18n)

    await i18n.startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
