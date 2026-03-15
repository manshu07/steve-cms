from django.contrib import admin
from .models import Page, Post, Category, Tag, NavMenu, NavItem, Footer, MediaAsset


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'publish_at', 'is_published']
    list_filter = ['status', 'publish_at']
    search_fields = ['title', 'slug']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'publish_at', 'is_published']
    list_filter = ['status', 'publish_at', 'categories']
    search_fields = ['title', 'slug']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NavMenu)
class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['label']


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'file', 'created_at']
    search_fields = ['alt_text', 'caption']
