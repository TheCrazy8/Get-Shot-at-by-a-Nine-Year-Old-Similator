"""Test module to verify all required game assets exist."""
import unittest
import os
from pathlib import Path


class TestAssets(unittest.TestCase):
    """Test that all required game assets are present."""

    @classmethod
    def setUpClass(cls):
        """Set up the test by finding the project root."""
        # Navigate to project root (parent of tests directory)
        cls.project_root = Path(__file__).parent.parent
        cls.required_audio_files = [
            "music.mp3",
            "game_0v3r.mp3",
            "game_0v3r_g0n333333333333.mp3",
            "PauseLoop.mp3",
            "uneasy type beat.wav",
            "e.mp3",
            "[UN]Canny.mp3"
        ]
        cls.required_image_files = [
            "icon3.ico",
            "icon3.png"
        ]
        cls.required_text_files = [
            "lore.txt"
        ]
        cls.required_code_files = [
            "Rift of Memories and Regrets.py",
            "build executable.py",
            "requirements.txt"
        ]

    def test_audio_files_exist(self):
        """Test that all required audio files exist."""
        for audio_file in self.required_audio_files:
            with self.subTest(file=audio_file):
                file_path = self.project_root / audio_file
                self.assertTrue(
                    file_path.exists(),
                    f"Audio file {audio_file} not found at {file_path}"
                )

    def test_image_files_exist(self):
        """Test that all required image files exist."""
        for image_file in self.required_image_files:
            with self.subTest(file=image_file):
                file_path = self.project_root / image_file
                self.assertTrue(
                    file_path.exists(),
                    f"Image file {image_file} not found at {file_path}"
                )

    def test_text_files_exist(self):
        """Test that all required text files exist."""
        for text_file in self.required_text_files:
            with self.subTest(file=text_file):
                file_path = self.project_root / text_file
                self.assertTrue(
                    file_path.exists(),
                    f"Text file {text_file} not found at {file_path}"
                )

    def test_code_files_exist(self):
        """Test that all required code files exist."""
        for code_file in self.required_code_files:
            with self.subTest(file=code_file):
                file_path = self.project_root / code_file
                self.assertTrue(
                    file_path.exists(),
                    f"Code file {code_file} not found at {file_path}"
                )

    def test_lore_file_readable(self):
        """Test that lore.txt can be read."""
        lore_path = self.project_root / "lore.txt"
        try:
            with open(lore_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertGreater(len(content), 0, "lore.txt is empty")
        except Exception as e:
            self.fail(f"Failed to read lore.txt: {e}")

    def test_requirements_file_readable(self):
        """Test that requirements.txt can be read and contains expected dependencies."""
        req_path = self.project_root / "requirements.txt"
        try:
            with open(req_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                self.assertIn('pygame', content, "requirements.txt should contain pygame")
                self.assertIn('pyinstaller', content, "requirements.txt should contain pyinstaller")
        except Exception as e:
            self.fail(f"Failed to read requirements.txt: {e}")

    def test_main_game_file_readable(self):
        """Test that the main game file can be read."""
        game_path = self.project_root / "Rift of Memories and Regrets.py"
        try:
            with open(game_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Main game file is empty")
                self.assertIn('bullet_hell_game', content, "Main game file should contain game class")
        except Exception as e:
            self.fail(f"Failed to read main game file: {e}")

    def test_icon_files_not_empty(self):
        """Test that icon files are not empty."""
        for icon_file in ["icon3.ico", "icon3.png"]:
            with self.subTest(file=icon_file):
                file_path = self.project_root / icon_file
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    self.assertGreater(file_size, 0, f"{icon_file} is empty")

    def test_audio_files_not_empty(self):
        """Test that audio files are not empty."""
        for audio_file in self.required_audio_files:
            with self.subTest(file=audio_file):
                file_path = self.project_root / audio_file
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    self.assertGreater(file_size, 0, f"{audio_file} is empty")


if __name__ == '__main__':
    unittest.main()
