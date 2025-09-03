#!/usr/bin/env python3
"""
Test script to verify the group selection functionality
"""

from database.models import Database
from handlers.group_selection import search_matching_groups
from keyboards.group_selection import get_group_confirmation_keyboard
import json


def test_group_selection():
    """Test group selection functionality"""
    print("Testing group selection functionality...")

    # Initialize database
    db = Database()
    print("✓ Database initialized")

    # Add test groups
    group1_id = db.add_group("М8О-207БВ-24", "Computer Science")
    group2_id = db.add_group("М8О-208БВ-24", "Computer Science")
    group3_id = db.add_group("М8О-209БВ-24", "Computer Science")
    print(f"✓ Added groups with IDs: {group1_id}, {group2_id}, {group3_id}")

    # Test exact match
    print("\nTesting exact match...")
    exact_matches = search_matching_groups("М8О-207БВ-24", db)
    assert len(exact_matches) > 0, "Should find exact match"
    assert exact_matches[0]["name"] == "М8О-207БВ-24", "Should match exact group name"
    print("✓ Exact match found")

    # Test partial match (user input contains group name)
    print("\nTesting partial match (user input contains group name)...")
    partial_matches1 = search_matching_groups("207БВ", db)
    assert len(partial_matches1) > 0, "Should find partial match"
    print("✓ Partial match found")

    # Test partial match (group name contains user input)
    print("\nTesting partial match (group name contains user input)...")
    partial_matches2 = search_matching_groups(
        "М8О207БВ24", db
    )  # without hyphens and spaces
    assert len(partial_matches2) > 0, "Should find partial match"
    print("✓ Partial match found")

    # Test group confirmation keyboard
    print("\nTesting group confirmation keyboard...")
    keyboard = get_group_confirmation_keyboard(group1_id, "М8О-207БВ-24")

    # Verify keyboard structure
    assert keyboard.inline_keyboard is not None, "Keyboard should have inline_keyboard"
    assert len(keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert len(keyboard.inline_keyboard[0]) == 2, "Keyboard should have two buttons"

    # Check button texts
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].text == "Да", "First button should be 'Да'"
    assert buttons[1].text == "Нет", "Second button should be 'Нет'"

    # Check callback data
    assert buttons[0].callback_data.startswith(
        "group_"
    ), "First button should have group callback"
    assert buttons[1].callback_data.startswith(
        "group_"
    ), "Second button should have group callback"

    # Parse callback data to verify structure
    yes_data = json.loads(buttons[0].callback_data[6:])  # Remove "group_" prefix
    no_data = json.loads(buttons[1].callback_data[6:])

    assert (
        yes_data["action"] == "confirm_group"
    ), "Yes button action should be 'confirm_group'"
    assert (
        no_data["action"] == "cancel_group"
    ), "No button action should be 'cancel_group'"
    assert yes_data["group_id"] == group1_id, "Yes button should have correct group ID"
    assert no_data["group_id"] == group1_id, "No button should have correct group ID"
    assert (
        yes_data["group_name"] == "М8О-207БВ-24"
    ), "Yes button should have correct group name"
    assert (
        no_data["group_name"] == "М8О-207БВ-24"
    ), "No button should have correct group name"

    print("✓ Group confirmation keyboard verified")

    print("\n" + "=" * 50)
    print("GROUP SELECTION TEST PASSED!")
    print("All features are working correctly:")
    print(" ✓ Exact group name matching")
    print("  ✓ Partial group name matching")
    print("  ✓ Group confirmation keyboard with 'Да' and 'Нет' buttons")
    print("  ✓ Proper callback data structure")
    print("=" * 50)


if __name__ == "__main__":
    test_group_selection()
