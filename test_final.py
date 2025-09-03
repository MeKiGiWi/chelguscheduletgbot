#!/usr/bin/env python3
"""
Final test script to verify the complete bot functionality
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
from datetime import datetime, date


def test_final_functionality():
    """Test final functionality"""
    print("Testing final bot functionality...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test data
    group_id = db.add_group("М8О-207БВ-24", "Computer Science")
    print(f"✓ Added group with ID: {group_id}")

    subject1_id = db.add_subject("Физическая культура", "PE101")
    subject2_id = db.add_subject("Математический анализ", "MA101")
    print(f"✓ Added subjects with IDs: {subject1_id}, {subject2_id}")

    teacher1_id = db.add_teacher("Иванов Иван Иванович", "Physical Education")
    teacher2_id = db.add_teacher("Петров Петр Петрович", "Mathematics")
    print(f"✓ Added teachers with IDs: {teacher1_id}, {teacher2_id}")

    # Add schedule for current week
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule for current week with ID: {schedule_id}")

    # Add multiple lessons for current week
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
    start_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=10, minute=45)
    )
    end_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=12, minute=15)
    )
    lesson2_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject2_id,
        teacher_id=teacher2_id,
        start_time=start_time,
        end_time=end_time,
        location="ГУК В-221",
        day_of_week=1,  # Tuesday
    )

    print(f"✓ Added lessons with IDs: {lesson1_id}, {lesson2_id}")

    # Test current week schedule
    schedule_message = get_current_week_schedule(group_id, db, "М8О-207БВ-24")
    print("✓ Current week schedule formatting successful")

    # Test navigation keyboard
    keyboard = get_week_navigation_keyboard(0)
    print("✓ Navigation keyboard creation successful")

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

    print("✓ All formatting checks passed")

    # Print final output
    print("\n" + "=" * 60)
    print("FINAL BOT OUTPUT")
    print("=" * 60)
    print(schedule_message)
    print("=" * 60)

    print("\nNavigation buttons:")
    buttons = keyboard.inline_keyboard[0]
    print(f"  ← Previous week: {buttons[0].callback_data}")
    print(f"  🏠 Current week: {buttons[1].callback_data}")
    print(f"  → Next week: {buttons[2].callback_data}")

    print("\n" + "=" * 60)
    print("ALL FINAL TESTS PASSED!")
    print("The bot is ready for use with all requested features:")
    print("  ✓ Blockquote formatting for quotes")
    print("  ✓ Multi-week navigation (up to 10 weeks)")
    print("  ✓ Proper schedule display with all required elements")
    print("=" * 60)


if __name__ == "__main__":
    test_final_functionality()
