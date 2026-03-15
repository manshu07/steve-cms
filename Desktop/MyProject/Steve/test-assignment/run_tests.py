#!/usr/bin/env python
"""
Comprehensive test runner for marketing app.
Runs all test suites and generates detailed reports.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py smoke        # Run only smoke tests
    python run_tests.py coverage     # Run tests with coverage report
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests(test_labels=None, verbosity=2, coverage=False):
    """
    Run Django tests with detailed output.

    Args:
        test_labels: List of test modules to run (None = all)
        verbosity: Output verbosity level (0-2)
        coverage: Whether to generate coverage report
    """
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
    django.setup()

    # Import coverage if requested
    if coverage:
        try:
            import coverage
            cov = coverage.Coverage(source=['marketing'])
            cov.start()
        except ImportError:
            print("Coverage package not installed. Run: pip install coverage")
            coverage = False

    # Get test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=False, keepdb=False)

    # Default to marketing tests if no labels provided
    if test_labels is None:
        test_labels = ['marketing.tests']

    # Use test settings for better compatibility
    os.environ['DJANGO_SETTINGS_MODULE'] = 'beyondcode_cms.test_settings'

    # Enable coverage if requested
    if coverage:
        try:
            import coverage
            cov = coverage.Coverage(source=['marketing'], omit=['*/tests/*', '*/migrations/*'])
            cov.start()
        except ImportError:
            print("⚠️  Coverage package not installed. Install with: pip install coverage")
            coverage = False

    print("\n" + "="*70)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("="*70 + "\n")

    # Run tests
    failures = test_runner.run_tests(test_labels)

    # Generate coverage report if requested
    if coverage:
        cov.stop()
        cov.save()

        print("\n" + "="*70)
        print("COVERAGE REPORT")
        print("="*70 + "\n")

        # Console report
        cov.report(show_missing=True)

        # Generate HTML report
        print("\n📊 Generating HTML coverage report...")
        cov.html_report(directory='htmlcov')
        print("✅ HTML report generated in htmlcov/index.html")

        # Show coverage percentage
        total_coverage = cov.report(file=open(os.devnull, 'w'))
        print(f"\n📈 Total Coverage: {total_coverage:.2f}%")

        if total_coverage < 80:
            print(f"⚠️  Coverage is below 80%. Add more tests!")
        else:
            print(f"✅ Coverage meets 80% threshold!")

        print("\n📂 Open htmlcov/index.html in your browser for detailed report")

    # Generate coverage report
    if coverage:
        cov.stop()
        cov.save()
        print("\n" + "="*70)
        print("COVERAGE REPORT")
        print("="*70 + "\n")
        cov.report()
        print("\nHTML coverage report generated in htmlcov/")

    # Exit with proper code
    if coverage:
        cov.html_report()

    sys.exit(bool(failures))


def print_usage():
    """Print usage information."""
    print(__doc__)
    print("\nAvailable test suites:")
    print("  smoke        - Quick smoke tests (fail fast on critical issues)")
    print("  models       - Model field and logic tests")
    print("  cms_views    - CMS CRUD and template tests")
    print("  public_views - Public-facing view tests")
    print("\nExamples:")
    print("  python run_tests.py")
    print("  python run_tests.py marketing.tests.test_smoke")
    print("  python run_tests.py coverage")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run comprehensive test suite')
    parser.add_argument('suite', nargs='?', default='all',
                       help='Test suite to run (smoke, models, cms_views, public_views, or all)')
    parser.add_argument('--coverage', action='store_true',
                       help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Map suite names to test labels
    suite_map = {
        'all': ['marketing.tests'],
        'smoke': ['marketing.tests.test_smoke_working'],
        'models': ['marketing.tests.test_models'],
        'cms_views': ['marketing.tests.test_cms_views'],
        'public_views': ['marketing.tests.test_public_views'],
    }

    if args.suite == 'help':
        print_usage()
        sys.exit(0)

    test_labels = suite_map.get(args.suite)
    if test_labels is None:
        print(f"Unknown test suite: {args.suite}")
        print_usage()
        sys.exit(1)

    verbosity = 2 if args.verbose else 1

    run_tests(test_labels=test_labels, verbosity=verbosity, coverage=args.coverage)
