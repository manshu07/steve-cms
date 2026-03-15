"""
Django management command to run integration tests.
Usage: py manage.py test_integration
"""

from django.core.management.base import BaseCommand
from django.test.utils import get_runner
from django.conf import settings


class Command(BaseCommand):
    help = 'Run integration tests for workflows'

    def handle(self, *args, **options):
        """Run integration tests and display results."""
        self.stdout.write(self.style.SUCCESS('Running integration tests...'))
        self.stdout.write('')

        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)

        # Run integration tests
        test_labels = ['marketing.tests.test_cms_integration']
        failures = test_runner.run_tests(test_labels)

        if failures:
            self.stdout.write(self.style.ERROR('Integration tests FAILED!'))
            self.stdout.write(self.style.WARNING('Fix workflow issues before committing.'))
        else:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('PASS: All integration tests passed!'))
            self.stdout.write(self.style.SUCCESS('CMS workflows verified.'))
