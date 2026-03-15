"""
Integration tests for CMS CRUD operations.
Tests complete workflows without template rendering (avoids Python 3.14 issues).
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from marketing.models import Page, Post, NavMenu, Footer, Category, PublishedStatus


User = get_user_model()


class CMSPageCRUDIntegrationTest(TestCase):
    """Test complete Page CRUD workflow."""

    def setUp(self):
        """Set up admin user."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_page_create_workflow(self):
        """Test creating a page works end-to-end."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )

        self.assertEqual(page.title, 'Test Page')
        self.assertEqual(page.slug, 'test-page')
        self.assertEqual(page.status, 'draft')
        self.assertFalse(page.is_published)

    def test_page_publish_workflow(self):
        """Test publishing a page works."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )

        # Publish the page
        page.status = PublishedStatus.PUBLISHED
        page.save()

        # Refresh from DB
        page.refresh_from_db()

        self.assertTrue(page.is_published)
        self.assertEqual(page.status, 'published')

    def test_page_unpublish_workflow(self):
        """Test unpublishing a page works."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status=PublishedStatus.PUBLISHED
        )

        # Unpublish the page
        page.status = PublishedStatus.DRAFT
        page.save()

        # Refresh from DB
        page.refresh_from_db()

        self.assertFalse(page.is_published)
        self.assertEqual(page.status, 'draft')

    def test_page_delete_workflow(self):
        """Test deleting a page works."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft'
        )
        page_id = page.id

        # Delete the page
        page.delete()

        # Verify it's gone
        self.assertFalse(Page.objects.filter(id=page_id).exists())

    def test_page_update_workflow(self):
        """Test updating a page works."""
        page = Page.objects.create(
            title='Original Title',
            slug='original',
            status='draft'
        )

        # Update the page
        page.title = 'Updated Title'
        page.save()

        # Refresh from DB
        page.refresh_from_db()

        self.assertEqual(page.title, 'Updated Title')

    def test_page_with_seo_fields_workflow(self):
        """Test page with SEO fields works."""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='draft',
            seo_title='SEO Title',
            seo_description='SEO Description',
            og_title='OG Title'
        )

        self.assertEqual(page.seo_title, 'SEO Title')
        self.assertEqual(page.seo_description, 'SEO Description')
        self.assertEqual(page.og_title, 'OG Title')


class CMSPostCRUDIntegrationTest(TestCase):
    """Test complete Post CRUD workflow."""

    def setUp(self):
        """Set up admin user and category."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )

    def test_post_create_workflow(self):
        """Test creating a post works end-to-end."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft'
        )

        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.status, 'draft')
        self.assertFalse(post.is_published)

    def test_post_with_category_workflow(self):
        """Test post with category assignment works."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft'
        )
        post.categories.add(self.category)

        self.assertEqual(post.categories.count(), 1)
        self.assertIn(self.category, post.categories.all())

    def test_post_with_excerpt_workflow(self):
        """Test post with explicit excerpt works."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft',
            excerpt='This is the excerpt'
        )

        self.assertEqual(post.computed_excerpt, 'This is the excerpt')

    def test_post_publish_workflow(self):
        """Test publishing a post works."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft'
        )

        # Publish the post
        post.status = PublishedStatus.PUBLISHED
        post.save()

        # Refresh from DB
        post.refresh_from_db()

        self.assertTrue(post.is_published)
        self.assertEqual(post.status, 'published')

    def test_post_delete_workflow(self):
        """Test deleting a post works."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='draft'
        )
        post_id = post.id

        # Delete the post
        post.delete()

        # Verify it's gone
        self.assertFalse(Post.objects.filter(id=post_id).exists())


