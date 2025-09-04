#!/usr/bin/env python3
"""
Simple test to verify quoteblock formatting
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule


def test_quoteblock_formatting():
    """Test quoteblock formatting"""
    print("Testing quoteblock formatting...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Get the test group
    group_id = db.get_group_id_by_name("М8О-207БВ-24")
    if not group_id:
        print("✗ Test group not found in database")
        return

    print(f"✓ Found test group: М8О-207БВ-24 (ID: {group_id})")

    # Test schedule retrieval
    print("\nTesting schedule retrieval...")
    schedule_message = get_current_week_schedule(group_id, db, "М8О-207БВ-24")
    print("✓ Schedule retrieval successful")

    # Check for empty lines between blockquotes
    import re

    # Look for patterns that might indicate empty lines between blockquotes
    empty_line_patterns = [
        r"</blockquote>\n\s*\n<blockquote>",
        r"</blockquote>\n\n+<blockquote>",
        r"</blockquote>\n{3,}<blockquote>",
    ]

    issues_found = []
    for pattern in empty_line_patterns:
        matches = re.findall(pattern, schedule_message)
        if matches:
            issues_found.append(f"Found pattern '{pattern}' {len(matches)} time(s)")

    if issues_found:
        print("Issues found:")
        for issue in issues_found:
            print(f" ✗ {issue}")
        print("\nSchedule output:")
        print("=" * 50)
        print(schedule_message)
        print("=" * 50)
    else:
        print("✓ No empty lines found between blockquotes")
        print("\nSchedule output:")
        print("=" * 50)
        print(schedule_message)
        print("=" * 50)


if __name__ == "__main__":
    test_quoteblock_formatting()
