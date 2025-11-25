# Test Suite for Rift of Memories and Regrets

This directory contains automated tests for the game and build system.

## Running Tests

To run all tests:
```bash
python run_tests.py
```

To run a specific test file:
```bash
python -m unittest tests.test_build_executable -v
```

To run tests with minimal output:
```bash
python run_tests.py -q
```

## Test Coverage

- **test_imports.py** - Verifies all required dependencies are installed (7 tests)
- **test_assets.py** - Checks that all required game assets exist (9 tests)
- **test_build_executable.py** - Tests the build script configuration and functionality (24 tests)
- **test_build_integration.py** - End-to-end build process verification (8 tests)
- **test_game_functionality.py** - Tests core game mechanics and functions (20 tests)

## Requirements

Tests use Python's built-in `unittest` framework - no additional dependencies required beyond what's already in `requirements.txt`.