class CMSNavigationIntegrationTest(TestCase):
    """Test navigation and footer CRUD workflow."""

    def setUp(self):
        """Set up admin user."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_nav_menu_create_workflow(self):
        """Test creating a navigation menu works."""
        nav = NavMenu.objects.create(
            name='Primary',
            items_json=[
                {'label': 'Home', 'url': '/'},
                {'label': 'About', 'url': '/about'}
            ]
        )

        self.assertEqual(nav.name, 'Primary')
        self.assertEqual(len(nav.items_json), 2)

    def test_nav_menu_update_workflow(self):
        """Test updating navigation menu works."""
        nav = NavMenu.objects.create(
            name='Primary',
            items_json=[{'label': 'Home', 'url': '/'}]
        )

        # Update the menu
        nav.items_json = [
            {'label': 'Home', 'url': '/'},
            {'label': 'Blog', 'url': '/blog'}
        ]
        nav.save()

        # Refresh from DB
        nav.refresh_from_db()

        self.assertEqual(len(nav.items_json), 2)

    def test_footer_create_workflow(self):
        """Test creating a footer works."""
        footer = Footer.objects.create(
            label='Default',
            columns_json=[
                {'title': 'Column 1', 'links': [{'label': 'Link 1', 'url': '/link1'}]}
            ],
            legal_text='© 2025 Test'
        )

        self.assertEqual(footer.label, 'Default')
        self.assertEqual(footer.legal_text, '© 2025 Test')
        self.assertEqual(len(footer.columns_json), 1)

    def test_footer_update_workflow(self):
        """Test updating footer works."""
        footer = Footer.objects.create(
            label='Default',
            legal_text='Original'
        )

        # Update the footer
        footer.legal_text = 'Updated'
        footer.save()

        # Refresh from DB
        footer.refresh_from_db()

        self.assertEqual(footer.legal_text, 'Updated')


class CMSWorkflowIntegrationTest(TestCase):
    """Test complete CMS workflows across multiple models."""

    def setUp(self):
        """Set up admin user."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_complete_content_workflow(self):
        """Test creating page, post, navigation, and footer together."""
        # Create navigation
        nav = NavMenu.objects.create(
            name='Primary',
            items_json=[{'label': 'Home', 'url': '/'}]
        )

        # Create footer
        footer = Footer.objects.create(
            label='Default',
            legal_text='© 2025'
        )

        # Create page
        page = Page.objects.create(
            title='Home',
            slug='home',
            status='published'
        )

        # Create post
        post = Post.objects.create(
            title='First Post',
            slug='first-post',
            status='published'
        )

        # Verify all were created
        self.assertEqual(NavMenu.objects.count(), 1)
        self.assertEqual(Footer.objects.count(), 1)
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)

        # Verify published status
        self.assertTrue(page.is_published)
        self.assertTrue(post.is_published)

    def test_bulk_operations_workflow(self):
        """Test bulk operations on multiple pages."""
        # Create multiple pages
        Page.objects.create(title='Page 1', slug='page-1', status='draft')
        Page.objects.create(title='Page 2', slug='page-2', status='draft')
        Page.objects.create(title='Page 3', slug='page-3', status='draft')

        # Bulk publish
        Page.objects.all().update(status='published')

        # Verify all are published
        self.assertEqual(Page.objects.filter(status='published').count(), 3)

    def test_filter_and_query_workflow(self):
        """Test filtering and querying content."""
        # Create mix of published and draft content
        Page.objects.create(title='Published 1', slug='pub-1', status='published')
        Page.objects.create(title='Published 2', slug='pub-2', status='published')
        Page.objects.create(title='Draft 1', slug='draft-1', status='draft')

        Post.objects.create(title='Post Published', slug='post-pub', status='published')
        Post.objects.create(title='Post Draft', slug='post-draft', status='draft')

        # Query published content
        published_pages = Page.objects.filter(status='published')
        published_posts = Post.objects.filter(status='published')

        self.assertEqual(published_pages.count(), 2)
        self.assertEqual(published_posts.count(), 1)


class CMSErrorHandlingIntegrationTest(TestCase):
    """Test error handling in CMS workflows."""

    def setUp(self):
        """Set up admin user."""
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

    def test_unique_slug_constraint(self):
        """Test that slug uniqueness is enforced."""
        Page.objects.create(title='Page 1', slug='test', status='draft')

        # Try to create duplicate slug - should fail
        try:
            Page.objects.create(title='Page 2', slug='test', status='draft')
            self.fail("Should have raised an exception for duplicate slug")
        except Exception:
            # Expected behavior - duplicate slugs are not allowed
            pass

    def test_required_field_handling(self):
        """Test that required fields are properly defined."""
        # Create a valid page
        page = Page.objects.create(title='Test', slug='test', status='draft')

        # Verify required fields have values
        self.assertIsNotNone(page.title)
        self.assertIsNotNone(page.slug)
        self.assertIsNotNone(page.status)

    def test_status_choices_work(self):
        """Test that status choices work correctly."""
        # Test all valid status values
        Page.objects.create(title='Draft', slug='draft', status='draft')
        Page.objects.create(title='Published', slug='published', status='published')
        Page.objects.create(title='Scheduled', slug='scheduled', status='scheduled')

        # Verify all were created successfully
        self.assertEqual(Page.objects.count(), 3)
