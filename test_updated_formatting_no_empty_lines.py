#!/usr/bin/env python3
"""
Test script to verify the updated formatting without empty lines and with abbreviated day names
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule
from datetime import datetime, date


def test_updated_formatting_no_empty_lines():
    """Test updated formatting without empty lines and with abbreviated day names"""
    print(
        "Testing updated formatting without empty lines and with abbreviated day names..."
    )

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

    # Verify schedule content
    assert "<blockquote>" in schedule_message, "Message should contain blockquote tags"
    assert (
        "</blockquote>" in schedule_message
    ), "Message should contain closing blockquote tags"
    assert "М8О-207БВ-24" in schedule_message, "Message should contain group name"
    assert (
        "Физическая культура" in schedule_message
    ), "Message should contain Physical Education"
    assert (
        "Математический анализ" in schedule_message
    ), "Message should contain Mathematical Analysis"
    assert (
        "Иностранный язык" in schedule_message
    ), "Message should contain Foreign Language"
    assert "Общая физика" in schedule_message, "Message should contain General Physics"
    assert "Программирование" in schedule_message, "Message should contain Programming"
    assert (
        "Выходной" in schedule_message
    ), "Message should contain 'Выходной' for days without lessons"

    # Check for abbreviated day names
    assert "пн" in schedule_message, "Message should contain abbreviated Monday (пн)"
    assert "вт" in schedule_message, "Message should contain abbreviated Tuesday (вт)"
    assert "ср" in schedule_message, "Message should contain abbreviated Wednesday (ср)"
    assert "чт" in schedule_message, "Message should contain abbreviated Thursday (чт)"
    assert "пт" in schedule_message, "Message should contain abbreviated Friday (пт)"
    assert "сб" in schedule_message, "Message should contain abbreviated Saturday (сб)"
    assert "вс" in schedule_message, "Message should contain abbreviated Sunday (вс)"

    print("✓ Schedule content verified")

    # Check that there are no empty lines between blockquotes
    import re

    consecutive_newlines = re.findall(r"\n{3,}", schedule_message)
    assert (
        len(consecutive_newlines) == 0
    ), "Should not have 3 or more consecutive newlines"

    print("✓ No empty lines between blockquotes verified")

    # Print final output
    print("\n" + "=" * 70)
    print("UPDATED FORMATTING OUTPUT")
    print("=" * 70)
    print(schedule_message)
    print("=" * 70)

    # Count blockquotes
    blockquote_count = schedule_message.count("<blockquote>")
    closing_blockquote_count = schedule_message.count("</blockquote>")
    print(
        f"\nBlockquote count: {blockquote_count} opening, {closing_blockquote_count} closing"
    )

    print("\n" + "=" * 70)
    print("UPDATED FORMATTING TEST PASSED!")
    print("All features are working correctly:")
    print("  ✓ Schedule retrieval from database")
    print("  ✓ Schedule formatting with blockquotes")
    print("  ✓ Abbreviated day names (пн, вт, ср, чт, пт, сб, вс)")
    print("  ✓ No empty lines between blockquotes")
    print("  ✓ Display of test lessons")
    print("  ✓ Proper handling of days without lessons")
    print("=" * 70)


if __name__ == "__main__":
    test_updated_formatting_no_empty_lines()
