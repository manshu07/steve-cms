# Automated Testing Suite for Django CMS

## Overview

This comprehensive testing suite prevents the critical issues that caused production failures. It catches model field mismatches, missing templates, broken endpoints, authentication issues, and SEO problems **before** they reach production.

## What These Tests Would Have Caught

### 1. Model Field Mismatches ✅
**Issue:** `uploaded_at` field doesn't exist on MediaAsset (it's `created_at`)
**Test:** `test_media_asset_has_uploaded_at_or_created_at` in `test_models.py`
**Result:** Would fail immediately, showing the field name mismatch

### 2. Missing Templates ✅
**Issue:** CMS CRUD views point to missing templates, causing 500 errors
**Test:** `test_all_cms_templates_exist` in `test_cms_views.py`
**Result:** Would show exactly which templates are missing and where

### 3. Broken Authentication ✅
**Issue:** `/cms/` redirects to `/accounts/login/` instead of proper CMS login
**Test:** `test_cms_requires_authentication` in `test_cms_views.py`
**Result:** Would show the incorrect redirect behavior

### 4. Missing SEO Endpoints ✅
**Issue:** `/robots.txt` and `/sitemap.xml` return 404
**Test:** `test_robots_txt_exists` and `test_sitemap_xml_exists` in `test_public_views.py`
**Result:** Would fail fast when endpoints don't return 200

### 5. Homepage Design Contract ✅
**Issue:** Homepage doesn't follow design system contract (nav, footer, SEO)
**Test:** `test_homepage_has_navigation`, `test_homepage_has_footer` in `test_smoke.py`
**Result:** Would verify design contract requirements are met

## Test Structure

```
marketing/tests/
├── __init__.py
├── test_models.py          # Model field integrity and business logic
├── test_cms_views.py       # CMS CRUD operations and authentication
├── test_public_views.py    # Public-facing pages and SEO
├── test_smoke.py           # Quick critical path tests
└── README.md               # This file
```

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Smoke Tests Only (Fast - 30 seconds)
```bash
python run_tests.py smoke
```

### Run Specific Test Suite
```bash
python run_tests.py models       # Model tests
python run_tests.py cms_views    # CMS tests
python run_tests.py public_views # Public view tests
```

### Run With Coverage Report
```bash
python run_tests.py coverage
```

### Run Specific Test
```bash
python manage.py test marketing.tests.test_smoke.CriticalEndpointSmokeTest
```

## Test Categories

### 1. Smoke Tests (Fast, Fail-Fast)
**Purpose:** Catch critical issues in under 30 seconds
**What they test:**
- Homepage loads
- SEO endpoints exist
- CMS accessible to admin
- Critical templates exist
- Basic workflows work

**When to run:** Before every commit, in CI/CD pipeline

### 2. Model Tests (Fast)
**Purpose:** Verify data model integrity
**What they test:**
- All required fields exist
- Field types are correct
- Model methods work
- Business logic (publish status, computed properties)
- JSON field handling

**When to run:** Before commits, after model changes

### 3. CMS View Tests (Medium)
**Purpose:** Test CMS CRUD operations
**What they test:**
- All CRUD operations work
- Templates exist and render
- Authentication works
- Forms validate properly
- File uploads work

**When to run:** Before commits, after CMS changes

### 4. Public View Tests (Medium)
**Purpose:** Test public-facing functionality
**What they test:**
- Pages render correctly
- Blog index and detail work
- SEO endpoints return correct content
- Published vs draft logic works
- Navigation and footer appear

**When to run:** Before commits, after view changes

## Continuous Integration

Add this to your `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python run_tests.py smoke
      - run: python run_tests.py coverage
```

## Test Coverage Goals

- **Unit Tests:** 80%+ coverage of models and utilities
- **Integration Tests:** All critical user flows
- **Smoke Tests:** 100% of critical endpoints

## Writing New Tests

### Template for a Model Test
```python
def test_model_feature(self):
    """Test what this feature does."""
    obj = Model.objects.create(field='value')
    self.assertEqual(obj.field, 'value')
```

### Template for a View Test
```python
def test_view_renders(self):
    """Test view renders successfully."""
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'template.html')
```

### Template for a Workflow Test
```python
def test_workflow(self):
    """Test end-to-end workflow."""
    # Create test data
    obj = Model.objects.create(field='value')

    # Perform action
    response = self.client.post(url, data={'key': 'value'})

    # Verify result
    self.assertRedirects(response, expected_url)
    self.assertTrue(Model.objects.filter(field='value').exists())
```

## Common Issues

### Tests Run But Don't Catch Real Bugs
**Solution:** Write tests that verify actual behavior, not just that code runs
```python
# BAD - Just runs code
def test_page_create(self):
    Page.objects.create(title='Test')

# GOOD - Verifies it works
def test_page_create(self):
    page = Page.objects.create(title='Test', slug='test')
    self.assertEqual(Page.objects.count(), 1)
    self.assertEqual(page.slug, 'test')
```

### Tests Are Brittle
**Solution:** Don't test implementation details, test behavior
```python
# BAD - Tests internal structure
def test_page_fields(self):
    self.assertTrue(hasattr(page, '_internal_state'))

# GOOD - Tests external behavior
def test_page_publish(self):
    page.publish()
    self.assertTrue(page.is_published)
```

### Tests Are Slow
**Solution:** Use factories, mock external services, only test what's needed
```python
# Use create() instead of full forms
# Mock Cloudinary uploads
# Use simple test data
```

## Next Steps

1. **Run smoke tests** before every commit
2. **Add CI/CD** to run tests automatically
3. **Increase coverage** to 80%+
4. **Add E2E tests** with Playwright for critical flows
5. **Monitor test results** and fix failures immediately

## Support

If tests fail:
1. Read the error message carefully
2. Check if it's a test issue or a code issue
3. Fix the code, not the test (unless test is wrong)
4. Run tests locally before pushing
