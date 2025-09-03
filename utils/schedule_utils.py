from datetime import datetime, timedelta, date
from typing import List, Dict
from database.models import Database
import logging

logger = logging.getLogger(__name__)

# Days of the week in Russian (abbreviated)
DAYS_OF_WEEK = [
    "пн",
    "вт",
    "ср",
    "чт",
    "пт",
    "сб",
    "вс",
]


def get_current_week_start() -> date:
    """
    Get the start date (Monday) of the current week

    Returns:
        date: Monday of the current week
    """
    today = date.today()
    # Calculate days since Monday (0 = Monday, 6 = Sunday)
    days_since_monday = today.weekday()
    # Subtract days to get to Monday
    monday = today - timedelta(days=days_since_monday)
    return monday


def get_week_start_with_offset(offset: int) -> date:
    """
    Get the start date of a week with an offset from the current week

    Args:
        offset (int): Number of weeks to offset from current week

    Returns:
        date: Monday of the target week
    """
    current_week_start = get_current_week_start()
    return current_week_start + timedelta(weeks=offset)


def get_week_schedule(
    group_id: int, db: Database, week_offset: int = 0, group_name: str = "М8О-207БВ-24"
) -> str:
    """
    Get formatted schedule for a specific week

    Args:
        group_id (int): ID of the group
        db (Database): Database instance
        week_offset (int): Week offset from current week (default: 0)
        group_name (str): Name of the group

    Returns:
        str: Formatted schedule message
    """
    try:
        week_start = get_week_start_with_offset(week_offset)
        lessons = db.get_schedule_for_week(group_id, week_start)
        return format_schedule_message(lessons, week_start, week_offset, group_name)
    except Exception as e:
        logger.error(f"Error getting week schedule: {e}")
        return "Ошибка при получении расписания. Пожалуйста, попробуйте позже."


def get_current_week_schedule(
    group_id: int, db: Database, group_name: str = "М8О-207БВ-24"
) -> str:
    """
    Get formatted schedule for the current week

    Args:
        group_id (int): ID of the group
        db (Database): Database instance
        group_name (str): Name of the group

    Returns:
        str: Formatted schedule message
    """
    return get_week_schedule(group_id, db, 0, group_name)


def format_schedule_message(
    lessons: List[Dict],
    week_start: date,
    week_offset: int = 0,
    group_name: str = "М8О-207БВ-24",
) -> str:
    """
    Format lessons into a readable schedule message

    Args:
        lessons (List[Dict]): List of lesson dictionaries
        week_start (date): Start date of the week
        week_offset (int): Week offset from current week
        group_name (str): Name of the group

    Returns:
        str: Formatted schedule message
    """
    # Start with group name as a blockquote
    message = f"<blockquote>{group_name}</blockquote>\n\n"

    # Group lessons by day
    lessons_by_day = {}
    for lesson in lessons:
        day = lesson["day_of_week"]
        if day not in lessons_by_day:
            lessons_by_day[day] = []
        lessons_by_day[day].append(lesson)

    # Format lessons for each day of the week (Monday to Sunday)
    for day_index in range(7):  # 0=Monday, 6=Sunday
        day_name = DAYS_OF_WEEK[day_index]
        day_date = week_start + timedelta(days=day_index)

        # Start blockquote for the day
        message += f"<blockquote>{day_name[:2]} ~ {day_date.strftime('%d.%m')}\n"

        # Check if there are lessons for this day
        if day_index in lessons_by_day and lessons_by_day[day_index]:
            # Format lessons for this day
            for lesson in lessons_by_day[day_index]:
                start_time = lesson["start_time"].strftime("%H:%M")
                end_time = lesson["end_time"].strftime("%H:%M")
                subject = lesson["subject_name"]
                # teacher = lesson["teacher_name"]
                location = lesson["location"] or "--каф."

                message += f"{subject}\n"
                message += f"{start_time}-{end_time}   ПЗ   {location}\n"
        else:
            # No lessons for this day
            message += "Выходной"

        # Close blockquote for the day
        message += "</blockquote>"

    return message
