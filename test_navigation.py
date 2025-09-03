#!/usr/bin/env python3
"""
Test script to verify navigation keyboard functionality
"""

from keyboards.navigation import get_week_navigation_keyboard


def test_navigation_keyboard():
    """Test navigation keyboard functionality"""
    print("Testing navigation keyboard functionality...")

    # Get the navigation keyboard
    keyboard = get_week_navigation_keyboard()
    print("✓ Navigation keyboard created successfully")

    # Check keyboard structure
    assert keyboard.inline_keyboard is not None, "Keyboard should have inline_keyboard"
    assert len(keyboard.inline_keyboard) == 1, "Keyboard should have one row"
    assert len(keyboard.inline_keyboard[0]) == 3, "Keyboard should have three buttons"

    # Check button texts
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].text == "←", "First button should be left arrow"
    assert buttons[1].text == "🏠", "Second button should be house emoji"
    assert buttons[2].text == "→", "Third button should be right arrow"

    # Check callback data
    assert buttons[0].callback_data.startswith(
        "schedule_"
    ), "First button should have schedule callback"
    assert buttons[1].callback_data.startswith(
        "schedule_"
    ), "Second button should have schedule callback"
    assert buttons[2].callback_data.startswith(
        "schedule_"
    ), "Third button should have schedule callback"

    print("✓ All keyboard properties verified")

    # Print callback data for inspection
    print(f"\nCallback data:")
    print(f"  Previous week: {buttons[0].callback_data}")
    print(f"  Current week: {buttons[1].callback_data}")
    print(f"  Next week: {buttons[2].callback_data}")

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_navigation_keyboard()
