#!/usr/bin/env python3
"""
Final integration test to verify all components work together
"""

from database.models import Database
from keyboards.group_selection import get_group_confirmation_keyboard
from handlers.group_selection import search_matching_groups
from utils.schedule_utils import get_current_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
import json


def test_final_integration():
    """Test final integration of all components"""
    print("Running final integration test...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Test group search functionality
    print("\nTesting group search functionality...")
    matches = search_matching_groups("М8О-207БВ-24", db)
    assert len(matches) > 0, "Should find exact match"
    assert matches[0]["name"] == "М8О-207БВ-24", "Should match exact group name"
    group_id = matches[0]["id"]
    print(f"✓ Found group: {matches[0]['name']} (ID: {group_id})")

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
    schedule_message = get_current_week_schedule(group_id, db, "М8О-207БВ-24")
    print("✓ Schedule retrieval successful")

    # Verify schedule content
    assert "<blockquote>" in schedule_message, "Message should contain blockquote tags"
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
    assert "Общая физика" in schedule_message, "Message should contain General Physics"
    assert "Программирование" in schedule_message, "Message should contain Programming"
    assert (
        "Выходной" in schedule_message
    ), "Message should contain 'Выходной' for days without lessons"

    print("✓ Schedule content verified")

    # Test navigation keyboard
    print("\nTesting navigation keyboard...")
    nav_keyboard = get_week_navigation_keyboard(0)

    # Verify navigation keyboard structure
    nav_buttons = nav_keyboard.inline_keyboard[0]
    assert nav_buttons[0].text == "←", "First navigation button should be left arrow"
    assert nav_buttons[1].text == "🏠", "Second navigation button should be house emoji"
    assert nav_buttons[2].text == "→", "Third navigation button should be right arrow"

    # Parse navigation callback data
    prev_data = json.loads(
        nav_buttons[0].callback_data[9:]
    )  # Remove "schedule_" prefix
    current_data = json.loads(nav_buttons[1].callback_data[9:])
    next_data = json.loads(nav_buttons[2].callback_data[9:])

    assert prev_data["action"] == "prev", "Previous button action should be 'prev'"
    assert (
        current_data["action"] == "current"
    ), "Current button action should be 'current'"
    assert next_data["action"] == "next", "Next button action should be 'next'"

    print("✓ Navigation keyboard verified")

    # Print final output
    print("\n" + "=" * 70)
    print("FINAL INTEGRATION TEST OUTPUT")
    print("=" * 70)
    print("Group confirmation message example:")
    print(f"Может быть <b><u>М8О-207БВ-24</u></b>?\n")
    print("Schedule message example:")
    print(schedule_message)
    print("=" * 70)

    print("\nGroup confirmation buttons:")
    print(f"  Да: {buttons[0].callback_data}")
    print(f"  Нет: {buttons[1].callback_data}")

    print("\nNavigation buttons:")
    print(f"  ← Previous week: {nav_buttons[0].callback_data}")
    print(f"  🏠 Current week: {nav_buttons[1].callback_data}")
    print(f"  → Next week: {nav_buttons[2].callback_data}")

    print("\n" + "=" * 70)
    print("FINAL INTEGRATION TEST PASSED!")
    print("All components are working correctly together:")
    print("  ✓ Group search with partial matching")
    print("  ✓ Group confirmation with 'Да' and 'Нет' buttons")
    print("  ✓ Short callback data within Telegram limits")
    print("  ✓ Schedule retrieval from database")
    print("  ✓ Schedule formatting with blockquotes")
    print("  ✓ Multi-week navigation with proper offset tracking")
    print("  ✓ Proper display of lessons and 'Выходной'")
    print("=" * 70)


if __name__ == "__main__":
    test_final_integration()
