"""
Integration tests for public-facing views.
Tests homepage, page rendering, blog, and SEO endpoints.
"""

from django.test import TestCase, Client
from django.urls import reverse
from marketing.models import Page, Post, NavMenu, Footer, Category, PublishedStatus


class PublicHomepageTest(TestCase):
    """Test homepage rendering and functionality."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_homepage_renders(self):
        """Test homepage renders successfully."""
        response = self.client.get(reverse('marketing-home'))
        self.assertEqual(response.status_code, 200,
                        "Homepage should render")

    def test_homepage_uses_valid_template(self):
        """Test homepage uses a valid template."""
        response = self.client.get(reverse('marketing-home'))
        # Should use one of these templates
        self.assertIn(response.status_code, [200])
        templates = [t.name for t in response.templates]
        self.assertTrue(len(templates) > 0,
                       "Homepage should use a template")

    def test_homepage_with_cms_page(self):
        """Test homepage uses CMS page when available."""
        # Create a published homepage
        home = Page.objects.create(
            title='Home',
            slug='home',
            status=PublishedStatus.PUBLISHED
        )

        response = self.client.get(reverse('marketing-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')


class PageDetailTest(TestCase):
    """Test individual page rendering."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status=PublishedStatus.PUBLISHED,
            body_html='<p>Test content</p>'
        )

    def test_published_page_renders(self):
        """Test published page is accessible."""
        response = self.client.get(reverse('marketing-page-detail',
                                   args=['test-page']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test content')

    def test_draft_page_raises_404(self):
        """Test draft pages are not accessible."""
        self.page.status = PublishedStatus.DRAFT
        self.page.save()

        response = self.client.get(reverse('marketing-page-detail',
                                   args=['test-page']))
        self.assertEqual(response.status_code, 404,
                        "Draft pages should return 404")

    def test_page_contains_seo_data(self):
        """Test page includes SEO metadata."""
        nav = NavMenu.objects.create(name='Primary')
        footer = Footer.objects.create(label='Default')

        response = self.client.get(reverse('marketing-page-detail',
                                   args=['test-page']))

        # Check for SEO context data
        self.assertIn('seo', response.context,
                     "Page should include SEO context")


class BlogIndexTest(TestCase):
    """Test blog index rendering."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )

    def test_blog_index_renders(self):
        """Test blog index renders successfully."""
        response = self.client.get(reverse('marketing-blog-index'))
        self.assertEqual(response.status_code, 200)

    def test_blog_index_shows_published_posts(self):
        """Test blog index shows only published posts."""
        Post.objects.create(
            title='Published Post',
            slug='published-post',
            status=PublishedStatus.PUBLISHED,
            publish_at=timezone.now()
        )

        Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            status=PublishedStatus.DRAFT
        )

        response = self.client.get(reverse('marketing-blog-index'))
        self.assertContains(response, 'Published Post')
        self.assertNotContains(response, 'Draft Post')

    def test_blog_index_includes_categories(self):
        """Test blog index includes category data."""
        response = self.client.get(reverse('marketing-blog-index'))
        self.assertIn('categories', response.context,
                     "Blog index should include categories")


class BlogPostDetailTest(TestCase):
    """Test individual blog post rendering."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status=PublishedStatus.PUBLISHED,
            body_html='<p>Test content</p>'
        )

    def test_published_post_renders(self):
        """Test published post is accessible."""
        response = self.client.get(reverse('marketing-blog-post',
                                   args=['test-post']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test content')

    def test_draft_post_raises_404(self):
        """Test draft posts are not accessible."""
        self.post.status = PublishedStatus.DRAFT
        self.post.save()

        response = self.client.get(reverse('marketing-blog-post',
                                   args=['test-post']))
        self.assertEqual(response.status_code, 404,
                        "Draft posts should return 404")


class SEOEndpointsTest(TestCase):
    """Test SEO endpoints (robots.txt, sitemap.xml)."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_robots_txt_exists(self):
        """Test robots.txt endpoint returns 200."""
        # This test would catch /robots.txt 404 errors
        response = self.client.get(reverse('robots-txt'))
        self.assertEqual(response.status_code, 200,
                        "/robots.txt should return 200")

    def test_robots_txt_content_type(self):
        """Test robots.txt returns plain text."""
        response = self.client.get(reverse('robots-txt'))
        self.assertEqual(response['Content-Type'], 'text/plain')

    def test_robots_txt_content(self):
        """Test robots.txt contains required content."""
        response = self.client.get(reverse('robots-txt'))
        content = response.content.decode('utf-8')
        self.assertIn('User-agent:', content)
        self.assertIn('Sitemap:', content)

    def test_sitemap_xml_exists(self):
        """Test sitemap.xml endpoint returns 200."""
        # This test would catch /sitemap.xml 404 errors
        response = self.client.get(reverse('sitemap'))
        self.assertEqual(response.status_code, 200,
                        "/sitemap.xml should return 200")

    def test_sitemap_xml_content_type(self):
        """Test sitemap.xml returns XML."""
        response = self.client.get(reverse('sitemap'))
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_sitemap_xml_structure(self):
        """Test sitemap.xml has valid XML structure."""
        response = self.client.get(reverse('sitemap'))
        content = response.content.decode('utf-8')
        self.assertIn('<?xml version="1.0"?>', content)
        self.assertIn('<urlset', content)
        self.assertIn('</urlset>', content)

    def test_sitemap_includes_homepage(self):
        """Test sitemap includes homepage."""
        response = self.client.get(reverse('sitemap'))
        content = response.content.decode('utf-8')
        self.assertIn('<loc>', content)
        self.assertIn('</loc>', content)

    def test_sitemap_includes_published_pages(self):
        """Test sitemap includes published pages."""
        Page.objects.create(
            title='Test Page',
            slug='test-page',
            status=PublishedStatus.PUBLISHED
        )

        response = self.client.get(reverse('sitemap'))
        content = response.content.decode('utf-8')
        self.assertIn('test-page', content)

    def test_sitemap_excludes_draft_pages(self):
        """Test sitemap excludes draft pages."""
        Page.objects.create(
            title='Draft Page',
            slug='draft-page',
            status=PublishedStatus.DRAFT
        )

        response = self.client.get(reverse('sitemap'))
        content = response.content.decode('utf-8')
        self.assertNotIn('draft-page', content,
                        "Sitemap should not include draft pages")


class URLConfigurationTest(TestCase):
    """Test URL routing is correct."""

    def test_public_urls_are_resolvable(self):
        """Test all public URLs can be resolved."""
        client = Client()

        public_urls = [
            ('marketing-home', []),
            ('marketing-blog-index', []),
            ('robots-txt', []),
            ('sitemap', []),
        ]

        for url_name, args in public_urls:
            try:
                url = reverse(url_name, args=args)
                response = client.get(url)
                self.assertIn(response.status_code, [200],
                           f"{url_name} should be accessible")
            except Exception as e:
                self.fail(f"{url_name} URL resolution failed: {e}")

    def test_cms_urls_are_resolvable(self):
        """Test CMS URLs can be resolved (will redirect for auth)."""
        cms_urls = [
            ('cms-dashboard', []),
            ('cms-page-list', []),
            ('cms-post-list', []),
            ('cms-navigation', []),
        ]

        for url_name, args in cms_urls:
            try:
                url = reverse(url_name, args=args)
                # Don't need to check response, just that URL resolves
            except Exception as e:
                self.fail(f"{url_name} URL resolution failed: {e}")


from django.utils import timezone
