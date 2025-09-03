#!/usr/bin/env python3
"""
Handler for group confirmation callbacks
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.navigation import get_week_navigation_keyboard
from utils.schedule_utils import get_current_week_schedule
from database.models import Database
import json
import logging
import sqlite3

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("grp_"))
async def group_confirmation_handler(callback: CallbackQuery, db: Database):
    """Handle group confirmation callbacks"""
    try:
        # Parse callback data
        if callback.data.startswith("grp_yes:"):
            action = "confirm_group"
            group_id = int(callback.data.split(":")[1])
        elif callback.data.startswith("grp_no:"):
            action = "cancel_group"
            group_id = int(callback.data.split(":")[1])
        else:
            # Handle unexpected callback data
            await callback.answer("Invalid callback data", show_alert=True)
            return

        # Get group name from database
        connection = sqlite3.connect(db.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM groups WHERE id = ?", (group_id,))
        result = cursor.fetchone()
        connection.close()

        if not result:
            await callback.answer("Group not found", show_alert=True)
            return

        group_name = result[0]

        if action == "confirm_group":
            # User confirmed the group, show the schedule
            schedule_message = get_current_week_schedule(group_id, db, group_name)

            # Edit the message to remove the confirmation and show schedule
            await callback.message.edit_text(
                schedule_message, reply_markup=get_week_navigation_keyboard()
            )
        elif action == "cancel_group":
            # User cancelled, delete the message
            await callback.message.delete()

        # Answer the callback query to remove the loading indicator
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in group_confirmation_handler: {e}")
        await callback.answer(
            "Sorry, an error occurred. Please try again later.", show_alert=True
        )
