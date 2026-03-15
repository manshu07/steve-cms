"""
Serializers for builder API endpoints.
"""

from rest_framework import serializers
from .models import BuilderTemplate, ComponentRegistry, BuilderAsset
from marketing.models import Page


class ComponentRegistrySerializer(serializers.ModelSerializer):
    """Serializer for component registry."""

    class Meta:
        model = ComponentRegistry
        fields = [
            'id', 'name', 'label', 'category', 'icon',
            'schema', 'default_props', 'is_enabled',
            'requires_asset', 'is_editable', 'render_component', 'order'
        ]


class BuilderAssetSerializer(serializers.ModelSerializer):
    """Serializer for builder assets."""

    class Meta:
        model = BuilderAsset
        fields = [
            'id', 'asset_type', 'file', 'original_filename',
            'metadata', 'upload_source', 'created_at'
        ]
        read_only_fields = ['created_at']


class BuilderTemplateSerializer(serializers.ModelSerializer):
    """Serializer for builder templates."""

    class Meta:
        model = BuilderTemplate
        fields = [
            'id', 'name', 'description', 'thumbnail',
            'builder_data', 'is_public', 'version', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'version']


class BuilderPageSerializer(serializers.ModelSerializer):
    """Serializer for pages with builder data."""

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'status', 'builder_data',
            'builder_template', 'updated_at', 'created_at'
        ]
        read_only_fields = ['updated_at', 'created_at']

    def to_representation(self, instance):
        """Add builder_settings to representation."""
        data = super().to_representation(instance)
        # Add builder settings if they exist
        if hasattr(instance, 'builder_settings'):
            data['builder_settings'] = {
                'grid_enabled': instance.builder_settings.grid_enabled,
                'snap_to_grid': instance.builder_settings.snap_to_grid,
                'current_viewport': instance.builder_settings.current_viewport,
            }
        return data


class BuilderPageUpdateSerializer(serializers.Serializer):
    """Serializer for updating page builder data."""

    builder_data = serializers.JSONField(help_text="Builder component data")

    def validate_builder_data(self, value):
        """Validate builder data structure and content."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("builder_data must be a JSON object")

        # Check if components key exists
        if 'components' not in value:
            raise serializers.ValidationError("builder_data must contain 'components' key")

        components = value['components']

        # Validate it's a list
        if not isinstance(components, list):
            raise serializers.ValidationError("'components' must be a list")

        # Check component count limit
        if len(components) > 100:
            raise serializers.ValidationError("Cannot have more than 100 components per page")

        # Validate each component
        for component in components:
            if not isinstance(component, dict):
                raise serializers.ValidationError("Each component must be a JSON object")

            # Check required fields
            required_fields = ['id', 'type', 'position', 'props', 'styles']
            for field in required_fields:
                if field not in component:
                    raise serializers.ValidationError(f"Component missing required field: {field}")

            # Validate component type is registered
            component_type = component['type']
            if not ComponentRegistry.objects.filter(
                name=component_type,
                is_enabled=True
            ).exists():
                raise serializers.ValidationError(
                    f"Invalid component type: {component_type}"
                )

            # Validate position
            position = component['position']
            if not all(key in position for key in ['x', 'y', 'w', 'h']):
                raise serializers.ValidationError(
                    f"Component position must contain x, y, w, h coordinates"
                )

        return value


class PublishPageSerializer(serializers.Serializer):
    """Serializer for publishing a page."""

    slug = serializers.SlugField(
        max_length=100,
        help_text="URL slug for published page"
    )

    def validate_slug(self, value):
        """Validate slug is not already in use by another published page."""
        # Check if slug is already used by a published page
        existing_pages = Page.objects.filter(
            slug=value,
            status='published'
        ).exclude(status='draft')

        if existing_pages.exists():
            raise serializers.ValidationError(
                f"A page with slug '{value}' is already published. "
                "Choose a different slug."
            )

        return value
