"""
Integration tests for CMS admin views.
Tests CMS CRUD operations, template rendering, and authentication.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from marketing.models import Page, Post, NavMenu, Footer, Category


User = get_user_model()


class CMSAuthenticationTest(TestCase):
    """Test CMS authentication and access control."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )

    def test_cms_requires_authentication(self):
        """Test CMS endpoints require authentication."""
        urls = [
            'cms-dashboard',
            'cms-page-list',
            'cms-post-list',
            'cms-navigation',
        ]

        for url_name in urls:
            url = reverse(url_name)
            response = self.client.get(url)
            # Should redirect to login or return 403
            self.assertIn(response.status_code, [302, 403],
                         f"{url_name} should require authentication")

    def test_cms_accessible_to_admin(self):
        """Test CMS is accessible to admin users."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.get(reverse('cms-dashboard'))
        self.assertEqual(response.status_code, 200,
                        "Admin should access CMS dashboard")


class CMSDashboardTest(TestCase):
    """Test CMS dashboard functionality."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_dashboard_renders(self):
        """Test dashboard renders without errors."""
        response = self.client.get(reverse('cms-dashboard'))
        self.assertEqual(response.status_code, 200,
                        "Dashboard should render successfully")

    def test_dashboard_uses_correct_template(self):
        """Test dashboard uses correct template."""
        response = self.client.get(reverse('cms-dashboard'))
        self.assertTemplateUsed(response, 'marketing/cms/dashboard.html')

    def test_dashboard_context_data(self):
        """Test dashboard passes required context data."""
        Page.objects.create(title='Test Page', slug='test', status='draft')
        Post.objects.create(title='Test Post', slug='test-post', status='draft')

        response = self.client.get(reverse('cms-dashboard'))
        self.assertIn('page_count', response.context)
        self.assertIn('post_count', response.context)
        self.assertIn('published_count', response.context)
        self.assertIn('draft_count', response.context)


class CMSPageCRUDTest(TestCase):
    """Test CMS Page CRUD operations."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_page_list_renders(self):
        """Test page list renders with correct template."""
        response = self.client.get(reverse('cms-page-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/page_list.html')

    def test_page_create_renders(self):
        """Test page create form renders."""
        response = self.client.get(reverse('cms-page-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/page_form.html')

    def test_page_create_submission(self):
        """Test page can be created."""
        response = self.client.post(reverse('cms-page-create'), {
            'title': 'New Page',
            'slug': 'new-page',
            'status': 'draft',
            'action': 'draft'
        }, follow=True)

        self.assertTrue(Page.objects.filter(slug='new-page').exists(),
                       "Page should be created")

    def test_page_edit_renders(self):
        """Test page edit form renders."""
        page = Page.objects.create(title='Test', slug='test', status='draft')
        response = self.client.get(reverse('cms-page-edit', args=[page.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/page_form.html')

    def test_page_delete(self):
        """Test page can be deleted."""
        page = Page.objects.create(title='Test', slug='test', status='draft')
        response = self.client.post(reverse('cms-page-delete', args=[page.id]))

        self.assertFalse(Page.objects.filter(id=page.id).exists(),
                        "Page should be deleted")


class CMSPostCRUDTest(TestCase):
    """Test CMS Post CRUD operations."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')
        self.category = Category.objects.create(name='Tech', slug='tech')

    def test_post_list_renders(self):
        """Test post list renders with correct template."""
        response = self.client.get(reverse('cms-post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/post_list.html')

    def test_post_create_renders(self):
        """Test post create form renders."""
        response = self.client.get(reverse('cms-post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/post_form.html')

    def test_post_create_submission(self):
        """Test post can be created."""
        response = self.client.post(reverse('cms-post-create'), {
            'title': 'New Post',
            'slug': 'new-post',
            'status': 'draft',
            'action': 'draft'
        }, follow=True)

        self.assertTrue(Post.objects.filter(slug='new-post').exists(),
                       "Post should be created")

    def test_post_edit_renders(self):
        """Test post edit form renders."""
        post = Post.objects.create(title='Test', slug='test', status='draft')
        response = self.client.get(reverse('cms-post-edit', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/post_form.html')


class CMSNavigationTest(TestCase):
    """Test CMS navigation and footer editing."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_navigation_edit_renders(self):
        """Test navigation edit page renders."""
        response = self.client.get(reverse('cms-navigation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/navigation.html')


class CMSImageUploadTest(TestCase):
    """Test CMS image upload functionality."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_upload_endpoint_requires_post(self):
        """Test upload endpoint only accepts POST requests."""
        response = self.client.get(reverse('cms-upload-image'))
        self.assertEqual(response.status_code, 405,
                        "Upload endpoint should require POST")

    def test_upload_endpoint_returns_json(self):
        """Test upload endpoint returns JSON response."""
        from io import BytesIO
        from PIL import Image

        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)

        response = self.client.post(reverse('cms-upload-image'), {
            'file': img_io
        })

        # Should return JSON (even if upload fails due to missing Cloudinary)
        self.assertIn(response.status_code, [200, 400, 500])
        self.assertEqual(response['Content-Type'], 'application/json')


class CMSTemplateIntegrityTest(TestCase):
    """Test that all CMS templates exist and render."""

    def setUp(self):
        """Set up test client and admin user."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')

    def test_all_cms_templates_exist(self):
        """Test all CMS templates exist and can be rendered."""
        # This test would catch missing template 500 errors
        template_tests = [
            ('cms-dashboard', 'marketing/cms/dashboard.html'),
            ('cms-page-list', 'marketing/cms/page_list.html'),
            ('cms-page-create', 'marketing/cms/page_form.html'),
            ('cms-post-list', 'marketing/cms/post_list.html'),
            ('cms-post-create', 'marketing/cms/post_form.html'),
            ('cms-navigation', 'marketing/cms/navigation.html'),
        ]

        for url_name, expected_template in template_tests:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200,
                           f"{url_name} should render successfully")
            self.assertTemplateUsed(response, expected_template,
                                  f"{url_name} should use {expected_template}")
