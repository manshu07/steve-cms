"""
Unit tests for marketing models.
Tests model field integrity, methods, and business logic.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from marketing.models import Page, Post, Category, Tag, NavMenu, Footer, MediaAsset, PublishedStatus


class MediaAssetModelTest(TestCase):
    """Test MediaAsset model fields and structure."""

    def test_media_asset_has_uploaded_at_or_created_at(self):
        """Ensure MediaAsset has proper timestamp field."""
        # This test would catch the uploaded_at vs created_at mismatch
        asset = MediaAsset.objects.create(
            file='https://example.com/image.jpg',
            alt_text='Test Image'
        )

        # Check for created_at field (correct field name)
        self.assertTrue(hasattr(asset, 'created_at'),
                       "MediaAsset must have created_at field")

        # Ensure created_at is auto-populated
        self.assertIsNotNone(asset.created_at)

        # Check that uploaded_at does NOT exist (would be an error)
        self.assertFalse(hasattr(asset, 'uploaded_at'),
                        "MediaAsset should not have uploaded_at field, use created_at instead")

    def test_media_asset_required_fields(self):
        """Test MediaAsset required and optional fields."""
        asset = MediaAsset.objects.create(
            file='https://example.com/image.jpg'
        )

        # Should work with minimal fields
        self.assertEqual(asset.file, 'https://example.com/image.jpg')
        self.assertEqual(asset.alt_text, '')


class PageModelTest(TestCase):
    """Test Page model fields, methods, and publish logic."""

    def test_page_has_seo_fields(self):
        """Ensure Page has all required SEO fields."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )

        seo_fields = ['seo_title', 'seo_description', 'og_title',
                     'og_description', 'og_image', 'twitter_image']
        for field in seo_fields:
            self.assertTrue(hasattr(page, field),
                          f"Page must have {field} field")

    def test_page_is_published_draft(self):
        """Test is_published property for draft status."""
        page = Page.objects.create(
            title='Draft Page',
            slug='draft-page',
            status=PublishedStatus.DRAFT
        )
        self.assertFalse(page.is_published)

    def test_page_is_published_published(self):
        """Test is_published property for published status."""
        page = Page.objects.create(
            title='Published Page',
            slug='published-page',
            status=PublishedStatus.PUBLISHED
        )
        self.assertTrue(page.is_published)

    def test_page_is_published_with_unpublish_date(self):
        """Test is_published respects unpublish_at date."""
        page = Page.objects.create(
            title='Expired Page',
            slug='expired-page',
            status=PublishedStatus.PUBLISHED,
            unpublish_at=timezone.now() - timedelta(hours=1)
        )
        self.assertFalse(page.is_published,
                        "Page should not be published after unpublish_at date")

    def test_page_is_published_scheduled_future(self):
        """Test is_published for scheduled posts with future date."""
        page = Page.objects.create(
            title='Future Page',
            slug='future-page',
            status=PublishedStatus.SCHEDULED,
            publish_at=timezone.now() + timedelta(hours=1)
        )
        self.assertFalse(page.is_published,
                        "Scheduled page should not be published before publish_at")

    def test_page_is_published_scheduled_past(self):
        """Test is_published for scheduled posts with past date."""
        page = Page.objects.create(
            title='Past Scheduled Page',
            slug='past-scheduled-page',
            status=PublishedStatus.SCHEDULED,
            publish_at=timezone.now() - timedelta(hours=1)
        )
        self.assertTrue(page.is_published,
                       "Scheduled page should be published after publish_at")

    def test_page_get_absolute_url(self):
        """Test Page URL generation."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )
        url = page.get_absolute_url()
        self.assertIn('test-page', url)


class PostModelTest(TestCase):
    """Test Post model fields, methods, and publish logic."""

    def test_post_computed_excerpt_explicit(self):
        """Test computed_excerpt returns explicit excerpt when set."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft',
            excerpt='This is the explicit excerpt.'
        )
        self.assertEqual(post.computed_excerpt, 'This is the explicit excerpt.')

    def test_post_computed_excerpt_fallback(self):
        """Test computed_excerpt auto-generates from body_html."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft',
            body_html='<p>This is the first paragraph with some content.</p><p>Second paragraph.</p>'
        )
        excerpt = post.computed_excerpt
        self.assertIn('first paragraph', excerpt.lower())
        self.assertLessEqual(len(excerpt), 210)  # 200 + margin


class NavMenuModelTest(TestCase):
    """Test NavMenu model JSON field handling."""

    def test_nav_menu_items_property_list(self):
        """Test items property returns list from JSONField."""
        nav = NavMenu.objects.create(
            name='Test Menu',
            items_json=[{'label': 'Home', 'url': '/'}]
        )
        items = nav.items
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['label'], 'Home')

    def test_nav_menu_items_property_string(self):
        """Test items property parses string JSON."""
        import json
        items_list = [{'label': 'About', 'url': '/about'}]
        nav = NavMenu.objects.create(
            name='Test Menu',
            items_json=json.dumps(items_list)
        )
        items = nav.items
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)

    def test_nav_menu_items_property_empty(self):
        """Test items property handles empty/null values."""
        nav = NavMenu.objects.create(name='Empty Menu')
        items = nav.items
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)


class FooterModelTest(TestCase):
    """Test Footer model JSON field handling."""

    def test_footer_columns_property_list(self):
        """Test columns property returns list from JSONField."""
        footer = Footer.objects.create(
            label='Test Footer',
            columns_json=[{'title': 'Column 1', 'links': []}]
        )
        columns = footer.columns
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 1)


class CategoryAndTagTest(TestCase):
    """Test Category and Tag models."""

    def test_category_str(self):
        """Test Category string representation."""
        cat = Category.objects.create(name='Technology', slug='technology')
        self.assertEqual(str(cat), 'Technology')

    def test_tag_str(self):
        """Test Tag string representation."""
        tag = Tag.objects.create(name='AI', slug='ai')
        self.assertEqual(str(tag), 'AI')
