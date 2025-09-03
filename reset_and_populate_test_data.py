#!/usr/bin/env python3
"""
Script to reset and populate the database with clean test schedule data
"""

from database.models import Database
from datetime import datetime, date, timedelta
import sqlite3
import os


def reset_and_populate_test_data():
    """Reset and populate the database with clean test schedule data"""
    print("Resetting and populating database with clean test schedule data...")

    # Delete existing database file
    db_file = "schedule.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print("✓ Deleted existing database file")

    # Initialize database (this will create a new database)
    db = Database()
    print("✓ Database initialized")

    # Add test group
    group_id = db.add_group("М8О-207БВ-24", "Computer Science")
    print(f"✓ Added group: М8О-207БВ-24 (ID: {group_id})")

    # Add test subjects
    subjects = [
        ("Физическая культура", "PE101"),
        ("Математический анализ", "MA101"),
        ("Иностранный язык", "FL101"),
        ("Общая физика", "GP101"),
        ("Программирование", "PR101"),
    ]

    subject_ids = []
    for subject_name, subject_code in subjects:
        subject_id = db.add_subject(subject_name, subject_code)
        subject_ids.append(subject_id)
        print(f"✓ Added subject: {subject_name} (ID: {subject_id})")

    # Add test teachers
    teachers = [
        ("Иванов Иван Иванович", "Physical Education"),
        ("Петров Петр Петрович", "Mathematics"),
        ("Сидоров Сидор Сидорович", "Foreign Languages"),
        ("Кузнецов Алексей Владимирович", "Physics"),
        ("Смирнов Владимир Владимирович", "Programming"),
    ]

    teacher_ids = []
    for teacher_name, department in teachers:
        teacher_id = db.add_teacher(teacher_name, department)
        teacher_ids.append(teacher_id)
        print(f"✓ Added teacher: {teacher_name} (ID: {teacher_id})")

    # Add schedule for current week
    from utils.schedule_utils import get_current_week_start

    week_start = get_current_week_start()
    schedule_id = db.add_schedule(group_id, week_start)
    print(f"✓ Added schedule for week starting {week_start} (ID: {schedule_id})")

    # Add test lessons for the week
    # Monday - Physical Education
    start_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=9, minute=0)
    )
    end_time = datetime.combine(
        week_start, datetime.min.time().replace(hour=10, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_ids[0],  # Физическая культура
        teacher_id=teacher_ids[0],  # Иванов Иван Иванович
        start_time=start_time,
        end_time=end_time,
        location="--каф. 919",
        day_of_week=0,  # Monday
    )
    print(f"✓ Added Monday lesson: Physical Education (ID: {lesson_id})")

    # Tuesday - Mathematical Analysis and Foreign Language
    tuesday = week_start + timedelta(days=1)

    # Mathematical Analysis
    start_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=10, minute=45)
    )
    end_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=12, minute=15)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_ids[1],  # Математический анализ
        teacher_id=teacher_ids[1],  # Петров Петрович
        start_time=start_time,
        end_time=end_time,
        location="ГУК В-221",
        day_of_week=1,  # Tuesday
    )
    print(f"✓ Added Tuesday lesson 1: Mathematical Analysis (ID: {lesson_id})")

    # Foreign Language
    start_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=13, minute=0)
    )
    end_time = datetime.combine(
        tuesday, datetime.min.time().replace(hour=14, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_ids[2],  # Иностранный язык
        teacher_id=teacher_ids[2],  # Сидоров Сидор Сидорович
        start_time=start_time,
        end_time=end_time,
        location="3-403",
        day_of_week=1,  # Tuesday
    )
    print(f"✓ Added Tuesday lesson 2: Foreign Language (ID: {lesson_id})")

    # Wednesday - General Physics
    wednesday = week_start + timedelta(days=2)
    start_time = datetime.combine(
        wednesday, datetime.min.time().replace(hour=13, minute=0)
    )
    end_time = datetime.combine(
        wednesday, datetime.min.time().replace(hour=14, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_ids[3],  # Общая физика
        teacher_id=teacher_ids[3],  # Кузнецов Алексей Владимирович
        start_time=start_time,
        end_time=end_time,
        location="ГУК Б-638",
        day_of_week=2,  # Wednesday
    )
    print(f"✓ Added Wednesday lesson: General Physics (ID: {lesson_id})")

    # Thursday - Programming
    thursday = week_start + timedelta(days=3)
    start_time = datetime.combine(
        thursday, datetime.min.time().replace(hour=9, minute=0)
    )
    end_time = datetime.combine(
        thursday, datetime.min.time().replace(hour=10, minute=30)
    )
    lesson_id = db.add_lesson(
        schedule_id=schedule_id,
        subject_id=subject_ids[4],  # Программирование
        teacher_id=teacher_ids[4],  # Смирнов Владимир Владимирович
        start_time=start_time,
        end_time=end_time,
        location="ГУК В-221",
        day_of_week=3,  # Thursday
    )
    print(f"✓ Added Thursday lesson: Programming (ID: {lesson_id})")

    # Verify the data was added correctly
    print("\nVerifying data...")
    connection = sqlite3.connect(db.db_path)
    cursor = connection.cursor()

    # Check groups
    cursor.execute("SELECT * FROM groups WHERE name = ?", ("М8О-207БВ-24",))
    groups = cursor.fetchall()
    print(f"✓ Found {len(groups)} group(s) with name М8О-207БВ-24")

    # Check schedule
    if groups:
        group_id = groups[0][0]
        cursor.execute("SELECT * FROM schedules WHERE group_id = ?", (group_id,))
        schedules = cursor.fetchall()
        print(f"✓ Found {len(schedules)} schedule(s) for group {group_id}")

        if schedules:
            schedule_id = schedules[0][0]
            cursor.execute(
                "SELECT * FROM lessons WHERE schedule_id = ?", (schedule_id,)
            )
            lessons = cursor.fetchall()
            print(f"✓ Found {len(lessons)} lesson(s) for schedule {schedule_id}")

    connection.close()

    print("\n" + "=" * 60)
    print("DATABASE RESET AND POPULATED WITH CLEAN TEST DATA!")
    print("Added:")
    print(" ✓ 1 group: М8О-207БВ-24")
    print("  ✓ 5 subjects")
    print(" ✓ 5 teachers")
    print("  ✓ 1 schedule for current week")
    print("  ✓ 5 lessons for different days")
    print("=" * 60)


if __name__ == "__main__":
    reset_and_populate_test_data()
