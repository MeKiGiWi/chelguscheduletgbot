from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.navigation import get_week_navigation_keyboard
from utils.schedule_utils import get_week_schedule, format_schedule_message
from database.models import Database
from config import DEFAULT_GROUP
import json
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("schedule_"))
async def schedule_navigation_handler(callback: CallbackQuery, db: Database):
    """Handle schedule navigation callbacks"""
    try:
        # Parse callback data
        data = json.loads(callback.data[9:])  # Remove "schedule_" prefix
        action = data.get("action")
        offset = data.get("offset", 0)
        current_offset = data.get("current_offset", 0)

        # Get the group ID for the default group
        group_id = db.get_or_create_group(DEFAULT_GROUP, "Computer Science")

        # Get schedule based on action
        schedule_message = get_week_schedule(group_id, db, offset, "М8О-207БВ-24")

        # Edit the message with the new schedule
        await callback.message.edit_text(
            schedule_message, reply_markup=get_week_navigation_keyboard(offset)
        )

        # Answer the callback query to remove the loading indicator
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in schedule_navigation_handler: {e}")
        await callback.answer(
            "Sorry, an error occurred while fetching the schedule. Please try again later.",
            show_alert=True,
        )
