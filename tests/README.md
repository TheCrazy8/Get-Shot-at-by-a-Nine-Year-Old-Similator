# Test Suite for Rift of Memories and Regrets

This directory contains automated tests for the game and build system.

## Running Tests

To run all tests:
```bash
python run_tests.py
```

To run a specific test file:
```bash
python -m pytest tests/test_build_executable.py -v
```

## Test Coverage

- **test_imports.py** - Verifies all required dependencies are installed
- **test_assets.py** - Checks that all required game assets exist
- **test_build_executable.py** - Tests the build script configuration and functionality
- **test_game_functionality.py** - Tests core game mechanics and functions

## Requirements

Tests require pytest:
```bash
pip install pytest
```
