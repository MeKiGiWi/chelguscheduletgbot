from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.navigation import get_week_navigation_keyboard
from utils.schedule_utils import get_current_week_schedule, format_schedule_message
from database.models import Database
from config import DEFAULT_GROUP
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(message: Message, db: Database):
    """Handle the /start command"""
    try:
        await message.answer(
            "Введите название вашей группы, чтобы получить расписание."
        )
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await message.answer("Sorry, an error occurred. Please try again later.")
