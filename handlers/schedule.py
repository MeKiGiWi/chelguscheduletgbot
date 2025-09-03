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


@router.callback_query(F.data.startswith("sch_"))
async def schedule_navigation_handler(callback: CallbackQuery, db: Database):
    """Handle schedule navigation callbacks"""
    try:
        # Parse callback data (short format to avoid Telegram limits)
        # Format: sch_action:offset:current_offset
        parts = callback.data.split(":")
        if len(parts) != 3:
            await callback.answer("Invalid callback data", show_alert=True)
            return

        action = parts[0][4:]  # Remove "sch_" prefix
        offset = int(parts[1])
        current_offset = int(parts[2])

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
