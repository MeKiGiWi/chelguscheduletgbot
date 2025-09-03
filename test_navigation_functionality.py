#!/usr/bin/env python3
"""
Test script to verify navigation functionality
"""

from database.models import Database
from utils.schedule_utils import get_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
from datetime import datetime, date
import json


def test_navigation_functionality():
    """Test navigation functionality"""
    print("Testing navigation functionality...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test data
    group_id = db.add_group("М8О-207БВ-24", "Computer Science")
    print(f"✓ Added group with ID: {group_id}")

    subject_id = db.add_subject("Физическая культура", "PE101")
    print(f"✓ Added subject with ID: {subject_id}")

    teacher_id = db.add_teacher("Иванов Иван Иванович", "Physical Education")
    print(f"✓ Added teacher with ID: {teacher_id}")

    # Add schedule for current week
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule for current week with ID: {schedule_id}")

    # Add a lesson on Monday of current week
    start_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=9, minute=0)
    )
    end_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=10, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_id,
        teacher_id=teacher_id,
        start_time=start_time,
        end_time=end_time,
        location="--каф. 919",
        day_of_week=0,  # Monday
    )
    print(f"✓ Added lesson with ID: {lesson_id}")

    # Test current week schedule
    schedule_message = get_week_schedule(group_id, db, 0, "М8О-207БВ-24")
    print("✓ Current week schedule formatting successful")

    # Test navigation keyboard
    keyboard = get_week_navigation_keyboard(0)
    print("✓ Navigation keyboard creation successful")

    # Verify keyboard structure
    assert keyboard.inline_keyboard is not None, "Keyboard should have inline_keyboard"
    assert len(keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert len(keyboard.inline_keyboard[0]) == 3, "Keyboard should have three buttons"

    # Check button texts
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].text == "←", "First button should be left arrow"
    assert buttons[1].text == "🏠", "Second button should be house emoji"
    assert buttons[2].text == "→", "Third button should be right arrow"

    # Check callback data
    assert buttons[0].callback_data.startswith(
        "schedule_"
    ), "First button should have schedule callback"
    assert buttons[1].callback_data.startswith(
        "schedule_"
    ), "Second button should have schedule callback"
    assert buttons[2].callback_data.startswith(
        "schedule_"
    ), "Third button should have schedule callback"

    # Parse callback data to verify structure
    prev_data = json.loads(buttons[0].callback_data[9:])  # Remove "schedule_" prefix
    current_data = json.loads(buttons[1].callback_data[9:])
    next_data = json.loads(buttons[2].callback_data[9:])

    assert (
        prev_data["action"] == "prev" and prev_data["offset"] == -1
    ), "Previous button data incorrect"
    assert (
        current_data["action"] == "current" and current_data["offset"] == 0
    ), "Current button data incorrect"
    assert (
        next_data["action"] == "next" and next_data["offset"] == 1
    ), "Next button data incorrect"

    print("✓ Navigation button properties verified")

    print("\nFormatted schedule message for current week:")
    print("=" * 50)
    print(schedule_message)
    print("=" * 50)

    print("\nNavigation buttons:")
    print(f"  Previous week: {buttons[0].callback_data}")
    print(f"  Current week: {buttons[1].callback_data}")
    print(f"  Next week: {buttons[2].callback_data}")

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_navigation_functionality()
