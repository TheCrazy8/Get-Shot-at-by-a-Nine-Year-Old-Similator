"""Test module for core game functionality."""
import unittest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Try to import tkinter, but make tests work even if it's not available
try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class TestGameFunctionality(unittest.TestCase):
    """Test core game mechanics and functions."""

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

    def test_game_file_has_main_class(self):
        """Test that the game file contains the main game class."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('class bullet_hell_game', content,
                         "Game file should contain bullet_hell_game class")

    def test_game_file_has_init_method(self):
        """Test that the game class has an __init__ method."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('def __init__', content,
                         "Game class should have __init__ method")

    def test_game_imports_required_modules(self):
        """Test that the game file imports all required modules."""
        required_imports = [
            'import tkinter',
            'import random',
            'import time',
            'import pygame',
            'import sys',
            'import os',
            'import math'
        ]
        
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for import_stmt in required_imports:
                with self.subTest(import_stmt=import_stmt):
                    self.assertIn(import_stmt, content,
                                f"Game should have: {import_stmt}")

    def test_game_has_asset_resolution_method(self):
        """Test that the game has a method to resolve asset paths."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('_resolve_asset_path', content,
                         "Game should have _resolve_asset_path method")
            self.assertIn('_MEIPASS', content,
                         "Game should check for PyInstaller _MEIPASS")

    def test_game_initializes_pygame(self):
        """Test that the game initializes pygame."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('pygame.init()', content,
                         "Game should initialize pygame")
            self.assertIn('pygame.mixer.init()', content,
                         "Game should initialize pygame mixer")

    def test_game_has_update_game_method(self):
        """Test that the game has an update_game method."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('def update_game', content,
                         "Game should have update_game method")

    def test_game_has_bullet_shooting_methods(self):
        """Test that the game has methods for shooting different bullet types."""
        bullet_methods = [
            'shoot_vertical',
            'shoot_horizontal',
            'shoot_triangle',
            'shoot_quad',
            'shoot_diagonal'
        ]
        
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # At least some bullet shooting methods should exist
            found_methods = sum(1 for method in bullet_methods if f'def {method}' in content)
            self.assertGreater(found_methods, 0,
                             "Game should have bullet shooting methods")

    def test_game_has_collision_detection(self):
        """Test that the game has collision detection logic."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for collision-related code
            collision_indicators = [
                'coords',
                'overlapping',
                'collision'
            ]
            found = any(indicator in content.lower() for indicator in collision_indicators)
            self.assertTrue(found, "Game should have collision detection")

    def test_game_has_score_tracking(self):
        """Test that the game tracks score."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('self.score', content,
                         "Game should track score")

    def test_game_has_main_guard(self):
        """Test that the game file has a __main__ guard."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('if __name__ == "__main__":', content,
                         "Game file should have a main guard")

    def test_game_creates_tkinter_root(self):
        """Test that the game creates a tkinter root window."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('tk.Tk()', content,
                         "Game should create a tkinter root window")

    def test_game_has_pause_functionality(self):
        """Test that the game has pause functionality."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('pause', content.lower(),
                         "Game should have pause functionality")

    def test_game_has_restart_functionality(self):
        """Test that the game has restart functionality."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('restart', content.lower(),
                         "Game should have restart functionality")

    def test_game_has_game_over_handling(self):
        """Test that the game has game over handling."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('game_over', content.lower(),
                         "Game should have game over handling")

    def test_game_uses_canvas(self):
        """Test that the game uses tkinter canvas."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('Canvas', content,
                         "Game should use tkinter Canvas")

    def test_game_loads_music(self):
        """Test that the game loads music files."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            music_files = ['music.mp3', 'game_0v3r.mp3', 'PauseLoop.mp3']
            for music_file in music_files:
                with self.subTest(music_file=music_file):
                    self.assertIn(music_file, content,
                                f"Game should reference {music_file}")

    def test_game_has_settings_system(self):
        """Test that the game has a settings system."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('settings', content.lower(),
                         "Game should have settings system")

    def test_game_has_player_movement(self):
        """Test that the game has player movement handling."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            movement_indicators = ['move', 'velocity', 'speed']
            found = any(indicator in content.lower() for indicator in movement_indicators)
            self.assertTrue(found, "Game should have player movement")

    def test_game_file_syntax_valid(self):
        """Test that the game file has valid Python syntax."""
        try:
            with open(self.game_file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                compile(code, str(self.game_file_path), 'exec')
        except SyntaxError as e:
            self.fail(f"Game file has syntax error: {e}")

    def test_game_has_background_system(self):
        """Test that the game has a background rendering system."""
        with open(self.game_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            background_indicators = ['background', 'init_background', 'update_background']
            found = any(indicator in content.lower() for indicator in background_indicators)
            self.assertTrue(found, "Game should have background system")


if __name__ == '__main__':
    unittest.main()
