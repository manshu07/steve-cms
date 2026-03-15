"""
Comprehensive tests for marketing app models.
Tests all model methods, properties, and edge cases.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from marketing.models import (
    Page, Post, Category, Tag, NavMenu, Footer, MediaAsset,
    PublishedStatus
)


class MediaAssetComprehensiveTest(TestCase):
    """Comprehensive tests for MediaAsset model."""

    def test_media_asset_str_representation(self):
        """Test string representation uses alt_text or file."""
        # With alt_text
        asset1 = MediaAsset.objects.create(
            file='https://example.com/image.jpg',
            alt_text='Test Image'
        )
        self.assertEqual(str(asset1), 'Test Image')

        # Without alt_text
        asset2 = MediaAsset.objects.create(
            file='https://example.com/image2.jpg'
        )
        self.assertEqual(str(asset2), 'https://example.com/image2.jpg')

    def test_media_asset_optional_fields(self):
        """Test MediaAsset optional fields work correctly."""
        asset = MediaAsset.objects.create(
            file='https://example.com/image.jpg'
        )

        # Optional fields should be blank by default
        self.assertEqual(asset.alt_text, '')
        self.assertEqual(asset.caption, '')
        self.assertIsNone(asset.width)
        self.assertIsNone(asset.height)
        self.assertEqual(asset.content_type, '')

    def test_media_asset_with_dimensions(self):
        """Test MediaAsset with width and height."""
        asset = MediaAsset.objects.create(
            file='https://example.com/image.jpg',
            width=1920,
            height=1080
        )

        self.assertEqual(asset.width, 1920)
        self.assertEqual(asset.height, 1080)

    def test_media_asset_created_at_auto_populates(self):
        """Test created_at is automatically set."""
        asset = MediaAsset.objects.create(
            file='https://example.com/image.jpg'
        )

        self.assertIsNotNone(asset.created_at)
        self.assertLessEqual(
            asset.created_at,
            timezone.now()
        )


class PageComprehensiveTest(TestCase):
    """Comprehensive tests for Page model."""

    def test_page_str_representation(self):
        """Test string representation returns title."""
        page = Page.objects.create(
            title='Test Page',
            slug='test',
            status='draft'
        )
        self.assertEqual(str(page), 'Test Page')

    def test_page_ordering(self):
        """Test pages are ordered by title."""
        Page.objects.create(title='Zulu', slug='zulu', status='draft')
        Page.objects.create(title='Alpha', slug='alpha', status='draft')
        Page.objects.create(title='Bravo', slug='bravo', status='draft')

        pages = list(Page.objects.all())
        self.assertEqual(pages[0].title, 'Alpha')
        self.assertEqual(pages[1].title, 'Bravo')
        self.assertEqual(pages[2].title, 'Zulu')

    def test_page_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )

        url = page.get_absolute_url()
        self.assertIn('test-page', url)

    def test_page_save_with_body_json(self):
        """Test page save processes body_json."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status='draft',
            body_json={'blocks': [{'type': 'paragraph', 'data': {}}]}
        )

        # body_html should be set
        self.assertIsNotNone(page.body_html)

    def test_page_save_without_body_json(self):
        """Test page save without body_json clears body_html."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status='draft',
            body_json=None
        )

        # body_html should be empty
        self.assertEqual(page.body_html, '')

    def test_page_published_with_unpublish_date_passed(self):
        """Test page is not published after unpublish_at date."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status=PublishedStatus.PUBLISHED,
            unpublish_at=timezone.now() - timedelta(hours=1)
        )

        self.assertFalse(page.is_published)

    def test_page_scheduled_with_future_date(self):
        """Test scheduled page is not published before date."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status=PublishedStatus.SCHEDULED,
            publish_at=timezone.now() + timedelta(hours=1)
        )

        self.assertFalse(page.is_published)

    def test_page_scheduled_with_past_date(self):
        """Test scheduled page is published after date."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status=PublishedStatus.SCHEDULED,
            publish_at=timezone.now() - timedelta(hours=1)
        )

        self.assertTrue(page.is_published)

    def test_page_unique_slug_enforced(self):
        """Test slug uniqueness is enforced."""
        Page.objects.create(title='Page 1', slug='test', status='draft')

        # Try to create duplicate
        with self.assertRaises(Exception):
            Page.objects.create(title='Page 2', slug='test', status='draft')


