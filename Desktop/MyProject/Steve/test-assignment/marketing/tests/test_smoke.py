"""
Smoke tests - Quick sanity checks for critical functionality.
These tests run fast and catch major configuration/implementation issues.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from marketing.models import Page, Post, NavMenu, Footer, MediaAsset, PublishedStatus


User = get_user_model()


class CriticalEndpointSmokeTest(TestCase):
    """Quick tests for critical endpoints - fail fast on major issues."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_homepage_loads(self):
        """Test homepage loads without errors - CRITICAL."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: Homepage must load")

    def test_robots_txt_exists(self):
        """Test robots.txt exists - CRITICAL for SEO."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: /robots.txt must exist")

    def test_sitemap_xml_exists(self):
        """Test sitemap.xml exists - CRITICAL for SEO."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: /sitemap.xml must exist")

    def test_blog_index_loads(self):
        """Test blog index loads - CRITICAL."""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: Blog index must load")

    def test_cms_dashboard_requires_auth(self):
        """Test CMS dashboard exists and requires auth."""
        response = self.client.get('/cms/')
        # Should redirect or deny access, not 500
        self.assertIn(response.status_code, [302, 403],
                     "CMS dashboard should require authentication")


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
        items = nav.items
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)


class AuthenticationSmokeTest(TestCase):
    """Quick sanity checks for authentication."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_admin_can_login(self):
        """Test admin user can login - CRITICAL."""
        logged_in = self.client.login(username='admin', password='testpass123')
        self.assertTrue(logged_in, "CRITICAL: Admin login must work")

    def test_cms_accessible_after_login(self):
        """Test CMS is accessible after login - CRITICAL."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/cms/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: CMS must be accessible to admin")


class TemplateExistenceSmokeTest(TestCase):
    """Quick tests that critical templates exist."""

    def setUp(self):
        """Set up authenticated client."""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_cms_dashboard_template_exists(self):
        """Test CMS dashboard template exists - CRITICAL."""
        response = self.client.get('/cms/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: CMS dashboard template must exist")

    def test_page_list_template_exists(self):
        """Test page list template exists - CRITICAL."""
        response = self.client.get('/cms/pages/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: Page list template must exist")

    def test_post_list_template_exists(self):
        """Test post list template exists - CRITICAL."""
        response = self.client.get('/cms/posts/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: Post list template must exist")

    def test_navigation_template_exists(self):
        """Test navigation template exists - CRITICAL."""
        response = self.client.get('/cms/navigation/')
        self.assertEqual(response.status_code, 200,
                        "CRITICAL: Navigation template must exist")


class CMSCriticalWorkflowSmokeTest(TestCase):
    """Test critical CMS workflows work end-to-end."""

    def setUp(self):
        """Set up authenticated client."""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_create_page_workflow(self):
        """Test page can be created - CRITICAL workflow."""
        response = self.client.post('/cms/pages/new/', {
            'title': 'New Page',
            'slug': 'new-page',
            'status': 'draft',
            'action': 'draft'
        }, follow=True)

        self.assertTrue(Page.objects.filter(slug='new-page').exists(),
                       "CRITICAL: Page creation must work")

    def test_create_post_workflow(self):
        """Test post can be created - CRITICAL workflow."""
        response = self.client.post('/cms/posts/new/', {
            'title': 'New Post',
            'slug': 'new-post',
            'status': 'draft',
            'action': 'draft'
        }, follow=True)

        self.assertTrue(Post.objects.filter(slug='new-post').exists(),
                       "CRITICAL: Post creation must work")


class DesignContractSmokeTest(TestCase):
    """Verify design contract requirements are met."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_homepage_has_navigation(self):
        """Test homepage includes navigation - CRITICAL."""
        NavMenu.objects.create(name='Primary', items_json=[
            {'label': 'Home', 'url': '/'}
        ])

        response = self.client.get('/')
        self.assertIn('nav_menu', response.context,
                     "CRITICAL: Homepage must include navigation")

    def test_homepage_has_footer(self):
        """Test homepage includes footer - CRITICAL."""
        Footer.objects.create(label='Default', legal_text='© 2025')

        response = self.client.get('/')
        self.assertIn('footer', response.context,
                     "CRITICAL: Homepage must include footer")

    def test_homepage_has_seo_data(self):
        """Test homepage includes SEO metadata - CRITICAL."""
        response = self.client.get('/')
        self.assertIn('seo', response.context,
                     "CRITICAL: Homepage must include SEO data")
