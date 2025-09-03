#!/usr/bin/env python3
"""
Test script to verify the group confirmation handler works with test data
"""

from database.models import Database
from keyboards.group_selection import get_group_confirmation_keyboard
from utils.schedule_utils import get_current_week_schedule
import json


def test_group_confirmation_with_data():
    """Test group confirmation handler with test data"""
    print("Testing group confirmation handler with test data...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Get the test group
    group_id = db.get_group_id_by_name("М8О-207БВ-24")
    if not group_id:
        print("✗ Test group not found in database")
        return

    print(f"✓ Found test group: М8О-207БВ-24 (ID: {group_id})")

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

    # Check callback data format
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

    print("✓ Group confirmation keyboard verified")
    print(f"  Да button callback data: {buttons[0].callback_data}")
    print(f"  Нет button callback data: {buttons[1].callback_data}")

    # Test schedule retrieval
    print("\nTesting schedule retrieval...")
    try:
        schedule_message = get_current_week_schedule(group_id, db, "М8О-207БВ-24")
        print("✓ Schedule retrieval successful")

        # Verify schedule content
        assert (
            "<blockquote>" in schedule_message
        ), "Message should contain blockquote tags"
        assert (
            "</blockquote>" in schedule_message
        ), "Message should contain closing blockquote tags"
        assert "М8О-207БВ-24" in schedule_message, "Message should contain group name"
        assert (
            "Физическая культура" in schedule_message
        ), "Message should contain Physical Education"
        assert (
            "Математический анализ" in schedule_message
        ), "Message should contain Mathematical Analysis"
        assert (
            "Иностранный язык" in schedule_message
        ), "Message should contain Foreign Language"
        assert (
            "Общая физика" in schedule_message
        ), "Message should contain General Physics"
        assert (
            "Программирование" in schedule_message
        ), "Message should contain Programming"
        assert (
            "Выходной" in schedule_message
        ), "Message should contain 'Выходной' for days without lessons"

        print("✓ Schedule content verified")

        # Print sample schedule
        print("\nSample schedule output:")
        print("=" * 50)
        print(schedule_message)
        print("=" * 50)

    except Exception as e:
        print(f"✗ Error retrieving schedule: {e}")
        return

    print("\n" + "=" * 60)
    print("GROUP CONFIRMATION TEST WITH DATA PASSED!")
    print("All features are working correctly:")
    print(" ✓ Group confirmation keyboard with proper callback data")
    print(" ✓ Schedule retrieval from database")
    print(" ✓ Schedule formatting with blockquotes")
    print(" ✓ Display of test lessons")
    print(" ✓ Proper handling of days without lessons")
    print("=" * 60)


if __name__ == "__main__":
    test_group_confirmation_with_data()
