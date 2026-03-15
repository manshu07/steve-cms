"""
Models for drag/drop page builder.
Extends existing Page model with builder-specific functionality.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
import bleach

User = get_user_model()


class BuilderTemplate(models.Model):
    """Reusable page templates for the builder."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=500, blank=True)
    builder_data = models.JSONField(help_text="Component structure for template")

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_templates'
    )
    is_public = models.BooleanField(default=True, help_text="Available to all users")
    is_active = models.BooleanField(default=True)

    # Version tracking
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Builder Template"
        verbose_name_plural = "Builder Templates"

    def __str__(self):
        return self.name

    def duplicate(self):
        """Create a copy of this template."""
        new_data = self.builder_data.copy()
        new_template = BuilderTemplate.objects.create(
            name=f"{self.name} (Copy)",
            description=self.description,
            thumbnail=self.thumbnail,
            builder_data=new_data,
            created_by=self.created_by,
            is_public=False,
        )
        return new_template


class ComponentRegistry(models.Model):
    """Registered components available in the builder."""

    COMPONENT_CATEGORIES = (
        ('layout', 'Layout Components'),
        ('content', 'Content Components'),
        ('media', 'Media Components'),
        ('form', 'Form Components'),
    )

    name = models.CharField(max_length=100, unique=True, help_text="Component identifier (e.g., 'heading')")
    category = models.CharField(max_length=20, choices=COMPONENT_CATEGORIES)

    # Component metadata
    icon = models.CharField(max_length=100, help_text="Material Design icon name (e.g., 'mdi:format-title')")
    label = models.CharField(max_length=100, help_text="Human-readable label")

    # Component schema
    schema = models.JSONField(help_text="JSON Schema for component properties")
    default_props = models.JSONField(help_text="Default property values")

    # Feature flags
    is_enabled = models.BooleanField(default=True)
    requires_asset = models.BooleanField(default=False, help_text="Does component need an image/file?")
    is_editable = models.BooleanField(default=True, help_text="Can component content be edited inline?")

    # Frontend rendering
    render_component = models.CharField(
        max_length=255,
        help_text="React component path (e.g., 'builder.components.Heading')"
    )

    # Sorting
    order = models.PositiveIntegerField(default=0, help_text="Display order in palette")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Component Registry"
        verbose_name_plural = "Component Registry"

    def __str__(self):
        return self.label

    def clean(self):
        """Validate schema is valid JSON."""
        import json
        try:
            json.dumps(self.schema)
        except (TypeError, ValueError) as e:
            raise ValidationError({'schema': f'Invalid JSON schema: {e}'})


class BuilderAsset(models.Model):
    """Assets uploaded specifically for the page builder."""

    ASSET_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('icon', 'Icon'),
    )

    UPLOAD_SOURCES = (
        ('builder', 'Page Builder Upload'),
        ('direct', 'Direct URL Entry'),
        ('cloudinary', 'Cloudinary Upload'),
        ('unsplash', 'Unsplash Search'),
    )

    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    file = models.URLField(max_length=500, help_text="Cloudinary URL")
    original_filename = models.CharField(max_length=255, blank=True)

    # Metadata
    upload_source = models.CharField(max_length=20, choices=UPLOAD_SOURCES, default='builder')
    metadata = models.JSONField(default=dict, blank=True, help_text="Alt text, dimensions, etc.")

    # Ownership
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_builder_assets'
    )

    # Usage tracking
    used_in_pages = models.ManyToManyField(
        'marketing.Page',
        related_name='builder_assets',
        blank=True,
        help_text="Pages using this asset"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Builder Asset"
        verbose_name_plural = "Builder Assets"

    def __str__(self):
        return f"{self.asset_type}: {self.original_filename or self.file}"

    @property
    def alt_text(self):
        """Get alt text for image assets."""
        if self.metadata:
            return self.metadata.get('alt_text', '')
        return ''


class BuilderPageSettings(models.Model):
    """Additional settings for pages created with the builder."""

    page = models.OneToOneField(
        'marketing.Page',
        on_delete=models.CASCADE,
        related_name='builder_settings'
    )

    # Builder state
    builder_version = models.PositiveIntegerField(default=1)
    last_auto_save = models.DateTimeField(auto_now_add=True)

    # Canvas settings
    grid_enabled = models.BooleanField(default=True)
    snap_to_grid = models.BooleanField(default=True)
    grid_size = models.PositiveIntegerField(default=12, help_text="Grid size in pixels")

    # Viewport settings
    current_viewport = models.CharField(
        max_length=20,
        choices=[('desktop', 'Desktop'), ('tablet', 'Tablet'), ('mobile', 'Mobile')],
        default='desktop'
    )

    # Editor settings
    show_rulers = models.BooleanField(default=False)
    show_outlines = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Builder Page Settings"
        verbose_name_plural = "Builder Page Settings"

    def __str__(self):
        return f"Settings for {self.page.title}"


# Extend existing Page model with builder_data field
# Note: In production, this would be a migration that adds the field
# For now, we'll document it here
#
# Add to marketing.Page model:
#
# builder_data = models.JSONField(default=dict, blank=True, null=True, help_text="""
# {
#     "components": [
#         {
#             "id": "comp_123",
#             "type": "heading",
#             "position": {"x": 0, "y": 0, "w": 12, "h": 1},
#             "props": {
#                 "text": "Welcome",
#                 "level": "h1",
#                 "align": "center"
#             },
#             "styles": {
#                 "background": "#ffffff",
#                 "padding": "20px"
#             }
#         }
#     ],
#     "settings": {
#         "viewport": "desktop",
#         "breakpoints": {
#             "mobile": 768,
#             "tablet": 1024
#         }
#     },
#     "version": 1
# }
# """)
#
# builder_template = models.ForeignKey(
#     'BuilderTemplate',
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True,
#     related_name='pages',
#     help_text="Template used if page was created from template"
# )
