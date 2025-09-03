import sqlite3
from datetime import datetime, date
from typing import Optional, List


class Database:
    def __init__(self, db_path: str = "schedule.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create groups table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                faculty TEXT NOT NULL
            )
        """
        )

        # Create subjects table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE
            )
        """
        )

        # Create teachers table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT
            )
        """
        )

        # Create schedules table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                week_start DATE NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups (id)
            )
        """
        )

        # Create lessons table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                location TEXT,
                day_of_week INTEGER NOT NULL, -- 0=Monday, 6=Sunday
                FOREIGN KEY (schedule_id) REFERENCES schedules (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        """
        )

        conn.commit()
        conn.close()

    def add_group(self, name: str, faculty: str) -> int:
        """Add a new group to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO groups (name, faculty) VALUES (?, ?)", (name, faculty)
        )
        group_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return group_id

    def add_subject(self, name: str, code: str) -> int:
        """Add a new subject to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO subjects (name, code) VALUES (?, ?)", (name, code)
        )
        conn.commit()

        # Get the subject id
        cursor.execute("SELECT id FROM subjects WHERE code = ?", (code,))
        subject_id = cursor.fetchone()[0]
        conn.close()
        return subject_id

    def add_teacher(self, name: str, department: str) -> int:
        """Add a new teacher to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teachers (name, department) VALUES (?, ?)", (name, department)
        )
        teacher_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return teacher_id

    def add_schedule(self, group_id: int, week_start: date) -> int:
        """Add a new schedule for a group"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO schedules (group_id, week_start) VALUES (?, ?)",
            (group_id, week_start),
        )
        schedule_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return schedule_id

    def add_lesson(
        self,
        schedule_id: int,
        subject_id: int,
        teacher_id: int,
        start_time: datetime,
        end_time: datetime,
        location: str,
        day_of_week: int,
    ) -> int:
        """Add a new lesson to a schedule"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO lessons (schedule_id, subject_id, teacher_id, start_time, end_time, location, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                schedule_id,
                subject_id,
                teacher_id,
                start_time,
                end_time,
                location,
                day_of_week,
            ),
        )
        lesson_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return lesson_id

    def get_schedule_for_week(self, group_id: int, week_start: date) -> List[dict]:
        """Get schedule for a specific group and week"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT l.id, s.name as subject_name, t.name as teacher_name, 
                   l.start_time, l.end_time, l.location, l.day_of_week
            FROM lessons l
            JOIN subjects s ON l.subject_id = s.id
            JOIN teachers t ON l.teacher_id = t.id
            JOIN schedules sch ON l.schedule_id = sch.id
            WHERE sch.group_id = ? AND sch.week_start = ?
            ORDER BY l.day_of_week, l.start_time
        """,
            (group_id, week_start),
        )

        lessons = cursor.fetchall()
        conn.close()

        # Convert to list of dictionaries
        result = []
        for lesson in lessons:
            result.append(
                {
                    "id": lesson[0],
                    "subject_name": lesson[1],
                    "teacher_name": lesson[2],
                    "start_time": datetime.fromisoformat(lesson[3]),
                    "end_time": datetime.fromisoformat(lesson[4]),
                    "location": lesson[5],
                    "day_of_week": lesson[6],
                }
            )

        return result

    def get_group_id_by_name(self, name: str) -> Optional[int]:
        """Get group ID by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM groups WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_or_create_group(self, name: str, faculty: str) -> int:
        """Get existing group or create a new one"""
        group_id = self.get_group_id_by_name(name)
        if group_id is None:
            group_id = self.add_group(name, faculty)
        return group_id
