#!/usr/bin/env python3
"""
Test script to verify the updated formatting v2
"""

from database.models import Database
from utils.schedule_utils import get_current_week_schedule
from datetime import datetime, date


def test_updated_formatting_v2():
    """Test updated formatting v2"""
    print("Testing updated formatting v2...")

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

    # Check for uppercase day names
    assert "Пн" in schedule_message, "Message should contain uppercase Monday (Пн)"
    assert "Вт" in schedule_message, "Message should contain uppercase Tuesday (Вт)"
    assert "Ср" in schedule_message, "Message should contain uppercase Wednesday (Ср)"
    assert "Чт" in schedule_message, "Message should contain uppercase Thursday (Чт)"
    assert "Пт" in schedule_message, "Message should contain uppercase Friday (Пт)"
    assert "Сб" in schedule_message, "Message should contain uppercase Saturday (Сб)"
    assert "Вс" in schedule_message, "Message should contain uppercase Sunday (Вс)"

    # Check for bold day names and dates
    assert "<b>Пн ~" in schedule_message, "Message should contain bold Monday"
    assert "<b>Вт ~" in schedule_message, "Message should contain bold Tuesday"
    assert "<b>Ср ~" in schedule_message, "Message should contain bold Wednesday"
    assert "<b>Чт ~" in schedule_message, "Message should contain bold Thursday"
    assert "<b>Пт ~" in schedule_message, "Message should contain bold Friday"
    assert "<b>Сб ~" in schedule_message, "Message should contain bold Saturday"
    assert "<b>Вс ~" in schedule_message, "Message should contain bold Sunday"

    print("✓ Schedule content verified")

    # Check that "Выходной" has a newline after it
    assert (
        "Выходной\n</blockquote>" in schedule_message
    ), "Message should have newline after 'Выходной'"

    print("✓ Newline after 'Выходной' verified")

    # Print final output
    print("\n" + "=" * 70)
    print("UPDATED FORMATTING V2 OUTPUT")
    print("=" * 70)
    print(schedule_message)
    print("=" * 70)

    # Count blockquotes
    blockquote_count = schedule_message.count("<blockquote>")
    closing_blockquote_count = schedule_message.count("</blockquote>")
    print(
        f"\nBlockquote count: {blockquote_count} opening, {closing_blockquote_count} closing"
    )

    # Count bold tags
    bold_count = schedule_message.count("<b>")
    closing_bold_count = schedule_message.count("</b>")
    print(f"Bold tag count: {bold_count} opening, {closing_bold_count} closing")

    print("\n" + "=" * 70)
    print("UPDATED FORMATTING V2 TEST PASSED!")
    print("All features are working correctly:")
    print("  ✓ Schedule retrieval from database")
    print("  ✓ Schedule formatting with blockquotes")
    print("  ✓ Uppercase day names (Пн, Вт, Ср, Чт, Пт, Сб, Вс)")
    print("  ✓ Bold day names and dates")
    print("  ✓ Newline after 'Выходной' to prevent merging on mobile")
    print("  ✓ Display of test lessons")
    print("  ✓ Proper handling of days without lessons")
    print("=" * 70)


if __name__ == "__main__":
    test_updated_formatting_v2()
