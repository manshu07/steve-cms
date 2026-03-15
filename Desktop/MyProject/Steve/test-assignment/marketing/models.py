import re
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .renderers import render_lexical_json, render_editorjs, sanitize_html


class PublishedStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    SCHEDULED = 'scheduled', 'Scheduled'


class SeoFieldsMixin(models.Model):
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.URLField(max_length=500, blank=True)
    twitter_image = models.URLField(max_length=500, blank=True)

    class Meta:
        abstract = True


class MediaAsset(models.Model):
    file = models.URLField(max_length=500, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alt_text or self.file


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Page(SeoFieldsMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=PublishedStatus.choices,
        default=PublishedStatus.DRAFT,
    )
    publish_at = models.DateTimeField(blank=True, null=True)
    unpublish_at = models.DateTimeField(blank=True, null=True)
    body_json = models.JSONField(blank=True, null=True)
    body_html = models.TextField(blank=True)
    blocks_json = models.JSONField(blank=True, null=True)
    blocks_html = models.TextField(blank=True)
    primary_image = models.URLField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = False
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('marketing-page-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.body_json:
            rendered = render_editorjs(self.body_json)
            self.body_html = sanitize_html(rendered)
        else:
            self.body_html = ''
        if self.blocks_json:
            from .blocks import render_blocks

            self.blocks_html = sanitize_html(render_blocks(self.blocks_json))
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        now = timezone.now()
        if self.status == PublishedStatus.DRAFT:
            return False
        if self.status == PublishedStatus.PUBLISHED:
            if self.unpublish_at and self.unpublish_at <= now:
                return False
            return True
        if self.status == PublishedStatus.SCHEDULED:
            return bool(self.publish_at and self.publish_at <= now)
        return False


class Post(SeoFieldsMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=PublishedStatus.choices,
        default=PublishedStatus.DRAFT,
    )
    publish_at = models.DateTimeField(blank=True, null=True)
    author_name = models.CharField(max_length=255, blank=True)
    excerpt = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    body_json = models.JSONField(blank=True, null=True)
    body_html = models.TextField(blank=True)
    blocks_json = models.JSONField(blank=True, null=True)
    blocks_html = models.TextField(blank=True)
    cover_image = models.URLField(max_length=500, blank=True)
    primary_image = models.URLField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = False
        ordering = ['-publish_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('marketing-blog-post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.body_json:
            rendered = render_editorjs(self.body_json)
            self.body_html = sanitize_html(rendered)
        else:
            self.body_html = ''
        if self.blocks_json:
            from .blocks import render_blocks

            self.blocks_html = sanitize_html(render_blocks(self.blocks_json))
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        now = timezone.now()
        if self.status == PublishedStatus.DRAFT:
            return False
        if self.status == PublishedStatus.PUBLISHED:
            return True
        if self.status == PublishedStatus.SCHEDULED:
            return bool(self.publish_at and self.publish_at <= now)
        return False

    @property
    def computed_excerpt(self):
        """Return the explicit excerpt, or auto-generate from content."""
        if self.excerpt:
            return self.excerpt
        # Fall back to first paragraph from body_html or blocks_html
        html = self.body_html or self.blocks_html or ''
        match = re.search(r'<p[^>]*>(.*?)</p>', html, flags=re.I | re.S)
        if match:
            raw = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            from django.utils.text import Truncator
            return Truncator(raw).chars(200)
        return ''


class NavMenu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    items_json = models.JSONField(blank=True, null=True)
    # Header buttons configuration
    header_buttons_json = models.JSONField(blank=True, null=True, help_text="Array of button objects with label, url, style, and open_new_tab")

    def __str__(self):
        return self.name

    @property
    def items(self):
        """Return items as a list, handling both JSONField and string data."""
        if not self.items_json:
            return []
        # If it's already a list (from JSONField), return it
        if isinstance(self.items_json, list):
            return self.items_json
        # If it's a string, try to parse it
        import json
        try:
            return json.loads(self.items_json)
        except (json.JSONDecodeError, TypeError):
            return []

    @property
    def header_buttons(self):
        """Return header buttons as a list."""
        if not self.header_buttons_json:
            return []
        # If it's already a list (from JSONField), return it
        if isinstance(self.header_buttons_json, list):
            return self.header_buttons_json
        # If it's a string, try to parse it
        import json
        try:
            return json.loads(self.header_buttons_json)
        except (json.JSONDecodeError, TypeError):
            return []


class NavItem(models.Model):
    menu = models.ForeignKey(NavMenu, on_delete=models.CASCADE, related_name='items')
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, blank=True, null=True)
    external = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class Footer(models.Model):
    label = models.CharField(max_length=100, default='Default')
    columns_json = models.JSONField(blank=True, null=True)
    cta_title = models.CharField(max_length=255, blank=True)
    cta_body = models.TextField(blank=True)
    cta_button_label = models.CharField(max_length=100, blank=True)
    cta_button_url = models.CharField(max_length=255, blank=True)
    legal_text = models.TextField(blank=True)

    def __str__(self):
        return self.label

    @property
    def columns(self):
        """Return columns as a list, handling both JSONField and string data."""
        if not self.columns_json:
            return []
        # If it's already a list (from JSONField), return it
        if isinstance(self.columns_json, list):
            return self.columns_json
        # If it's a string, try to parse it
        import json
        try:
            return json.loads(self.columns_json)
        except (json.JSONDecodeError, TypeError):
            return []
