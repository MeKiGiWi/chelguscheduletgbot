#!/usr/bin/env python3
"""
Comprehensive test script to verify all functionality including:
1. Blockquote formatting
2. Multi-week navigation
3. Database integration
"""

from database.models import Database
from utils.schedule_utils import get_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
from datetime import datetime, date
import json


def test_comprehensive_functionality():
    """Test comprehensive functionality"""
    print("Testing comprehensive functionality...")

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

    # Test navigation for multiple weeks
    print("\nTesting navigation for multiple weeks:")

    # Test current week (offset 0)
    keyboard_0 = get_week_navigation_keyboard(0)
    print("✓ Navigation keyboard for current week created")

    # Test next week (offset 1)
    keyboard_1 = get_week_navigation_keyboard(1)
    print("✓ Navigation keyboard for next week created")

    # Test 10 weeks ahead (offset 10)
    keyboard_10 = get_week_navigation_keyboard(10)
    print("✓ Navigation keyboard for 10 weeks ahead created")

    # Verify keyboard structure for 10 weeks ahead
    buttons_10 = keyboard_10.inline_keyboard[0]
    prev_data_10 = json.loads(
        buttons_10[0].callback_data[9:]
    )  # Remove "schedule_" prefix
    current_data_10 = json.loads(buttons_10[1].callback_data[9:])
    next_data_10 = json.loads(buttons_10[2].callback_data[9:])

    # Check that offsets are correct for 10 weeks ahead
    assert (
        prev_data_10["offset"] == 9
    ), f"Previous button offset should be 9, got {prev_data_10['offset']}"
    assert (
        current_data_10["offset"] == 0
    ), f"Current button offset should be 0, got {current_data_10['offset']}"
    assert (
        next_data_10["offset"] == 11
    ), f"Next button offset should be 11, got {next_data_10['offset']}"

    print("✓ Navigation offsets verified for 10 weeks ahead")

    # Test schedule formatting with blockquotes
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()

    # Add a lesson on Monday of current week
    start_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=9, minute=0)
    )
    end_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=10, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=db.add_schedule(group_id, week_start),
        subject_id=subject_id,
        teacher_id=teacher_id,
        start_time=start_time,
        end_time=end_time,
        location="--каф. 919",
        day_of_week=0,  # Monday
    )
    print(f"✓ Added lesson with ID: {lesson_id}")

    # Get formatted schedule
    schedule_message = get_week_schedule(group_id, db, 0, "М8О-207БВ-24")
    print("✓ Schedule formatting successful")

    # Verify blockquote formatting
    assert "<blockquote>" in schedule_message, "Message should contain blockquote tags"
    assert (
        "</blockquote>" in schedule_message
    ), "Message should contain closing blockquote tags"
    assert "<code>" not in schedule_message, "Message should not contain code tags"

    print("✓ Blockquote formatting verified")

    # Print sample output
    print("\nSample formatted schedule message:")
    print("=" * 50)
    print(schedule_message)
    print("=" * 50)

    # Print sample navigation data
    print("\nSample navigation button data for 10 weeks ahead:")
    print(f"  Previous week (9): {buttons_10[0].callback_data}")
    print(f"  Current week (0): {buttons_10[1].callback_data}")
    print(f"  Next week (11): {buttons_10[2].callback_data}")

    print("\nAll comprehensive tests passed!")


if __name__ == "__main__":
    test_comprehensive_functionality()
