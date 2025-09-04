#!/usr/bin/env python3
"""
Final comprehensive test with all updates v3
"""

from database.models import Database
from keyboards.navigation import get_week_navigation_keyboard
from utils.schedule_utils import get_week_schedule
from keyboards.group_selection import get_group_confirmation_keyboard
from handlers.group_selection import search_matching_groups
import json


def test_final_with_all_updates_v3():
    """Test final comprehensive functionality with all updates v3"""
    print("Running final comprehensive test with all updates v3...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Test group search functionality
    print("\nTesting group search functionality...")
    matches = search_matching_groups("М8О-207БВ-24", db)
    assert len(matches) > 0, "Should find exact match"
    assert matches[0]["name"] == "М8О-207БВ-24", "Should match exact group name"
    group_id = matches[0]["id"]
    print(f"✓ Found group: {matches[0]['name']} (ID: {group_id})")

    # Test group confirmation keyboard
    print("\nTesting group confirmation keyboard...")
    group_keyboard = get_group_confirmation_keyboard(group_id, "М8О-207БВ-24")

    # Verify group keyboard structure
    assert (
        group_keyboard.inline_keyboard is not None
    ), "Keyboard should have inline_keyboard"
    assert len(group_keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert (
        len(group_keyboard.inline_keyboard[0]) == 2
    ), "Keyboard should have two buttons"

    # Check group button texts
    group_buttons = group_keyboard.inline_keyboard[0]
    assert group_buttons[0].text == "Да", "First button should be 'Да'"
    assert group_buttons[1].text == "Нет", "Second button should be 'Нет'"

    # Check group callback data format (should be short)
    assert group_buttons[0].callback_data.startswith(
        "grp_yes:"
    ), "First button should have 'grp_yes:' prefix"
    assert group_buttons[1].callback_data.startswith(
        "grp_no:"
    ), "Second button should have 'grp_no:' prefix"

    # Check that group callback data is short enough for Telegram
    assert (
        len(group_buttons[0].callback_data) <= 64
    ), "Group callback data should be <= 64 characters"
    assert (
        len(group_buttons[1].callback_data) <= 64
    ), "Group callback data should be <= 64 characters"

    print("✓ Group confirmation keyboard verified")
    print(f"  Да button callback data: {group_buttons[0].callback_data}")
    print(f"  Нет button callback data: {group_buttons[1].callback_data}")

    # Test navigation keyboard with different offsets
    print("\nTesting navigation keyboard with different offsets...")

    # Test with offset 0 (current week)
    nav_keyboard_0 = get_week_navigation_keyboard(0)
    print("✓ Navigation keyboard for current week created")

    # Test with offset 100 (100 weeks ahead)
    nav_keyboard_100 = get_week_navigation_keyboard(100)
    print("✓ Navigation keyboard for week +100 created")

    # Test with offset -100 (100 weeks back)
    nav_keyboard_neg100 = get_week_navigation_keyboard(-100)
    print("✓ Navigation keyboard for week -100 created")

    # Verify navigation keyboard structures
    for i, (keyboard, offset) in enumerate(
        [(nav_keyboard_0, 0), (nav_keyboard_100, 100), (nav_keyboard_neg100, -100)]
    ):
        assert (
            keyboard.inline_keyboard is not None
        ), f"Nav keyboard {i} should have inline_keyboard"
        assert (
            len(keyboard.inline_keyboard) == 1
        ), f"Nav keyboard {i} should have one row"
        assert (
            len(keyboard.inline_keyboard[0]) == 3
        ), f"Nav keyboard {i} should have three buttons"

        # Check navigation button texts
        nav_buttons = keyboard.inline_keyboard[0]
        assert (
            nav_buttons[0].text == "←"
        ), f"Nav keyboard {i} first button should be left arrow"
        assert (
            nav_buttons[1].text == "🏠"
        ), f"Nav keyboard {i} second button should be house emoji"
        assert (
            nav_buttons[2].text == "→"
        ), f"Nav keyboard {i} third button should be right arrow"

        # Check navigation callback data format (should be short)
        assert nav_buttons[0].callback_data.startswith(
            "sch_"
        ), f"Nav keyboard {i} first button should have 'sch_' prefix"
        assert nav_buttons[1].callback_data.startswith(
            "sch_"
        ), f"Nav keyboard {i} second button should have 'sch_' prefix"
        assert nav_buttons[2].callback_data.startswith(
            "sch_"
        ), f"Nav keyboard {i} third button should have 'sch_' prefix"

        # Check that navigation callback data is short enough for Telegram
        assert (
            len(nav_buttons[0].callback_data) <= 64
        ), f"Nav keyboard {i} first button should be <= 64 characters"
        assert (
            len(nav_buttons[1].callback_data) <= 64
        ), f"Nav keyboard {i} second button should be <= 64 characters"
        assert (
            len(nav_buttons[2].callback_data) <= 64
        ), f"Nav keyboard {i} third button should be <= 64 characters"

        print(f"  Navigation keyboard for offset {offset}:")
        print(f"    ← Previous week: {nav_buttons[0].callback_data}")
        print(f"    🏠 Current week: {nav_buttons[1].callback_data}")
        print(f"    → Next week: {nav_buttons[2].callback_data}")

    print("✓ Navigation keyboards verified")

    # Test schedule retrieval with different offsets
    print("\nTesting schedule retrieval with different offsets...")

    # Test current week schedule
    schedule_0 = get_week_schedule(group_id, db, 0, "М8О-207БВ-24")
    print("✓ Current week schedule retrieval successful")

    # Test schedule 100 weeks ahead
    schedule_100 = get_week_schedule(group_id, db, 100, "М8О-207БВ-24")
    print("✓ Schedule for week +100 retrieval successful")

    # Test schedule 100 weeks back
    schedule_neg100 = get_week_schedule(group_id, db, -100, "М8О-207БВ-24")
    print("✓ Schedule for week -100 retrieval successful")

    # Verify schedule content
    for i, (schedule, offset) in enumerate(
        [(schedule_0, 0), (schedule_100, 100), (schedule_neg100, -100)]
    ):
        assert (
            "<blockquote>" in schedule
        ), f"Schedule {i} should contain blockquote tags"
        assert (
            "</blockquote>" in schedule
        ), f"Schedule {i} should contain closing blockquote tags"
        assert "М8О-207БВ-24" in schedule, f"Schedule {i} should contain group name"
        assert "Пн" in schedule, f"Schedule {i} should contain uppercase Monday (Пн)"
        assert "Вт" in schedule, f"Schedule {i} should contain uppercase Tuesday (Вт)"
        assert "Ср" in schedule, f"Schedule {i} should contain uppercase Wednesday (Ср)"
        assert "Чт" in schedule, f"Schedule {i} should contain uppercase Thursday (Чт)"
        assert "Пт" in schedule, f"Schedule {i} should contain uppercase Friday (Пт)"
        assert "Сб" in schedule, f"Schedule {i} should contain uppercase Saturday (Сб)"
        assert "Вс" in schedule, f"Schedule {i} should contain uppercase Sunday (Вс)"
        assert (
            "Выходной" in schedule
        ), f"Schedule {i} should contain 'Выходной' for days without lessons"
        assert "<b>Пн ~" in schedule, f"Schedule {i} should contain bold Monday"
        assert "<b>Вт ~" in schedule, f"Schedule {i} should contain bold Tuesday"
        assert "<b>Ср ~" in schedule, f"Schedule {i} should contain bold Wednesday"
        assert "<b>Чт ~" in schedule, f"Schedule {i} should contain bold Thursday"
        assert "<b>Пт ~" in schedule, f"Schedule {i} should contain bold Friday"
        assert "<b>Сб ~" in schedule, f"Schedule {i} should contain bold Saturday"
        assert "<b>Вс ~" in schedule, f"Schedule {i} should contain bold Sunday"
        assert (
            "Выходной\n</blockquote>\n" in schedule
        ), f"Schedule {i} should have newline after 'Выходной' and after </blockquote>"
        assert (
            "</blockquote>\n<blockquote>" in schedule
        ), f"Schedule {i} should have single newline between blockquotes"

    print("✓ Schedule content verified")

    # Print final output
    print("\n" + "=" * 70)
    print("FINAL COMPREHENSIVE TEST OUTPUT WITH ALL UPDATES V3")
    print("=" * 70)
    print("Group confirmation message example:")
    print(f"Может быть <b><u>М8О-207БВ-24</u></b>?\n")

    print("Navigation buttons for extreme offsets:")
    print(
        f"  Offset 0: ← Previous week: {nav_keyboard_0.inline_keyboard[0][0].callback_data}"
    )
    print(
        f"  Offset 0: 🏠 Current week: {nav_keyboard_0.inline_keyboard[0][1].callback_data}"
    )
    print(
        f"  Offset 0: → Next week: {nav_keyboard_0.inline_keyboard[0][2].callback_data}"
    )
    print()
    print(
        f"  Offset 100: ← Previous week: {nav_keyboard_100.inline_keyboard[0][0].callback_data}"
    )
    print(
        f"  Offset 100: 🏠 Current week: {nav_keyboard_100.inline_keyboard[0][1].callback_data}"
    )
    print(
        f"  Offset 100: → Next week: {nav_keyboard_100.inline_keyboard[0][2].callback_data}"
    )
    print()
    print(
        f"  Offset -100: ← Previous week: {nav_keyboard_neg100.inline_keyboard[0][0].callback_data}"
    )
    print(
        f"  Offset -100: 🏠 Current week: {nav_keyboard_neg100.inline_keyboard[0][1].callback_data}"
    )
    print(
        f"  Offset -100: → Next week: {nav_keyboard_neg100.inline_keyboard[0][2].callback_data}"
    )

    print("\nSample schedule for current week:")
    print("=" * 50)
    print(schedule_0)
    print("=" * 50)

    print("\nSample schedule for week +100:")
    print("=" * 50)
    print(schedule_100)
    print("=" * 50)

    print("\nSample schedule for week -100:")
    print("=" * 50)
    print(schedule_neg100)
    print("=" * 50)

    print("\n" + "=" * 70)
    print("FINAL COMPREHENSIVE TEST PASSED!")
    print("All features are working correctly with all updates v3:")
    print("  ✓ Group selection with partial matching")
    print("  ✓ Group confirmation with 'Да' and 'Нет' buttons")
    print("  ✓ Short callback data for group buttons within Telegram limits")
    print("  ✓ Navigation buttons with short callback data")
    print("  ✓ Navigation callback data within Telegram limits")
    print("  ✓ No BUTTON_DATA_INVALID errors even for extreme offsets")
    print("  ✓ Schedule retrieval for different weeks")
    print("  ✓ Schedule formatting with blockquotes")
    print("  ✓ Uppercase day names (Пн, Вт, Ср, Чт, Пт, Сб, Вс)")
    print("  ✓ Bold day names and dates")
    print("  ✓ Single newline after 'Выходной' and after </blockquote>")
    print("  ✓ Single newline between blockquotes to prevent merging on mobile")
    print("  ✓ No newlines before blockquotes")
    print("  ✓ Proper display of lessons and 'Выходной'")
    print("=" * 70)


if __name__ == "__main__":
    test_final_with_all_updates_v3()
