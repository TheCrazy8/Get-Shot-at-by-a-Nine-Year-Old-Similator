"""Integration tests for the build process."""
import unittest
import os
import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestBuildIntegration(unittest.TestCase):
    """Integration tests that verify the build process works end-to-end."""

    @classmethod
    def setUpClass(cls):
        """Set up the test by finding the project root."""
        cls.project_root = Path(__file__).parent.parent
        cls.build_script_path = cls.project_root / "build executable.py"

    def test_build_script_runs_without_errors(self):
        """Test that the build script can be executed without syntax or import errors."""
        # We won't actually build (takes too long), but we'll verify the script loads
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            build_code = f.read()
        
        # Create a mock environment
        mock_globals = {
            '__file__': str(self.build_script_path),
            '__name__': '__test__',
        }
        
        try:
            # Execute the build script code (but don't run main)
            exec(build_code.replace("if __name__ == '__main__':", "if False:"), mock_globals)
            build_func = mock_globals.get('build')
            self.assertIsNotNone(build_func, "Build function should be defined")
        except Exception as e:
            self.fail(f"Build script execution failed: {e}")

    def test_all_data_files_referenced_exist(self):
        """Test that all files referenced in --add-data actually exist."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # List of expected asset files that should be included
        expected_assets = [
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
        
        # Verify each expected asset is mentioned in the build script
        # and that it exists
        for asset in expected_assets:
            with self.subTest(file=asset):
                self.assertIn(asset, content,
                            f"Asset {asset} should be referenced in build script")
                file_path = self.project_root / asset
                self.assertTrue(
                    file_path.exists(),
                    f"Referenced file {asset} does not exist"
                )

    def test_pyinstaller_arguments_are_valid(self):
        """Test that PyInstaller arguments used are valid."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Valid PyInstaller arguments that should be present
        valid_args = [
            '--onefile',
            '--windowed',
            '--icon',
            '--name',
            '--add-data',
            '--splash'
        ]
        
        found_args = []
        for arg in valid_args:
            if arg in content:
                found_args.append(arg)
        
        # At least the critical args should be present
        critical_args = ['--onefile', '--windowed', '--icon', '--name']
        for arg in critical_args:
            self.assertIn(arg, found_args,
                         f"Critical PyInstaller argument {arg} not found")

    def test_build_script_handles_current_platform(self):
        """Test that the build script correctly handles the current platform."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Build script should check platform for separator
        self.assertIn('os.name', content,
                     "Build script should check os.name for platform")
        
        # Should handle different separators
        if sys.platform == 'win32':
            self.assertIn("';'", content,
                         "Build script should handle Windows separator")
        else:
            self.assertIn("':'", content,
                         "Build script should handle Unix separator")

    def test_main_python_file_is_specified(self):
        """Test that the build script specifies the main Python file."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        main_file = "Rift of Memories and Regrets.py"
        self.assertIn(main_file, content,
                     f"Build script should reference main file: {main_file}")
        
        # Verify the main file exists
        main_file_path = self.project_root / main_file
        self.assertTrue(main_file_path.exists(),
                       f"Main file {main_file} does not exist")

    @patch('PyInstaller.__main__.run')
    def test_build_creates_expected_artifacts(self, mock_pyinstaller_run):
        """Test that running build would create expected artifacts (mocked)."""
        # Import and execute the build function
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            build_code = f.read()
        
        mock_globals = {
            '__file__': str(self.build_script_path),
            '__name__': '__test__',
        }
        
        original_cwd = os.getcwd()
        try:
            os.chdir(self.project_root)
            exec(build_code.replace("if __name__ == '__main__':", "if False:"), mock_globals)
            build_func = mock_globals.get('build')
            
            # Call the build function (PyInstaller.run is mocked)
            build_func()
            
            # Verify PyInstaller was called with correct arguments
            self.assertTrue(mock_pyinstaller_run.called,
                          "PyInstaller.run should be called")
            
            # Get the arguments passed to PyInstaller
            call_args = mock_pyinstaller_run.call_args[0][0]
            
            # Verify expected output name
            name_args = [arg for arg in call_args if arg.startswith('--name=')]
            self.assertEqual(len(name_args), 1, "Should have exactly one --name argument")
            self.assertIn('RiftOfMemories', name_args[0],
                         "Output name should be RiftOfMemories")
            
        finally:
            os.chdir(original_cwd)

    def test_project_root_resolution(self):
        """Test that PROJECT_ROOT is correctly resolved."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should use Path and __file__
        self.assertIn('Path(__file__)', content,
                     "Build script should use Path(__file__) to find project root")
        self.assertIn('.resolve()', content,
                     "Build script should resolve the path")
        self.assertIn('.parent', content,
                     "Build script should get parent directory")

    def test_build_prints_useful_info(self):
        """Test that the build script prints useful information."""
        with open(self.build_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should print where it's building from
        self.assertIn('print', content,
                     "Build script should print information")
        self.assertIn('Building from', content,
                     "Build script should indicate where it's building from")


if __name__ == '__main__':
    unittest.main()
