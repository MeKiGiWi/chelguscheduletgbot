#!/usr/bin/env python3
"""
Test script to verify database functionality
"""

from database.models import Database
from datetime import datetime, date


def test_database():
    """Test database functionality"""
    print("Testing database functionality...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Test adding a group
    group_id = db.add_group("CSU_Group_1", "Computer Science")
    print(f"✓ Added group with ID: {group_id}")

    # Test adding a subject
    subject_id = db.add_subject("Mathematics", "MATH101")
    print(f"✓ Added subject with ID: {subject_id}")

    # Test adding a teacher
    teacher_id = db.add_teacher("Dr. Smith", "Mathematics Department")
    print(f"✓ Added teacher with ID: {teacher_id}")

    # Test adding a schedule
    week_start = date(2025, 9, 1)  # Monday of the week
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule with ID: {schedule_id}")

    # Test adding a lesson
    start_time = datetime(2025, 9, 1, 9, 0)  # September 1, 2025, 9:00 AM
    end_time = datetime(2025, 9, 1, 10, 30)  # September 1, 2025, 10:30 AM
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_id,
        teacher_id=teacher_id,
        start_time=start_time,
        end_time=end_time,
        location="Room 101",
        day_of_week=0,  # Monday
    )
    print(f"✓ Added lesson with ID: {lesson_id}")

    # Test retrieving schedule
    lessons = db.get_schedule_for_week(group_id, week_start)
    print(f"✓ Retrieved {len(lessons)} lessons for the week")

    # Print lesson details
    for lesson in lessons:
        print(
            f"  - {lesson['subject_name']} on {lesson['start_time']} with {lesson['teacher_name']}"
        )

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_database()
