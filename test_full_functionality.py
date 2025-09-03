#!/usr/bin/env python3
"""
Test script to verify full functionality including database and formatting
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule
from datetime import datetime, date, timedelta


def test_full_functionality():
    """Test full functionality including database and formatting"""
    print("Testing full functionality...")

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

    week_start = date(2025, 10, 6)  # Monday of the week
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule with ID: {schedule_id}")

    # Add a lesson on Monday
    start_time = datetime(2025, 10, 6, 9, 0)  # October 6, 2025, 9:00 AM
    end_time = datetime(2025, 10, 6, 10, 30)  # October 6, 2025, 10:30 AM
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

    # Calculate offset for the test week (October 6, 2025)
    # We need to calculate how many weeks from the current week to October 6, 2025
    from utils.schedule_utils import get_current_week_start

    current_week_start = get_current_week_start()
    target_week_start = date(2025, 10, 6)  # Monday of the target week

    # Calculate the offset in weeks
    from datetime import timedelta

    week_diff = target_week_start - current_week_start
    week_offset = week_diff.days // 7

    # Get formatted schedule for the specific week
    from utils.schedule_utils import get_week_schedule

    schedule_message = get_week_schedule(group_id, db, week_offset, "М8О-207БВ-24")
    print("✓ Schedule formatting successful")

    print("\nFormatted schedule message:")
    print("=" * 50)
    print(schedule_message)
    print("=" * 50)

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_full_functionality()
