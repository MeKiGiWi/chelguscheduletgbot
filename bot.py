import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from database.models import Database
from handlers import start, schedule, group_selection, group_confirmation

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set. Please set it in the .env file.")
        return

    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Initialize database
    database = Database()

    # Register handlers
    dp.include_router(start.router)
    dp.include_router(schedule.router)
    dp.include_router(group_selection.router)
    dp.include_router(group_confirmation.router)

    # Middleware to pass database to handlers
    @dp.update.outer_middleware()
    async def database_middleware(handler, event, data):
        data["db"] = database
        return await handler(event, data)

    # Add the middleware
    dp.update.outer_middleware(database_middleware)

    # Start polling
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
