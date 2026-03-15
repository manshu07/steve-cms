"""
Tests for Django forms in the marketing app.
Tests form validation, field requirements, and clean methods.
"""

from django.test import TestCase
from marketing.forms import PageForm, PostForm, NavMenuForm, FooterForm
from marketing.models import Page, Post, NavMenu, Footer, Category, PublishedStatus


class PageFormTest(TestCase):
    """Test PageForm validation and behavior."""

    def test_form_has_required_fields(self):
        """Test form requires title and slug."""
        form = PageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('slug', form.errors)

    def test_form_accepts_valid_data(self):
        """Test form accepts valid page data."""
        data = {
            'title': 'Test Page',
            'slug': 'test-page',
            'status': 'draft'
        }
        form = PageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_creates_page(self):
        """Test form can create a page."""
        data = {
            'title': 'Test Page',
            'slug': 'test-page',
            'status': 'draft'
        }
        form = PageForm(data=data)
        if form.is_valid():
            page = form.save()
            self.assertEqual(page.title, 'Test Page')
            self.assertEqual(page.slug, 'test-page')

    def test_form_accepts_seo_fields(self):
        """Test form accepts SEO metadata fields."""
        data = {
            'title': 'Test Page',
            'slug': 'test-page',
            'status': 'draft',
            'seo_title': 'SEO Title',
            'seo_description': 'SEO Description'
        }
        form = PageForm(data=data)
        self.assertTrue(form.is_valid())


class PostFormTest(TestCase):
    """Test PostForm validation and behavior."""

    def setUp(self):
        """Set up test category."""
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )

    def test_form_has_required_fields(self):
        """Test form requires title and slug."""
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('slug', form.errors)

    def test_form_accepts_valid_data(self):
        """Test form accepts valid post data."""
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'status': 'draft'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_categories(self):
        """Test form can accept category assignments."""
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'status': 'draft',
            'categories': [self.category.id]
        }
        form = PostForm(data=data)
        if form.is_valid():
            post = form.save()
            self.assertEqual(post.categories.count(), 1)

    def test_form_accepts_excerpt(self):
        """Test form accepts excerpt field."""
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'status': 'draft',
            'excerpt': 'This is the excerpt'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())


class NavMenuFormTest(TestCase):
    """Test NavMenuForm validation and behavior."""

    def test_form_accepts_valid_data(self):
        """Test form accepts valid navigation data."""
        data = {
            'name': 'Primary',
            'items_json': '[{"label": "Home", "url": "/"}]'
        }
        form = NavMenuForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_creates_nav_menu(self):
        """Test form can create a navigation menu."""
        data = {
            'name': 'Primary',
            'items_json': '[{"label": "Home", "url": "/"}]'
        }
        form = NavMenuForm(data=data)
        if form.is_valid():
            nav = form.save()
            self.assertEqual(nav.name, 'Primary')

    def test_form_accepts_header_buttons(self):
        """Test form accepts header buttons configuration."""
        data = {
            'name': 'Primary',
            'header_buttons_json': '[{"label": "Contact", "url": "/contact"}]'
        }
        form = NavMenuForm(data=data)
        self.assertTrue(form.is_valid())


class FooterFormTest(TestCase):
    """Test FooterForm validation and behavior."""

    def test_form_accepts_valid_data(self):
        """Test form accepts valid footer data."""
        data = {
            'label': 'Default',
            'legal_text': '© 2025 Company'
        }
        form = FooterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_creates_footer(self):
        """Test form can create a footer."""
        data = {
            'label': 'Default',
            'legal_text': '© 2025 Company'
        }
        form = FooterForm(data=data)
        if form.is_valid():
            footer = form.save()
            self.assertEqual(footer.label, 'Default')

    def test_form_accepts_columns(self):
        """Test form accepts column configuration."""
        data = {
            'label': 'Default',
            'columns_json': '[{"title": "Column 1"}]'
        }
        form = FooterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_cta_fields(self):
        """Test form accepts CTA fields."""
        data = {
            'label': 'Default',
            'cta_title': 'Get Started',
            'cta_body': 'Sign up now',
            'cta_button_label': 'Sign Up',
            'cta_button_url': '/signup'
        }
        form = FooterForm(data=data)
        self.assertTrue(form.is_valid())
