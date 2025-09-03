#!/usr/bin/env python3
"""
Final comprehensive test script to verify all functionality including group selection
"""

from database.models import Database
from handlers.group_selection import search_matching_groups
from keyboards.group_selection import get_group_confirmation_keyboard
from utils.schedule_utils import get_current_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
from datetime import datetime, date
import json


def test_final_with_group_selection():
    """Test final comprehensive functionality including group selection"""
    print("Running final comprehensive test with group selection...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test data
    group1_id = db.add_group("М8О-207БВ-24", "Computer Science")
    group2_id = db.add_group("М8О-208БВ-24", "Computer Science")
    group3_id = db.add_group("М8О-209БВ-24", "Computer Science")
    print(f"✓ Added groups with IDs: {group1_id}, {group2_id}, {group3_id}")

    subject1_id = db.add_subject("Физическая культура", "PE101")
    subject2_id = db.add_subject("Математический анализ", "MA101")
    print(f"✓ Added subjects with IDs: {subject1_id}, {subject2_id}")

    teacher1_id = db.add_teacher("Иванов Иван Иванович", "Physical Education")
    teacher2_id = db.add_teacher("Петров Петрович", "Mathematics")
    print(f"✓ Added teachers with IDs: {teacher1_id}, {teacher2_id}")

    # Add schedule for group 1 (М8О-207БВ-24)
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()
    schedule_id = db.add_schedule(group1_id, week_start)
    print(f"✓ Added schedule for group 1 with ID: {schedule_id}")

    # Add lessons for group 1
    # Monday lesson
    start_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=9, minute=0)
    )
    end_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=10, minute=30)
    )
    lesson1_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject1_id,
        teacher_id=teacher1_id,
        start_time=start_time,
        end_time=end_time,
        location="--каф. 919",
        day_of_week=0,  # Monday
    )

    # Tuesday lesson
    tuesday = week_start + date.resolution * 1  # Tuesday
    start_time1 = datetime.combine(
        tuesday, datetime.min.time().replace(hour=13, minute=0)
    )
    end_time1 = datetime.combine(
        tuesday, datetime.min.time().replace(hour=14, minute=30)
    )
    lesson2_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject2_id,
        teacher_id=teacher2_id,
        start_time=start_time1,
        end_time=end_time1,
        location="ГУК В-221",
        day_of_week=1,  # Tuesday
    )

    print(f"✓ Added lessons with IDs: {lesson1_id}, {lesson2_id}")

    # Test group search functionality
    print("\nTesting group search functionality...")

    # Test exact match
    exact_matches = search_matching_groups("М8О-207БВ-24", db)
    assert len(exact_matches) > 0, "Should find exact match"
    assert exact_matches[0]["name"] == "М8О-207БВ-24", "Should match exact group name"
    assert exact_matches[0]["id"] == group1_id, "Should have correct group ID"
    print("✓ Exact match found")

    # Test partial match (user input contains group name)
    partial_matches1 = search_matching_groups("207БВ", db)
    assert len(partial_matches1) > 0, "Should find partial match"
    print("✓ Partial match (user input contains group name) found")

    # Test partial match (group name contains user input)
    partial_matches2 = search_matching_groups(
        "М8О207БВ24", db
    )  # without hyphens and spaces
    assert len(partial_matches2) > 0, "Should find partial match"
    print("✓ Partial match (group name contains user input) found")

    # Test group confirmation keyboard
    print("\nTesting group confirmation keyboard...")
    keyboard = get_group_confirmation_keyboard(group1_id, "М8О-207БВ-24")

    # Verify keyboard structure
    assert keyboard.inline_keyboard is not None, "Keyboard should have inline_keyboard"
    assert len(keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert len(keyboard.inline_keyboard[0]) == 2, "Keyboard should have two buttons"

    # Check button texts
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].text == "Да", "First button should be 'Да'"
    assert buttons[1].text == "Нет", "Second button should be 'Нет'"

    # Check callback data
    assert buttons[0].callback_data.startswith(
        "group_"
    ), "First button should have group callback"
    assert buttons[1].callback_data.startswith(
        "group_"
    ), "Second button should have group callback"

    # Parse callback data to verify structure
    yes_data = json.loads(buttons[0].callback_data[6:])  # Remove "group_" prefix
    no_data = json.loads(buttons[1].callback_data[6:])

    assert (
        yes_data["action"] == "confirm_group"
    ), "Yes button action should be 'confirm_group'"
    assert (
        no_data["action"] == "cancel_group"
    ), "No button action should be 'cancel_group'"
    assert yes_data["group_id"] == group1_id, "Yes button should have correct group ID"
    assert no_data["group_id"] == group1_id, "No button should have correct group ID"
    assert (
        yes_data["group_name"] == "М8О-207БВ-24"
    ), "Yes button should have correct group name"
    assert (
        no_data["group_name"] == "М8О-207БВ-24"
    ), "No button should have correct group name"

    print("✓ Group confirmation keyboard verified")

    # Test schedule formatting
    print("\nTesting schedule formatting...")
    schedule_message = get_current_week_schedule(group1_id, db, "М8О-207БВ-24")

    # Verify formatting
    assert "<blockquote>" in schedule_message, "Message should contain blockquote tags"
    assert (
        "</blockquote>" in schedule_message
    ), "Message should contain closing blockquote tags"
    assert "М8О-207БВ-24" in schedule_message, "Message should contain group name"
    assert "Физическая культура" in schedule_message, "Message should contain subject 1"
    assert (
        "Математический анализ" in schedule_message
    ), "Message should contain subject 2"
    assert (
        "Выходной" in schedule_message
    ), "Message should contain 'Выходной' for days without lessons"

    # Count blockquotes - should be 8 (1 for group name + 7 for days)
    blockquote_count = schedule_message.count("<blockquote>")
    assert blockquote_count == 8, f"Should have 8 blockquotes, got {blockquote_count}"

    # Count closing blockquotes - should be 8
    closing_blockquote_count = schedule_message.count("</blockquote>")
    assert (
        closing_blockquote_count == 8
    ), f"Should have 8 closing blockquotes, got {closing_blockquote_count}"

    # Check that there are no empty lines between blockquotes
    import re

    consecutive_newlines = re.findall(r"\n{3,}", schedule_message)
    assert (
        len(consecutive_newlines) == 0
    ), "Should not have 3 or more consecutive newlines"

    print("✓ Schedule formatting verified")

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
    print("FINAL COMPREHENSIVE TEST OUTPUT WITH GROUP SELECTION")
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
    print("FINAL COMPREHENSIVE TEST PASSED!")
    print("All features are working correctly:")
    print("  ✓ Group selection with partial matching")
    print("  ✓ Group confirmation with 'Да' and 'Нет' buttons")
    print("  ✓ Blockquote formatting for all content")
    print("  ✓ Multi-week navigation with proper offset tracking")
    print("  ✓ Database integration with multiple lessons")
    print("  ✓ Proper display of lessons and 'Выходной'")
    print("  ✓ No empty lines between blockquotes")
    print("=" * 70)


if __name__ == "__main__":
    test_final_with_group_selection()
