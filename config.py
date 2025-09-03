import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///schedule.db")

# Default group for schedule
DEFAULT_GROUP = os.getenv("DEFAULT_GROUP", "М8О-207БВ-24")
