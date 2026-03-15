"""
Smoke tests - Quick sanity checks for critical functionality.
These tests run fast and catch major configuration/implementation issues.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from marketing.models import Page, Post, NavMenu, Footer, MediaAsset, PublishedStatus


User = get_user_model()


class ModelIntegritySmokeTest(TestCase):
    """Quick sanity checks for model structure."""

    def test_media_asset_timestamp_field(self):
        """Test MediaAsset has correct timestamp field - CRITICAL."""
        # This would catch uploaded_at vs created_at mismatch
        asset = MediaAsset.objects.create(
            file='https://example.com/test.jpg',
            alt_text='Test'
        )

        # Must have created_at
        self.assertTrue(hasattr(asset, 'created_at'),
                       "CRITICAL: MediaAsset must have created_at field")

        # Must NOT have uploaded_at
        self.assertFalse(hasattr(asset, 'uploaded_at'),
                        "CRITICAL: MediaAsset should not have uploaded_at")

    def test_page_can_be_created(self):
        """Test Page model works - CRITICAL."""
        page = Page.objects.create(
            title='Test',
            slug='test',
            status='draft'
        )
        self.assertIsNotNone(page.id)

    def test_post_can_be_created(self):
        """Test Post model works - CRITICAL."""
        post = Post.objects.create(
            title='Test',
            slug='test',
            status='draft'
        )
        self.assertIsNotNone(post.id)

    def test_nav_menu_json_handling(self):
        """Test NavMenu handles JSON correctly - CRITICAL."""
        nav = NavMenu.objects.create(
            name='Test',
            items_json=[{'label': 'Home', 'url': '/'}]
        )
        items_list = nav.items_json
        self.assertIsInstance(items_list, list)
        self.assertEqual(len(items_list), 1)

    def test_footer_json_handling(self):
        """Test Footer handles JSON correctly - CRITICAL."""
        footer = Footer.objects.create(
            label='Test',
            columns_json=[{'title': 'Column 1'}]
        )
        columns_list = footer.columns_json
        self.assertIsInstance(columns_list, list)
        self.assertEqual(len(columns_list), 1)


class AuthenticationSmokeTest(TestCase):
    """Quick sanity checks for authentication."""

    def setUp(self):
        """Set up test client and user."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_admin_can_be_created(self):
        """Test admin user can be created - CRITICAL."""
        admin = User.objects.create_user(
            username='admin2',
            password='testpass123',
            is_staff=True
        )
        self.assertTrue(admin.is_staff)


class ModelBusinessLogicSmokeTest(TestCase):
    """Test critical business logic."""

    def test_page_publish_status(self):
        """Test page publish status logic - CRITICAL."""
        page = Page.objects.create(
            title='Published Page',
            slug='published',
            status=PublishedStatus.PUBLISHED
        )
        self.assertTrue(page.is_published,
                       "Published pages should return True for is_published")

    def test_draft_page_status(self):
        """Test draft page status - CRITICAL."""
        page = Page.objects.create(
            title='Draft Page',
            slug='draft',
            status=PublishedStatus.DRAFT
        )
        self.assertFalse(page.is_published,
                        "Draft pages should return False for is_published")

    def test_post_publish_status(self):
        """Test post publish status logic - CRITICAL."""
        post = Post.objects.create(
            title='Published Post',
            slug='published',
            status=PublishedStatus.PUBLISHED
        )
        self.assertTrue(post.is_published,
                       "Published posts should return True for is_published")


class SEOEndpointsExistenceTest(TestCase):
    """Test that SEO URLs are configured."""

    def test_robots_txt_url_resolves(self):
        """Test robots.txt URL can be resolved - CRITICAL."""
        from django.urls import reverse
        try:
            url = reverse('robots-txt')
            self.assertEqual(url, '/robots.txt')
        except Exception as e:
            self.fail(f"robots.txt URL should resolve: {e}")

    def test_sitemap_xml_url_resolves(self):
        """Test sitemap.xml URL can be resolved - CRITICAL."""
        from django.urls import reverse
        try:
            url = reverse('sitemap')
            self.assertEqual(url, '/sitemap.xml')
        except Exception as e:
            self.fail(f"sitemap.xml URL should resolve: {e}")


class CMSURLsExistenceTest(TestCase):
    """Test that CMS URLs are configured."""

    def test_cms_dashboard_url_resolves(self):
        """Test CMS dashboard URL can be resolved - CRITICAL."""
        from django.urls import reverse
        try:
            url = reverse('cms-dashboard')
            self.assertEqual(url, '/cms/')
        except Exception as e:
            self.fail(f"CMS dashboard URL should resolve: {e}")

    def test_cms_page_list_url_resolves(self):
        """Test page list URL can be resolved - CRITICAL."""
        from django.urls import reverse
        try:
            url = reverse('cms-page-list')
            self.assertEqual(url, '/cms/pages/')
        except Exception as e:
            self.fail(f"Page list URL should resolve: {e}")

    def test_cms_post_list_url_resolves(self):
        """Test post list URL can be resolved - CRITICAL."""
        from django.urls import reverse
        try:
            url = reverse('cms-post-list')
            self.assertEqual(url, '/cms/posts/')
        except Exception as e:
            self.fail(f"Post list URL should resolve: {e}")
