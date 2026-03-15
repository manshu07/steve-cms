"""
Test settings for Django project.
Disables template debugging to avoid Python 3.14 compatibility issues.
"""

from .settings import *

# Disable template debugging to avoid Python 3.14 compatibility issues
for template_config in TEMPLATES:
    template_config['OPTIONS']['debug'] = False

# Use faster password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debugging
DEBUG = False
TEMPLATE_DEBUG = False

# Faster test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Suppress logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
