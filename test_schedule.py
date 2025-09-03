#!/usr/bin/env python3
"""
Test script to verify schedule formatting functionality
"""

from utils.schedule_utils import format_schedule_message
from datetime import datetime


def test_schedule_formatting():
    """Test schedule formatting functionality"""
    print("Testing schedule formatting functionality...")

    # Sample lessons data
    lessons = [
        {
            "id": 1,
            "subject_name": "Mathematics",
            "teacher_name": "Dr. Smith",
            "start_time": datetime(2025, 9, 1, 9, 0),
            "end_time": datetime(2025, 9, 1, 10, 30),
            "location": "Room 101",
            "day_of_week": 0,  # Monday
        },
        {
            "id": 2,
            "subject_name": "Physics",
            "teacher_name": "Prof. Johnson",
            "start_time": datetime(2025, 9, 1, 1, 0),
            "end_time": datetime(2025, 9, 1, 12, 30),
            "location": "Room 205",
            "day_of_week": 0,  # Monday
        },
        {
            "id": 3,
            "subject_name": "Chemistry",
            "teacher_name": "Dr. Williams",
            "start_time": datetime(2025, 9, 3, 13, 0),
            "end_time": datetime(2025, 9, 3, 14, 30),
            "location": "Lab 301",
            "day_of_week": 2,  # Wednesday
        },
    ]

    # Test formatting for current week
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()

    formatted_message = format_schedule_message(lessons, week_start, 0, "М8О-207БВ-24")
    print("✓ Schedule formatting successful")
    print("\nFormatted message:")
    print(formatted_message)

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_schedule_formatting()
