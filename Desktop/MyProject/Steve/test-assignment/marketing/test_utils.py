"""
Test utilities to work around Python 3.14 + Django template compatibility issues.
"""

from django.test import TestCase, Client
from django.test.utils import override_settings
from django.contrib.auth import get_user_model


User = get_user_model()


class TemplateFreeTestCase(TestCase):
    """
    Base test class that avoids template rendering issues in Python 3.14.
    Use this for view tests that would normally trigger template context copying.
    """

    def setUp(self):
        """Set up test client without template debugging."""
        self.client = Client()

    def assert_response_status(self, response, expected_status=200):
        """Assert response status without accessing template context."""
        self.assertEqual(response.status_code, expected_status)

    def assert_response_contains(self, response, text):
        """Assert response contains text without template context."""
        self.assertIn(text, response.content.decode('utf-8'))


class CMSTestCase(TemplateFreeTestCase):
    """Base test case for CMS tests with common setup."""

    def setUp(self):
        """Set up admin user and client."""
        super().setUp()
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.login(username='admin', password='testpass123')


def skip_template_tests(func):
    """
    Decorator to skip tests that require template rendering on Python 3.14.
    Use this for tests that would trigger the template context copying issue.
    """
    import sys
    import unittest

    if sys.version_info >= (3, 14):
        return unittest.skip("Template rendering tests skipped on Python 3.14")(func)
    return func
