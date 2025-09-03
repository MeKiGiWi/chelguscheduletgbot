#!/usr/bin/env python3
"""
Debug script to examine schedule data in the database
"""

from database.models import Database
import sqlite3


def debug_schedule_data():
    """Debug schedule data in the database"""
    print("Debugging schedule data in the database...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Get the test group
    group_id = db.get_group_id_by_name("М8О-207БВ-24")
    if not group_id:
        print("✗ Test group not found in database")
        return

    print(f"✓ Found test group: М8О-207БВ-24 (ID: {group_id})")

    # Connect to database directly to examine data
    connection = sqlite3.connect(db.db_path)
    cursor = connection.cursor()

    # Check groups table
    print("\nGroups table:")
    cursor.execute("SELECT * FROM groups")
    groups = cursor.fetchall()
    for group in groups:
        print(f"  {group}")

    # Check subjects table
    print("\nSubjects table:")
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    for subject in subjects:
        print(f"  {subject}")

    # Check teachers table
    print("\nTeachers table:")
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    for teacher in teachers:
        print(f"  {teacher}")

    # Check schedules table
    print("\nSchedules table:")
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    for schedule in schedules:
        print(f"  {schedule}")

    # Check lessons table
    print("\nLessons table:")
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    for lesson in lessons:
        print(f"  {lesson}")

    # Check specific schedule for the group
    print(f"\nSchedule for group {group_id}:")
    cursor.execute("SELECT * FROM schedules WHERE group_id = ?", (group_id,))
    group_schedules = cursor.fetchall()
    for schedule in group_schedules:
        print(f"  {schedule}")

        # Check lessons for this schedule
        schedule_id = schedule[0]
        print(f"  Lessons for schedule {schedule_id}:")
        cursor.execute("SELECT * FROM lessons WHERE schedule_id = ?", (schedule_id,))
        schedule_lessons = cursor.fetchall()
        for lesson in schedule_lessons:
            print(f"    {lesson}")

            # Get subject name
            subject_id = lesson[2]
            cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
            subject = cursor.fetchone()
            print(f"      Subject: {subject[0] if subject else 'Not found'}")

            # Get teacher name
            teacher_id = lesson[3]
            cursor.execute("SELECT name FROM teachers WHERE id = ?", (teacher_id,))
            teacher = cursor.fetchone()
            print(f"      Teacher: {teacher[0] if teacher else 'Not found'}")

    connection.close()

    print("\n" + "=" * 50)
    print("DATABASE DEBUG COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    debug_schedule_data()
