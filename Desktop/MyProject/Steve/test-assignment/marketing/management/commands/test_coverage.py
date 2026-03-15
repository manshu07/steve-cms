"""
Django management command to run tests with coverage.
Usage: py manage.py test_coverage
"""

from django.core.management.base import BaseCommand
from django.test.utils import get_runner
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Run tests with coverage report'

    def handle(self, *args, **options):
        """Run tests with coverage and display results."""
        self.stdout.write(self.style.SUCCESS('Running tests with coverage...'))
        self.stdout.write('')

        try:
            import coverage
        except ImportError:
            self.stdout.write(self.style.ERROR('Coverage package not installed!'))
            self.stdout.write(self.style.WARNING('Install with: pip install coverage'))
            return

        # Initialize coverage
        cov = coverage.Coverage(source=['marketing'], omit=['*/tests/*', '*/migrations/*'])
        cov.start()

        # Run tests
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=1, interactive=False, keepdb=False)

        test_labels = [
            'marketing.tests.test_smoke_working',
            'marketing.tests.test_cms_integration',
            'marketing.tests.test_model_comprehensive',
            'marketing.tests.test_forms',
        ]
        failures = test_runner.run_tests(test_labels)

        # Stop coverage
        cov.stop()
        cov.save()

        # Display report
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('COVERAGE REPORT'))
        self.stdout.write('=' * 70)

        # Console report
        cov.report(show_missing=True)

        # Generate HTML report
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Generating HTML coverage report...'))
        cov.html_report(directory='htmlcov')
        self.stdout.write(self.style.SUCCESS('PASS: HTML report: htmlcov/index.html'))

        # Show total coverage
        total_coverage = cov.report(file=open(sys.__stdout__.fileno(), 'w'))
        self.stdout.write('')
        self.stdout.write(f'Total Coverage: {total_coverage:.2f}%')

        # Coverage assessment
        if total_coverage >= 80:
            self.stdout.write(self.style.SUCCESS('PASS: Excellent! Coverage meets 80% threshold'))
        elif total_coverage >= 60:
            self.stdout.write(self.style.WARNING('WARN: Good progress, aim for 80%'))
        else:
            self.stdout.write(self.style.ERROR('FAIL: Coverage too low. Add more tests!'))

        if failures:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('Some tests FAILED!'))
