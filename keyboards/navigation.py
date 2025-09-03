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
    # Create callback data for each button with adjusted offsets
    prev_week_data = json.dumps(
        {
            "action": "prev",
            "offset": current_offset - 1,
            "current_offset": current_offset,
        }
    )
    current_week_data = json.dumps(
        {"action": "current", "offset": 0, "current_offset": current_offset}
    )
    next_week_data = json.dumps(
        {
            "action": "next",
            "offset": current_offset + 1,
            "current_offset": current_offset,
        }
    )

    # Create the keyboard
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="←", callback_data=f"schedule_{prev_week_data}"
                ),
                InlineKeyboardButton(
                    text="🏠", callback_data=f"schedule_{current_week_data}"
                ),
                InlineKeyboardButton(
                    text="→", callback_data=f"schedule_{next_week_data}"
                ),
            ]
        ]
    )

    return keyboard
