from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


def get_week_navigation_keyboard(current_offset: int = 0) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for week navigation

    Args:
        current_offset (int): Current week offset from current week

    Returns:
        InlineKeyboardMarkup: Keyboard with previous, current, and next week buttons
    """
    # Create callback data for each button with adjusted offsets (short format to avoid Telegram limits)
    prev_week_data = f"sch_prev:{current_offset - 1}:{current_offset}"
    current_week_data = f"sch_curr:0:{current_offset}"
    next_week_data = f"sch_next:{current_offset + 1}:{current_offset}"

    # Create the keyboard
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="←", callback_data=prev_week_data),
                InlineKeyboardButton(text="🏠", callback_data=current_week_data),
                InlineKeyboardButton(text="→", callback_data=next_week_data),
            ]
        ]
    )

    return keyboard
