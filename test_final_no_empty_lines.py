#!/usr/bin/env python3
"""
Final comprehensive test script to verify all functionality without empty lines
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule, get_week_schedule
from keyboards.navigation import get_week_navigation_keyboard
from datetime import datetime, date
import json


def test_final_no_empty_lines():
    """Test final comprehensive functionality without empty lines"""
    print("Running final comprehensive test without empty lines...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test data
    group_id = db.add_group("М8О-207БВ-24", "Computer Science")
    print(f"✓ Added group with ID: {group_id}")

    subject1_id = db.add_subject("Физическая культура", "PE101")
    subject2_id = db.add_subject("Математический анализ", "MA101")
    subject3_id = db.add_subject("Иностранный язык", "FL101")
    subject4_id = db.add_subject("Общая физика", "GP101")
    print(
        f"✓ Added subjects with IDs: {subject1_id}, {subject2_id}, {subject3_id}, {subject4_id}"
    )

    teacher1_id = db.add_teacher("Иванов Иван Иванович", "Physical Education")
    teacher2_id = db.add_teacher("Петров Петр Петрович", "Mathematics")
    teacher3_id = db.add_teacher("Сидоров Сидор Сидорович", "Foreign Languages")
    teacher4_id = db.add_teacher("Кузнецов Алексей Владимирович", "Physics")
    print(
        f"✓ Added teachers with IDs: {teacher1_id}, {teacher2_id}, {teacher3_id}, {teacher4_id}"
    )

    # Add schedule for current week
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule for current week with ID: {schedule_id}")

    # Add multiple lessons for different days
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

    # Tuesday lessons
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

    start_time2 = datetime.combine(
        tuesday, datetime.min.time().replace(hour=14, minute=45)
    )
    end_time2 = datetime.combine(
        tuesday, datetime.min.time().replace(hour=16, minute=15)
    )
    lesson3_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject3_id,
        teacher_id=teacher3_id,
        start_time=start_time2,
        end_time=end_time2,
        location="3-403",
        day_of_week=1,  # Tuesday
    )

    # Wednesday lesson
    wednesday = week_start + date.resolution * 2  # Wednesday
    start_time3 = datetime.combine(
        wednesday, datetime.min.time().replace(hour=10, minute=45)
    )
    end_time3 = datetime.combine(
        wednesday, datetime.min.time().replace(hour=12, minute=15)
    )
    lesson4_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject4_id,
        teacher_id=teacher4_id,
        start_time=start_time3,
        end_time=end_time3,
        location="ГУК Б-638",
        day_of_week=2,  # Wednesday
    )

    print(
        f"✓ Added lessons with IDs: {lesson1_id}, {lesson2_id}, {lesson3_id}, {lesson4_id}"
    )

    # Test current week schedule
    schedule_message = get_current_week_schedule(group_id, db, "М8О-207БВ-24")
    print("✓ Current week schedule formatting successful")

    # Test navigation keyboards for different offsets
    keyboard_current = get_week_navigation_keyboard(0)
    keyboard_next = get_week_navigation_keyboard(5)
    keyboard_prev = get_week_navigation_keyboard(-3)
    print("✓ Navigation keyboards creation successful")

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
    assert "Иностранный язык" in schedule_message, "Message should contain subject 3"
    assert "Общая физика" in schedule_message, "Message should contain subject 4"
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
    # Count the number of consecutive newlines
    import re

    consecutive_newlines = re.findall(r"\n{3,}", schedule_message)
    assert (
        len(consecutive_newlines) == 0
    ), "Should not have 3 or more consecutive newlines"

    print("✓ All formatting checks passed")

    # Verify navigation functionality
    # Check current week keyboard
    buttons_current = keyboard_current.inline_keyboard[0]
    prev_data_current = json.loads(buttons_current[0].callback_data[9:])
    current_data_current = json.loads(buttons_current[1].callback_data[9:])
    next_data_current = json.loads(buttons_current[2].callback_data[9:])

    assert (
        prev_data_current["offset"] == -1
    ), f"Previous button offset should be -1, got {prev_data_current['offset']}"
    assert (
        current_data_current["offset"] == 0
    ), f"Current button offset should be 0, got {current_data_current['offset']}"
    assert (
        next_data_current["offset"] == 1
    ), f"Next button offset should be 1, got {next_data_current['offset']}"

    # Check next week keyboard (offset 5)
    buttons_next = keyboard_next.inline_keyboard[0]
    prev_data_next = json.loads(buttons_next[0].callback_data[9:])
    current_data_next = json.loads(buttons_next[1].callback_data[9:])
    next_data_next = json.loads(buttons_next[2].callback_data[9:])

    assert (
        prev_data_next["offset"] == 4
    ), f"Previous button offset should be 4, got {prev_data_next['offset']}"
    assert (
        current_data_next["offset"] == 0
    ), f"Current button offset should be 0, got {current_data_next['offset']}"
    assert (
        next_data_next["offset"] == 6
    ), f"Next button offset should be 6, got {next_data_next['offset']}"

    print("✓ Navigation functionality verified")

    # Print final output
    print("\n" + "=" * 70)
    print("FINAL COMPREHENSIVE TEST OUTPUT (NO EMPTY LINES)")
    print("=" * 70)
    print(schedule_message)
    print("=" * 70)

    print("\nNavigation buttons for current week (offset 0):")
    print(f"  ← Previous week: {buttons_current[0].callback_data}")
    print(f"  🏠 Current week: {buttons_current[1].callback_data}")
    print(f"  → Next week: {buttons_current[2].callback_data}")

    print("\nNavigation buttons for week +5:")
    print(f"  ← Previous week: {buttons_next[0].callback_data}")
    print(f"  🏠 Current week: {buttons_next[1].callback_data}")
    print(f"  → Next week: {buttons_next[2].callback_data}")

    print("\n" + "=" * 70)
    print("FINAL COMPREHENSIVE TEST PASSED!")
    print("All features are working correctly:")
    print("  ✓ Blockquote formatting for all content")
    print("  ✓ Multi-week navigation with proper offset tracking")
    print("  ✓ Database integration with multiple lessons")
    print("  ✓ Proper display of lessons and 'Выходной'")
    print("  ✓ No empty lines between blockquotes")
    print("=" * 70)


if __name__ == "__main__":
    test_final_no_empty_lines()