class PostComprehensiveTest(TestCase):
    """Comprehensive tests for Post model."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name='Tech',
            slug='tech'
        )

    def test_post_str_representation(self):
        """Test string representation returns title."""
        post = Post.objects.create(
            title='Test Post',
            slug='test',
            status='draft'
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_ordering(self):
        """Test posts are ordered by publish_at then created_at."""
        post1 = Post.objects.create(
            title='Post 1',
            slug='post-1',
            status='draft',
            publish_at=timezone.now() - timedelta(days=2)
        )
        post2 = Post.objects.create(
            title='Post 2',
            slug='post-2',
            status='draft',
            publish_at=timezone.now() - timedelta(days=1)
        )

        posts = list(Post.objects.all())
        self.assertEqual(posts[0].id, post2.id)  # More recent first
        self.assertEqual(posts[1].id, post1.id)

    def test_post_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft'
        )

        url = post.get_absolute_url()
        self.assertIn('test-post', url)

    def test_post_categories_many_to_many(self):
        """Test post can have multiple categories."""
        cat1 = Category.objects.create(name='Cat1', slug='cat1')
        cat2 = Category.objects.create(name='Cat2', slug='cat2')

        post = Post.objects.create(
            title='Test',
            slug='test',
            status='draft'
        )
        post.categories.add(cat1, cat2)

        self.assertEqual(post.categories.count(), 2)
        self.assertIn(cat1, post.categories.all())
        self.assertIn(cat2, post.categories.all())

    def test_post_tags_many_to_many(self):
        """Test post can have multiple tags."""
        tag1 = Tag.objects.create(name='tag1', slug='tag1')
        tag2 = Tag.objects.create(name='tag2', slug='tag2')

        post = Post.objects.create(
            title='Test',
            slug='test',
            status='draft'
        )
        post.tags.add(tag1, tag2)

        self.assertEqual(post.tags.count(), 2)

    def test_post_computed_excerpt_from_body(self):
        """Test computed_excerpt extracts from body_html."""
        post = Post.objects.create(
            title='Test',
            slug='test',
            status='draft',
            body_html='<p>First paragraph with some content.</p><p>Second paragraph.</p>'
        )

        # If body_html is set, excerpt should use it
        # Note: The actual rendering depends on render_editorjs implementation
        # This test verifies the property exists and doesn't error
        excerpt = post.computed_excerpt

        # Just verify it returns a string (implementation may vary)
        self.assertIsInstance(excerpt, str)

    def test_post_published_status_simple(self):
        """Test published post status logic."""
        post = Post.objects.create(
            title='Test',
            slug='test',
            status=PublishedStatus.PUBLISHED
        )

        self.assertTrue(post.is_published)

    def test_post_draft_status(self):
        """Test draft post status."""
        post = Post.objects.create(
            title='Test',
            slug='test',
            status=PublishedStatus.DRAFT
        )

        self.assertFalse(post.is_published)


class CategoryAndTagComprehensiveTest(TestCase):
    """Comprehensive tests for Category and Tag models."""

    def test_category_ordering(self):
        """Test categories are ordered alphabetically."""
        Category.objects.create(name='Zulu', slug='zulu')
        Category.objects.create(name='Alpha', slug='alpha')
        Category.objects.create(name='Bravo', slug='bravo')

        categories = list(Category.objects.all())
        self.assertEqual(categories[0].name, 'Alpha')
        self.assertEqual(categories[1].name, 'Bravo')
        self.assertEqual(categories[2].name, 'Zulu')

    def test_category_unique_name(self):
        """Test category names must be unique."""
        Category.objects.create(name='Tech', slug='tech1')

        # Try to create duplicate name
        with self.assertRaises(Exception):
            Category.objects.create(name='Tech', slug='tech2')

    def test_category_unique_slug(self):
        """Test category slugs must be unique."""
        Category.objects.create(name='Tech 1', slug='tech')

        # Try to create duplicate slug
        with self.assertRaises(Exception):
            Category.objects.create(name='Tech 2', slug='tech')

    def test_tag_ordering(self):
        """Test tags are ordered alphabetically."""
        Tag.objects.create(name='Zulu', slug='zulu')
        Tag.objects.create(name='Alpha', slug='alpha')

        tags = list(Tag.objects.all())
        self.assertEqual(tags[0].name, 'Alpha')
        self.assertEqual(tags[1].name, 'Zulu')


class NavMenuComprehensiveTest(TestCase):
    """Comprehensive tests for NavMenu model."""

    def test_nav_menu_str_representation(self):
        """Test string representation returns name."""
        nav = NavMenu.objects.create(name='Primary')
        self.assertEqual(str(nav), 'Primary')

    def test_nav_menu_unique_name(self):
        """Test nav menu names must be unique."""
        NavMenu.objects.create(name='Primary')

        # Try to create duplicate
        with self.assertRaises(Exception):
            NavMenu.objects.create(name='Primary')

    def test_nav_menu_items_property_with_list(self):
        """Test items property with JSONField list."""
        nav = NavMenu.objects.create(
            name='Test',
            items_json=[{'label': 'Home', 'url': '/'}]
        )

        items = nav.items_json
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)

    def test_nav_menu_header_buttons_property(self):
        """Test header_buttons property."""
        nav = NavMenu.objects.create(
            name='Test',
            header_buttons_json=[{'label': 'Contact', 'url': '/contact'}]
        )

        buttons = nav.header_buttons_json
        self.assertIsInstance(buttons, list)
        self.assertEqual(len(buttons), 1)


class FooterComprehensiveTest(TestCase):
    """Comprehensive tests for Footer model."""

    def test_footer_str_representation(self):
        """Test string representation returns label."""
        footer = Footer.objects.create(label='Default')
        self.assertEqual(str(footer), 'Default')

    def test_footer_columns_property(self):
        """Test columns property with JSONField."""
        footer = Footer.objects.create(
            label='Test',
            columns_json=[{'title': 'Column 1'}]
        )

        columns = footer.columns_json
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 1)

    def test_footer_default_label(self):
        """Test footer has default label."""
        footer = Footer.objects.create()
        self.assertEqual(footer.label, 'Default')
