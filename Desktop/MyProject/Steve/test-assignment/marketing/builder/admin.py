"""
Admin configuration for builder models.
"""

from django.contrib import admin
from .models import (
    BuilderTemplate,
    ComponentRegistry,
    BuilderAsset,
    BuilderPageSettings
)


@admin.register(BuilderTemplate)
class BuilderTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public', 'is_active', 'version', 'created_at']
    list_filter = ['is_public', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['version', 'created_at', 'updated_at']

    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description', 'thumbnail')
        }),
        ('Content', {
            'fields': ('builder_data',)
        }),
        ('Settings', {
            'fields': ('is_public', 'is_active', 'created_by')
        }),
        ('Metadata', {
            'fields': ('version', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['duplicate_template']

    def duplicate_template(self, request, queryset):
        """Duplicate selected templates."""
        count = 0
        for template in queryset:
            template.duplicate()
            count += 1
        self.message_user(request, f'{count} template(s) duplicated.')
    duplicate_template.short_description = "Duplicate selected templates"


@admin.register(ComponentRegistry)
class ComponentRegistryAdmin(admin.ModelAdmin):
    list_display = ['label', 'category', 'is_enabled', 'order']
    list_filter = ['category', 'is_enabled', 'requires_asset']
    search_fields = ['name', 'label']
    ordering = ['order', 'name']

    fieldsets = (
        ('Component Information', {
            'fields': ('name', 'label', 'category')
        }),
        ('Appearance', {
            'fields': ('icon', 'order')
        }),
        ('Component Schema', {
            'fields': ('schema', 'default_props')
        }),
        ('Features', {
            'fields': ('is_enabled', 'requires_asset', 'is_editable')
        }),
        ('Rendering', {
            'fields': ('render_component',)
        }),
    )


@admin.register(BuilderAsset)
class BuilderAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'original_filename', 'upload_source', 'uploaded_by', 'created_at']
    list_filter = ['asset_type', 'upload_source']
    search_fields = ['original_filename', 'file']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Asset Information', {
            'fields': ('asset_type', 'file', 'original_filename')
        }),
        ('Metadata', {
            'fields': ('metadata',)
        }),
        ('Source', {
            'fields': ('upload_source', 'uploaded_by')
        }),
        ('Usage', {
            'fields': ('used_in_pages',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BuilderPageSettings)
class BuilderPageSettingsAdmin(admin.ModelAdmin):
    list_display = ['page', 'builder_version', 'current_viewport', 'last_auto_save']
    list_filter = ['current_viewport', 'grid_enabled']
    readonly_fields = ['last_auto_save']

    fieldsets = (
        ('Page', {
            'fields': ('page',)
        }),
        ('Builder State', {
            'fields': ('builder_version', 'last_auto_save')
        }),
        ('Canvas Settings', {
            'fields': ('grid_enabled', 'snap_to_grid', 'grid_size')
        }),
        ('Viewport', {
            'fields': ('current_viewport',)
        }),
        ('Editor', {
            'fields': ('show_rulers', 'show_outlines')
        }),
    )
