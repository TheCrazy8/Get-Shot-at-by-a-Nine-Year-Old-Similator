#!/usr/bin/env python3
"""
Test runner for Rift of Memories and Regrets.

This script runs all tests in the tests directory and provides a summary of results.
"""
import sys
import unittest
import os
from pathlib import Path


def run_tests(verbosity=2):
    """
    Run all tests in the tests directory.
    
    Args:
        verbosity: Level of test output detail (0=quiet, 1=normal, 2=verbose)
    
    Returns:
        True if all tests passed, False otherwise
    """
    # Get the project root directory
    project_root = Path(__file__).parent
    tests_dir = project_root / 'tests'
    
    # Add project root to path so imports work
    sys.path.insert(0, str(project_root))
    
    print("=" * 70)
    print("Running Test Suite for Rift of Memories and Regrets")
    print("=" * 70)
    print()
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover(str(tests_dir), pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Return True if all tests passed
    return result.wasSuccessful()


def main():
    """Main entry point for the test runner."""
    # Parse command line arguments
    verbosity = 2
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-q', '--quiet']:
            verbosity = 0
        elif sys.argv[1] in ['-v', '--verbose']:
            verbosity = 2
        elif sys.argv[1] in ['-h', '--help']:
            print("Usage: python run_tests.py [OPTIONS]")
            print()
            print("Options:")
            print("  -q, --quiet    Minimal output")
            print("  -v, --verbose  Detailed output (default)")
            print("  -h, --help     Show this help message")
            print()
            print("Examples:")
            print("  python run_tests.py          # Run with verbose output")
            print("  python run_tests.py -q       # Run with minimal output")
            return 0
    
    # Run the tests
    success = run_tests(verbosity)
    
    # Exit with appropriate code
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
