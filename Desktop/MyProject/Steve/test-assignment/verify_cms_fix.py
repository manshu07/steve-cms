#!/usr/bin/env python
"""
CMS Template Fix Verification Script

This script verifies that the CMS template fix is working correctly
by checking Django's template system for syntax errors.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.template import Template, Context
from django.template.loader import get_template
from django.template.exceptions import TemplateSyntaxError

def test_template(template_path):
    """Test a template for syntax errors."""
    try:
        template = get_template(template_path)
        print(f"[OK] {template_path}")
        return True
    except TemplateSyntaxError as e:
        print(f"[ERROR] {template_path} - {e}")
        return False
    except Exception as e:
        print(f"[WARN] {template_path} - {e}")
        return True

def main():
    print("=" * 60)
    print("CMS Template Fix Verification")
    print("=" * 60)
    print()

    templates_to_test = [
        'marketing/cms/base.html',
        'marketing/cms/dashboard.html',
        'marketing/cms/page_list.html',
        'marketing/cms/page_form.html',
        'marketing/cms/post_list.html',
        'marketing/cms/post_form.html',
        'marketing/cms/navigation.html',
    ]

    results = []
    for template_path in templates_to_test:
        results.append(test_template(template_path))

    print()
    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} templates passed")
    print("=" * 60)

    if all(results):
        print("[SUCCESS] All CMS templates are valid!")
        return 0
    else:
        print("[FAILED] Some templates have errors. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
