"""Test module for the build executable script."""
import unittest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestBuildExecutable(unittest.TestCase):
    """Test the build executable script functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the test by finding the project root."""
        cls.project_root = Path(__file__).parent.parent
        cls.build_script_path = cls.project_root / "build executable.py"

    def test_build_script_exists(self):
        """Test that the build script file exists."""
        self.assertTrue(
            self.build_script_path.exists(),
            f"Build script not found at {self.build_script_path}"
        )

    def test_build_script_is_readable(self):
        """Test that the build script can be read."""
        try:
            with open(self.build_script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Build script is empty")
        except Exception as e:
            self.fail(f"Failed to read build script: {e}")

    def test_build_script_has_build_function(self):
        """Test that the build script contains a build function."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('def build()', content, "Build script should have a build() function")

    def test_build_script_imports_pyinstaller(self):
        """Test that the build script imports PyInstaller."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('import PyInstaller.__main__', content, 
                         "Build script should import PyInstaller.__main__")

    def test_build_script_has_main_guard(self):
        """Test that the build script has a __main__ guard."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('if __name__ == \'__main__\':', content,
                         "Build script should have a main guard")

    def test_build_script_includes_all_assets(self):
        """Test that the build script includes all required assets."""
        required_assets = [
            "music.mp3",
            "game_0v3r.mp3",
            "game_0v3r_g0n333333333333.mp3",
            "lore.txt",
            "icon3.ico",
            "icon3.png",
            "uneasy type beat.wav",
            "e.mp3",
            "[UN]Canny.mp3",
            "PauseLoop.mp3"
        ]
        
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for asset in required_assets:
                with self.subTest(asset=asset):
                    self.assertIn(asset, content,
                                f"Build script should include {asset} in data files")

    def test_build_script_specifies_onefile(self):
        """Test that the build script specifies --onefile option."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('--onefile', content,
                         "Build script should use --onefile option")

    def test_build_script_specifies_windowed(self):
        """Test that the build script specifies --windowed option."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('--windowed', content,
                         "Build script should use --windowed option")

    def test_build_script_specifies_icon(self):
        """Test that the build script specifies an icon."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('--icon=icon3.ico', content,
                         "Build script should specify icon3.ico as the icon")

    def test_build_script_uses_project_root(self):
        """Test that the build script sets up PROJECT_ROOT."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('PROJECT_ROOT', content,
                         "Build script should define PROJECT_ROOT")
            self.assertIn('Path(__file__)', content,
                         "Build script should use __file__ to determine PROJECT_ROOT")

    def test_build_script_changes_directory(self):
        """Test that the build script changes to the project directory."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('os.chdir', content,
                         "Build script should change to project directory")

    def test_build_script_handles_platform_separator(self):
        """Test that the build script handles platform-specific separators."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('os.name', content,
                         "Build script should check os.name for platform detection")
            # Check for separator handling
            self.assertTrue(
                ';' in content or 'sep' in content,
                "Build script should handle path separators"
            )

    def test_build_script_handles_macos_splash(self):
        """Test that the build script conditionally handles macOS splash screen."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('darwin', content,
                         "Build script should check for darwin (macOS)")
            self.assertIn('--splash', content,
                         "Build script should have splash screen configuration")

    @patch('PyInstaller.__main__.run')
    def test_build_function_can_be_called(self, mock_pyinstaller_run):
        """Test that the build function can be called without errors."""
        # Read and compile the build script
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            build_code = f.read()
        
        # Create a mock environment
        mock_globals = {
            '__file__': str(self.build_script_path),
            '__name__': '__test__',
        }
        
        try:
            # Execute the build script code (but not main)
            exec(build_code.replace("if __name__ == '__main__':", "if False:"), mock_globals)
            # Get the build function
            build_func = mock_globals.get('build')
            self.assertIsNotNone(build_func, "Build function should be defined")
            
            # Change to project root before calling
            original_cwd = os.getcwd()
            try:
                os.chdir(self.project_root)
                # Call the build function
                build_func()
                # Verify PyInstaller.run was called
                self.assertTrue(mock_pyinstaller_run.called,
                              "PyInstaller.run should be called")
                # Verify arguments contain expected options
                args = mock_pyinstaller_run.call_args[0][0]
                self.assertIn('--onefile', args)
                self.assertIn('--windowed', args)
            finally:
                os.chdir(original_cwd)
                
        except Exception as e:
            self.fail(f"Build function raised an exception: {e}")

    def test_build_script_name_output(self):
        """Test that the build script specifies output name."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('--name=', content,
                         "Build script should specify output name with --name")
            self.assertIn('RiftOfMemories', content,
                         "Build script should name output as RiftOfMemories")


if __name__ == '__main__':
    unittest.main()
