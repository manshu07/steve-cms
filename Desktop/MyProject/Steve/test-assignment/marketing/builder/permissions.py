"""
Permissions for page builder.
"""

from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


def can_use_builder(user):
    """Check if user has permission to use the page builder."""
    if not user.is_authenticated:
        return False
    return user.is_staff or user.has_perm('marketing.can_use_builder')


def can_publish_pages(user):
    """Check if user has permission to publish pages."""
    if not user.is_authenticated:
        return False
    return user.is_staff or user.has_perm('marketing.can_publish_pages')


def can_create_templates(user):
    """Check if user can create page templates."""
    if not user.is_authenticated:
        return False
    return user.is_staff or user.has_perm('marketing.can_create_templates')


def can_upload_assets(user):
    """Check if user can upload assets."""
    if not user.is_authenticated:
        return False
    return user.is_staff or user.has_perm('marketing.can_upload_assets')


class CanUseBuilder(permissions.BasePermission):
    """Permission class for checking if user can use the builder."""

    def has_permission(self, request, view):
        return can_use_builder(request.user)


class CanPublishPages(permissions.BasePermission):
    """Permission class for checking if user can publish pages."""

    def has_permission(self, request, view):
        return can_publish_pages(request.user)


class CanCreateTemplates(permissions.BasePermission):
    """Permission class for checking if user can create templates."""

    def has_permission(self, request, view):
        return can_create_templates(request.user)


class CanUploadAssets(permissions.BasePermission):
    """Permission class for checking if user can upload assets."""

    def has_permission(self, request, view):
        return can_upload_assets(request.user)
