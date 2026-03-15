#!/usr/bin/env python
"""
Generate coverage report for the marketing app.
Shows which code is tested and which needs more tests.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.test_settings')
django.setup()

import coverage
from django.test.utils import get_runner
from django.conf import settings

print("=" * 70)
print("RUNNING TESTS WITH COVERAGE")
print("=" * 70)
print()

# Initialize coverage
cov = coverage.Coverage(source=['marketing'], omit=['*/tests/*', '*/migrations/*'])
cov.start()

# Run tests
TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1, interactive=False, keepdb=False)

# Run all marketing tests
test_labels = ['marketing.tests']
failures = test_runner.run_tests(test_labels)

# Stop coverage
cov.stop()
cov.save()

print()
print("=" * 70)
print("COVERAGE REPORT")
print("=" * 70)
print()

# Generate console report
cov.report(show_missing=True)

# Generate HTML report
print()
print("📊 Generating HTML coverage report...")
cov.html_report(directory='htmlcov')
print("✅ HTML report generated: htmlcov/index.html")

# Show summary
total_coverage = cov.report(file=open(os.devnull, 'w'))
print()
print(f"📈 Total Coverage: {total_coverage:.2f}%")

# Coverage assessment
if total_coverage >= 80:
    print("✅ Excellent! Coverage meets 80% threshold")
elif total_coverage >= 60:
    print("⚠️  Good progress, but aim for 80%+ coverage")
else:
    print("❌ Coverage is too low. Add more tests!")

print()
print("=" * 70)
print("NEXT STEPS")
print("=" * 70)
print()
print("1. Open htmlcov/index.html in your browser")
print("2. Look for red/yellow files that need more tests")
print("3. Add tests for uncovered code paths")
print("4. Run this script again to verify improvement")
print()

sys.exit(bool(failures))
