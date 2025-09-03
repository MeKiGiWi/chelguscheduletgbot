# Telegram Bot for University Schedule

A Telegram bot that provides university schedule information with navigation buttons for previous, current, and next week.

## Features

- Display university schedule for a specific group
- Navigate between weeks using inline buttons (previous, current, next)
- Clean and readable schedule formatting
- SQLite database for storing schedule data

## Project Structure

```
tgbot_chelgu/
├── bot.py                 # Main bot application
├── config.py              # Configuration settings
├── database/
│   ├── __init__.py
│   └── models.py          # Database models and connection logic
├── handlers/
│   ├── __init__.py
│   ├── start.py           # Start command handler
│   └── schedule.py        # Schedule navigation handlers
├── keyboards/
│   ├── __init__.py
│   └── navigation.py      # Inline keyboards for navigation
├── utils/
│   ├── __init__.py
│   └── schedule_utils.py  # Schedule formatting utilities
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tgbot_chelgu
   ```

2. Create a virtual environment:
   ```bash
   python -m venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your bot token:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ```

## Usage

1. Run the bot:
   ```bash
   python bot.py
   ```

2. Start a conversation with your bot in Telegram and use the `/start` command to see the current week's schedule.

## Database Schema

The bot uses SQLite for data storage with the following tables:

- `groups`: University groups
- `subjects`: Course subjects
- `teachers`: Teachers information
- `schedules`: Weekly schedules for groups
- `lessons`: Individual lessons with time, subject, and teacher

## Navigation

The bot provides three navigation buttons below the schedule message:

- ← (Previous Week): Shows the schedule for the previous week
- 🏠 (Current Week): Returns to the current week's schedule
- → (Next Week): Shows the schedule for the next week

## Adding Schedule Data

To add schedule data, you can directly interact with the database using the methods provided in `database/models.py`:

```python
from database.models import Database
from datetime import datetime, date

db = Database()

# Add a group
group_id = db.add_group("М8О-207БВ-24", "Computer Science")

# Add a subject
subject_id = db.add_subject("Физическая культура", "PE101")

# Add a teacher
teacher_id = db.add_teacher("Иванов Иван Иванович", "Physical Education")

# Add a schedule for the week
week_start = date(2025, 10, 6)  # Monday of the week
schedule_id = db.add_schedule(group_id, week_start)

# Add a lesson
start_time = datetime(2025, 10, 6, 9, 0)  # October 6, 2025, 9:00 AM
end_time = datetime(2025, 10, 6, 10, 30)  # October 6, 2025, 10:30 AM
lesson_id = db.add_lesson(
    schedule_id=schedule_id,
    subject_id=subject_id,
    teacher_id=teacher_id,
    start_time=start_time,
    end_time=end_time,
    location="--каф. 919",
    day_of_week=0  # Monday
)
```

## Schedule Format

The bot displays schedules in the following format using Telegram blockquotes:

```
<blockquote>М8О-207БВ-24</blockquote>

<blockquote>По ~ 06.10
Физическая культура
09:00-10:30   ПЗ   --каф. 919
</blockquote>
<blockquote>Вт ~ 07.10
Математический анализ
13:00-14:30   ЛК   ГУК В-221

Иностранный язык
14:45-16:15   ПЗ   3-403
</blockquote>
<blockquote>Ср ~ 08.10
Выходной</blockquote>
<blockquote>Че ~ 09.10
Выходной</blockquote>
<blockquote>Пя ~ 10.10
Выходной</blockquote>
<blockquote>Су ~ 11.10
Выходной</blockquote>
<blockquote>Во ~ 12.10
Выходной</blockquote>
```

- Group name is displayed as a separate blockquote at the top
- Each day's content (header, lessons, and "Выходной") is wrapped in a single blockquote
- Lessons are formatted with subject, time, "ПЗ" (practice), and location
- Days with no lessons show "Выходной" (Day off) within the blockquote
- All 7 days of the week are always displayed
- No empty lines between blockquotes

## Group Selection

Users can now select their group by sending the group name to the bot:

1. User sends a message with their group name (e.g., "М8О-207БВ-24")
2. Bot searches for matching groups using partial matching:
   - Exact matches are prioritized
   - Partial matches (user input contains group name)
   - Partial matches (group name contains user input)
   - Matching ignores spaces and hyphens
3. Bot sends a confirmation message with the group name in bold and underlined text
4. User can confirm with "Да" or cancel with "Нет" using inline buttons

## Navigation

The bot supports infinite week navigation:
- ← (Previous Week): Navigate to the previous week
- 🏠 (Current Week): Return to the current week
- → (Next Week): Navigate to the next week

Users can navigate forward or backward through weeks without limitation.

## Technical Notes

- Callback data for inline buttons is optimized to stay within Telegram's 64-byte limit
- Group information is retrieved from the database when needed rather than stored in callback data
- Error handling is implemented for invalid callback data and missing groups

## Populating Test Data

To populate the database with test data for development and testing:

```bash
python reset_and_populate_test_data.py
```

This script will:
1. Delete the existing database file
2. Create a new database with the proper schema
3. Add a test group (М8О-207БВ-24)
4. Add test subjects and teachers
5. Add a schedule for the current week
6. Add sample lessons for different days of the week

After running this script, you can test the bot with the group name "М8О-207БВ-24".

## Schedule Format

The bot displays schedules in the following format using Telegram blockquotes:

```
<blockquote>М8О-207БВ-24</blockquote>

<blockquote>пн ~ 01.09
Физическая культура
09:00-10:30   ПЗ   --каф. 919
</blockquote><blockquote>вт ~ 02.09
Математический анализ
10:45-12:15   ПЗ   ГУК В-221
Иностранный язык
13:00-14:30   ПЗ   3-403
</blockquote><blockquote>ср ~ 03.09
Общая физика
13:00-14:30   ПЗ   ГУК Б-638
</blockquote><blockquote>чт ~ 04.09
Программирование
09:00-10:30   ПЗ   ГУК В-221
</blockquote><blockquote>пт ~ 05.09
Выходной</blockquote><blockquote>сб ~ 06.09
Выходной</blockquote><blockquote>вс ~ 07.09
Выходной</blockquote>
```

- Group name is displayed as a separate blockquote at the top
- Each day's content (header, lessons, and "Выходной") is wrapped in a single blockquote
- Day names are abbreviated (пн, вт, ср, чт, пт, сб, вс)
- Lessons are formatted with subject, time, "ПЗ" (practice), and location
- Days with no lessons show "Выходной" (Day off) within the blockquote
- All 7 days of the week are always displayed
- No empty lines between blockquotes
</content>
<line_count>161</line_count>
</write_to_file


## Technologies Used

- Python 3.8+
- aiogram 3.x (Telegram Bot API framework)
- SQLite (Database)
- python-dotenv (Environment variable management)

## License

This project is licensed under the MIT License.