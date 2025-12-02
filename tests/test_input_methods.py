"""Test module for input method support."""
import unittest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestInputMethods(unittest.TestCase):
    """Test input method configurations and functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the test by finding the project root."""
        cls.project_root = Path(__file__).parent.parent
        cls.game_file_path = cls.project_root / "Rift of Memories and Regrets.py"

    def test_game_file_exists(self):
        """Test that the main game file exists."""
        self.assertTrue(
            self.game_file_path.exists(),
            f"Game file not found at {self.game_file_path}"
        )

    def test_keybinds_configuration_exists(self):
        """Test that keybinds configuration is present in settings."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("'keybinds'", content,
                         "Keybinds configuration should exist in settings")
            self.assertIn("'move_left'", content,
                         "move_left keybind should be defined")
            self.assertIn("'move_right'", content,
                         "move_right keybind should be defined")
            self.assertIn("'move_up'", content,
                         "move_up keybind should be defined")
            self.assertIn("'move_down'", content,
                         "move_down keybind should be defined")
            self.assertIn("'shoot'", content,
                         "shoot keybind should be defined")
            self.assertIn("'focus'", content,
                         "focus keybind should be defined")

    def test_mouse_support_exists(self):
        """Test that mouse support functionality is present."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("'mouse_enabled'", content,
                         "Mouse enabled setting should exist")
            self.assertIn("def handle_mouse_motion", content,
                         "Mouse motion handler should exist")
            self.assertIn("def handle_mouse_click", content,
                         "Mouse click handler should exist")
            self.assertIn("def update_mouse_movement", content,
                         "Mouse movement update method should exist")

    def test_touchscreen_support_exists(self):
        """Test that touchscreen support functionality is present."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("'touchscreen_enabled'", content,
                         "Touchscreen enabled setting should exist")
            self.assertIn("def handle_touch_start", content,
                         "Touch start handler should exist")
            self.assertIn("def handle_touch_move", content,
                         "Touch move handler should exist")
            self.assertIn("def handle_touch_end", content,
                         "Touch end handler should exist")

    def test_controller_support_exists(self):
        """Test that controller support functionality is present."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("'controller_enabled'", content,
                         "Controller enabled setting should exist")
            self.assertIn("def update_controller_input", content,
                         "Controller input update method should exist")
            self.assertIn("pygame.joystick.init()", content,
                         "Joystick initialization should exist")

    def test_keybinds_menu_exists(self):
        """Test that keybinds menu functionality is present."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("def show_keybinds_menu", content,
                         "Keybinds menu should exist")
            self.assertIn("def toggle_input_method", content,
                         "Input method toggle function should exist")

    def test_default_keybinds_structure(self):
        """Test that default keybinds follow expected structure."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for list-based keybind values
            self.assertIn("'move_left': ['a', 'Left']", content,
                         "move_left should have list of keys")
            self.assertIn("'move_right': ['d', 'Right']", content,
                         "move_right should have list of keys")
            self.assertIn("'move_up': ['w', 'Up']", content,
                         "move_up should have list of keys")
            self.assertIn("'move_down': ['s', 'Down']", content,
                         "move_down should have list of keys")

    def test_input_handlers_check_game_state(self):
        """Test that input handlers check game state before processing."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find mouse handler and check for state checks
            mouse_handler_start = content.find("def handle_mouse_motion")
            mouse_handler_section = content[mouse_handler_start:mouse_handler_start+500]
            self.assertIn("if not self.game_started", mouse_handler_section,
                         "Mouse handler should check game_started")
            self.assertIn("self.paused", mouse_handler_section,
                         "Mouse handler should check paused state")
            
            # Find controller handler and check for state checks
            controller_handler_start = content.find("def update_controller_input")
            controller_handler_section = content[controller_handler_start:controller_handler_start+500]
            self.assertIn("if not self.game_started", controller_handler_section,
                         "Controller handler should check game_started")

    def test_joystick_initialization(self):
        """Test that joysticks are properly initialized."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("self.joysticks = []", content,
                         "Joysticks list should be initialized")
            self.assertIn("pygame.joystick.get_count()", content,
                         "Should check for connected joysticks")
            self.assertIn("joy.init()", content,
                         "Should initialize each joystick")

    def test_mouse_target_tracking(self):
        """Test that mouse target position is tracked."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("self.mouse_target_x", content,
                         "Mouse target X should be tracked")
            self.assertIn("self.mouse_target_y", content,
                         "Mouse target Y should be tracked")
            self.assertIn("self.mouse_move_active", content,
                         "Mouse movement active state should be tracked")

    def test_input_updates_called_in_game_loop(self):
        """Test that input update methods are called in the game loop."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find update_game method
            update_game_start = content.find("def update_game(self):")
            update_game_section = content[update_game_start:update_game_start+3000]
            
            self.assertIn("self.update_mouse_movement()", update_game_section,
                         "Mouse movement update should be called in game loop")
            self.assertIn("self.update_controller_input()", update_game_section,
                         "Controller input update should be called in game loop")

    def test_keybind_usage_in_movement(self):
        """Test that move_player uses configurable keybinds."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find move_player method
            move_player_start = content.find("def move_player(self, event):")
            move_player_section = content[move_player_start:move_player_start+800]
            
            self.assertIn("self.settings['keybinds']['move_left']", move_player_section,
                         "move_player should use keybinds configuration for left movement")
            self.assertIn("self.settings['keybinds']['move_right']", move_player_section,
                         "move_player should use keybinds configuration for right movement")
            self.assertIn("self.settings['keybinds']['move_up']", move_player_section,
                         "move_player should use keybinds configuration for up movement")
            self.assertIn("self.settings['keybinds']['move_down']", move_player_section,
                         "move_player should use keybinds configuration for down movement")

    def test_event_bindings_in_start_game(self):
        """Test that input events are bound when game starts."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find start_game method
            start_game_start = content.find("def start_game(self):")
            start_game_section = content[start_game_start:start_game_start+2000]
            
            self.assertIn("self.canvas.bind('<Motion>'", start_game_section,
                         "Mouse motion event should be bound")
            self.assertIn("self.canvas.bind('<Button-1>'", start_game_section,
                         "Mouse button event should be bound")
            self.assertIn("self.canvas.bind('<ButtonPress-1>'", start_game_section,
                         "Touch start event should be bound")
            self.assertIn("self.canvas.bind('<B1-Motion>'", start_game_section,
                         "Touch move event should be bound")

    def test_controller_deadzone_handling(self):
        """Test that controller has deadzone to avoid drift."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find controller update method
            controller_start = content.find("def update_controller_input")
            controller_section = content[controller_start:controller_start+1500]
            
            self.assertIn("deadzone", controller_section,
                         "Controller should implement deadzone")
            self.assertIn("abs(axis_x)", controller_section,
                         "Controller should check absolute axis values")

    def test_input_method_toggles(self):
        """Test that input methods can be toggled on/off."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            self.assertIn("mouse_enabled", content,
                         "Mouse should be toggleable")
            self.assertIn("controller_enabled", content,
                         "Controller should be toggleable")
            self.assertIn("touchscreen_enabled", content,
                         "Touchscreen should be toggleable")

    def test_smooth_mouse_movement(self):
        """Test that mouse movement is smoothed."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find mouse movement update
            mouse_update_start = content.find("def update_mouse_movement")
            mouse_update_section = content[mouse_update_start:mouse_update_start+800]
            
            self.assertIn("distance", mouse_update_section,
                         "Mouse movement should calculate distance")
            self.assertIn("_hypot", mouse_update_section,
                         "Mouse movement should use distance calculation")


if __name__ == '__main__':
    unittest.main()
