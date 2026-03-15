"""
URL configuration for marketing app.
Includes all public and CMS admin URLs.
"""

from django.urls import path, include

from . import views
from . import cms_views


urlpatterns = [
    # Public URLs
    path('', views.marketing_home, name='marketing-home'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots-txt'),
    path('blog/', views.blog_index, name='marketing-blog-index'),
    path('blog/<slug:slug>/', views.blog_post_detail, name='marketing-blog-post'),

    # Page Builder API
    path('api/builder/', include('marketing.builder.urls')),

    # CMS Admin URLs
    path('cms/', cms_views.dashboard, name='cms-dashboard'),
    path('cms/pages/', cms_views.page_list, name='cms-page-list'),
    path('cms/pages/new/', cms_views.page_create, name='cms-page-create'),
    path('cms/pages/<int:page_id>/', cms_views.page_edit, name='cms-page-edit'),
    path('cms/pages/<int:page_id>/delete/', cms_views.page_delete, name='cms-page-delete'),
    path('cms/pages/<int:page_id>/toggle-status/', cms_views.page_toggle_status, name='cms-page-toggle-status'),
    path('cms/posts/', cms_views.post_list, name='cms-post-list'),
    path('cms/posts/new/', cms_views.post_create, name='cms-post-create'),
    path('cms/posts/<int:post_id>/', cms_views.post_edit, name='cms-post-edit'),
    path('cms/posts/<int:post_id>/delete/', cms_views.post_delete, name='cms-post-delete'),
    path('cms/posts/<int:post_id>/toggle-status/', cms_views.post_toggle_status, name='cms-post-toggle-status'),
    path('cms/navigation/', cms_views.navigation_edit, name='cms-navigation'),
    path('cms/upload/', cms_views.upload_image, name='cms-upload-image'),

    # Catch-all page detail MUST BE LAST
    path('<slug:slug>/', views.page_detail, name='marketing-page-detail'),
]
