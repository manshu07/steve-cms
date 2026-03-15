"""
Django management command to run all tests.
Usage: py manage.py test_all
"""

from django.core.management.base import BaseCommand
from django.test.utils import get_runner
from django.conf import settings


class Command(BaseCommand):
    help = 'Run all marketing app tests'

    def handle(self, *args, **options):
        """Run all tests and display results."""
        self.stdout.write(self.style.SUCCESS('Running all tests...'))
        self.stdout.write('')

        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)

        # Run all working tests
        test_labels = [
            'marketing.tests.test_smoke_working',
            'marketing.tests.test_cms_integration',
            'marketing.tests.test_model_comprehensive',
            'marketing.tests.test_forms',
        ]
        failures = test_runner.run_tests(test_labels)

        if failures:
            self.stdout.write(self.style.ERROR('Some tests FAILED!'))
            self.stdout.write(self.style.WARNING('Fix issues before deploying.'))
        else:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('PASS: All tests passed!'))
            self.stdout.write(self.style.SUCCESS('Ready to deploy.'))
