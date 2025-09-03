#!/usr/bin/env python3
"""
Test script to verify the fixed group selection functionality
"""

from database.models import Database
from keyboards.group_selection import get_group_confirmation_keyboard
from handlers.group_confirmation import group_confirmation_handler
import json


def test_fixed_group_selection():
    """Test fixed group selection functionality"""
    print("Testing fixed group selection functionality...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test group
    group_id = db.add_group("М8О-207БВ-24", "Computer Science")
    print(f"✓ Added group with ID: {group_id}")

    # Test group confirmation keyboard
    print("\nTesting group confirmation keyboard...")
    keyboard = get_group_confirmation_keyboard(group_id, "М8О-207БВ-24")

    # Verify keyboard structure
    assert keyboard.inline_keyboard is not None, "Keyboard should have inline_keyboard"
    assert len(keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert len(keyboard.inline_keyboard[0]) == 2, "Keyboard should have two buttons"

    # Check button texts
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].text == "Да", "First button should be 'Да'"
    assert buttons[1].text == "Нет", "Second button should be 'Нет'"

    # Check callback data format (should be short and simple)
    assert buttons[0].callback_data.startswith(
        "grp_yes:"
    ), "First button should have 'grp_yes:' prefix"
    assert buttons[1].callback_data.startswith(
        "grp_no:"
    ), "Second button should have 'grp_no:' prefix"

    # Check that callback data contains the group ID
    yes_group_id = int(buttons[0].callback_data.split(":")[1])
    no_group_id = int(buttons[1].callback_data.split(":")[1])
    assert yes_group_id == group_id, "Yes button should have correct group ID"
    assert no_group_id == group_id, "No button should have correct group ID"

    # Check that callback data is short enough for Telegram
    assert (
        len(buttons[0].callback_data) <= 64
    ), "Callback data should be <= 64 characters"
    assert (
        len(buttons[1].callback_data) <= 64
    ), "Callback data should be <= 64 characters"

    print("✓ Group confirmation keyboard verified")
    print(f"  Да button callback data: {buttons[0].callback_data}")
    print(f"  Нет button callback data: {buttons[1].callback_data}")

    print("\n" + "=" * 50)
    print("FIXED GROUP SELECTION TEST PASSED!")
    print("All features are working correctly:")
    print(" ✓ Short callback data format")
    print(" ✓ Callback data within Telegram limits")
    print(" ✓ Proper group ID encoding")
    print(" ✓ Correct button labels")
    print("=" * 50)


if __name__ == "__main__":
    test_fixed_group_selection()
