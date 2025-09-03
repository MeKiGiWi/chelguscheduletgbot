#!/usr/bin/env python3
"""
Keyboard for group selection confirmation
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


def get_group_confirmation_keyboard(
    group_id: int, group_name: str
) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for group confirmation

    Args:
        group_id (int): ID of the group
        group_name (str): Name of the group

    Returns:
        InlineKeyboardMarkup: Keyboard with Yes and No buttons
    """
    # Create callback data for each button (keeping it short to avoid Telegram limits)
    yes_data = f"grp_yes:{group_id}"
    no_data = f"grp_no:{group_id}"

    # Create the keyboard
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=yes_data),
                InlineKeyboardButton(text="Нет", callback_data=no_data),
            ]
        ]
    )

    return keyboard
