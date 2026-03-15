"""
URL configuration for builder API endpoints.
"""

from django.urls import path
from . import views

app_name = 'builder'

urlpatterns = [
    # Page builder endpoints
    path('pages/<int:page_id>/', views.get_builder_page, name='get-page'),
    path('pages/<int:page_id>/update/', views.update_builder_page, name='update-page'),
    path('pages/<int:page_id>/publish/', views.publish_builder_page, name='publish-page'),

    # Component registry
    path('components/', views.get_component_registry, name='get-components'),

    # Templates
    path('templates/', views.get_builder_templates, name='get-templates'),

    # Assets
    path('assets/upload/', views.upload_builder_asset, name='upload-asset'),
    path('assets/', views.get_user_assets, name='get-assets'),
]
