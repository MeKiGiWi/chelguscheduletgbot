#!/usr/bin/env python3
"""
Handler for group selection functionality
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.group_selection import get_group_confirmation_keyboard
from utils.schedule_utils import get_current_week_schedule
from database.models import Database
import logging
import re
import sqlite3

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


@router.message(F.text)
async def group_input_handler(message: Message, db: Database):
    """Handle group name input from user"""
    try:
        user_input = message.text.strip()

        # Search for matching groups
        matching_groups = search_matching_groups(user_input, db)

        if not matching_groups:
            await message.answer(
                "Группа не найдена. Пожалуйста, проверьте название и попробуйте снова."
            )
            return

        # Get the best matching group
        best_match = matching_groups[0]

        # Create confirmation message with bold and underlined group name
        confirmation_message = (
            f"Может быть <b><u>{best_match['name']}</u></b>?\n\n"
            f"Факультет: {best_match['faculty']}"
        )

        # Send confirmation message with buttons
        await message.answer(
            confirmation_message,
            reply_markup=get_group_confirmation_keyboard(
                best_match["id"], best_match["name"]
            ),
        )
    except Exception as e:
        logger.error(f"Error in group_input_handler: {e}")
        await message.answer(
            "Sorry, an error occurred while processing your request. Please try again later."
        )


def search_matching_groups(user_input: str, db: Database):
    """
    Search for groups that match the user input

    Args:
        user_input (str): User's group name input
        db (Database): Database instance

    Returns:
        list: List of matching groups
    """
    try:
        # Get all groups from database
        connection = sqlite3.connect(db.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, faculty FROM groups")
        all_groups = cursor.fetchall()
        connection.close()

        # Normalize user input (remove spaces and hyphens)
        normalized_input = re.sub(r"[\s\-]+", "", user_input.lower())

        matching_groups = []

        for group in all_groups:
            group_id, group_name, faculty = group
            # Normalize group name (remove spaces and hyphens)
            normalized_group_name = re.sub(r"[\s\-]+", "", group_name.lower())

            # Check for exact match
            if group_name.lower() == user_input.lower():
                matching_groups.append(
                    {
                        "id": group_id,
                        "name": group_name,
                        "faculty": faculty,
                        "match_type": "exact",
                    }
                )
                # If exact match, prioritize it
                if len(matching_groups) > 1:
                    matching_groups.insert(0, matching_groups.pop())
                continue

            # Check for partial match (user input contains group name)
            if normalized_input in normalized_group_name:
                matching_groups.append(
                    {
                        "id": group_id,
                        "name": group_name,
                        "faculty": faculty,
                        "match_type": "partial_contains",
                    }
                )

            # Check for partial match (group name contains user input)
            if normalized_group_name in normalized_input:
                matching_groups.append(
                    {
                        "id": group_id,
                        "name": group_name,
                        "faculty": faculty,
                        "match_type": "group_contains",
                    }
                )

        return matching_groups
    except Exception as e:
        logger.error(f"Error in search_matching_groups: {e}")
        return []
