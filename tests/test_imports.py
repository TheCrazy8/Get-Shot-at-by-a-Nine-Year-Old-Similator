"""Test module to verify all required dependencies are available."""
import unittest
import sys


class TestImports(unittest.TestCase):
    """Test that all required packages can be imported."""

    def test_pygame_import(self):
        """Test that pygame can be imported."""
        try:
            import pygame
            self.assertIsNotNone(pygame)
        except ImportError as e:
            self.fail(f"Failed to import pygame: {e}")

    def test_pygame_version(self):
        """Test that pygame version is acceptable."""
        import pygame
        version = pygame.version.ver
        major, minor, _ = map(int, version.split('.'))
        self.assertGreaterEqual(major, 2, "pygame version should be 2.x or higher")
        if major == 2:
            self.assertGreaterEqual(minor, 5, "pygame 2.x version should be 2.5 or higher")

    def test_pyinstaller_import(self):
        """Test that PyInstaller can be imported."""
        try:
            import PyInstaller
            self.assertIsNotNone(PyInstaller)
        except ImportError as e:
            self.fail(f"Failed to import PyInstaller: {e}")

    def test_pyinstaller_main_import(self):
        """Test that PyInstaller.__main__ can be imported."""
        try:
            import PyInstaller.__main__
            self.assertIsNotNone(PyInstaller.__main__)
        except ImportError as e:
            self.fail(f"Failed to import PyInstaller.__main__: {e}")

    def test_tkinter_import(self):
        """Test that tkinter can be imported."""
        try:
            import tkinter as tk
            self.assertIsNotNone(tk)
        except ImportError as e:
            self.skipTest(f"tkinter not available in this environment: {e}")

    def test_standard_library_imports(self):
        """Test that all required standard library modules can be imported."""
        required_modules = [
            'os', 'sys', 'time', 'random', 'math', 'ctypes',
            'collections', 'pathlib', 'ast'
        ]
        for module_name in required_modules:
            with self.subTest(module=module_name):
                try:
                    __import__(module_name)
                except ImportError as e:
                    self.fail(f"Failed to import {module_name}: {e}")

    def test_python_version(self):
        """Test that Python version is compatible."""
        version_info = sys.version_info
        self.assertGreaterEqual(version_info.major, 3, "Python 3 is required")
        if version_info.major == 3:
            self.assertGreaterEqual(version_info.minor, 7, "Python 3.7 or higher is required")


if __name__ == '__main__':
    unittest.main()
