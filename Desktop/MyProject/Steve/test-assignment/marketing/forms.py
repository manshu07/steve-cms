from django import forms

from .models import Page, Post, NavMenu, Footer


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'status', 'publish_at', 'unpublish_at',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image',
            'body_json', 'blocks_json',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # body_json is kept in the form for backward compat but hidden;
        # all content now lives in blocks_json via rich_text blocks.
        self.fields['body_json'].required = False
        self.fields['body_json'].widget = forms.HiddenInput()
        # Hide the URL input for primary_image - the custom upload widget handles file uploads
        self.fields['primary_image'].widget = forms.HiddenInput()
        # Add data-blocks-input attribute for the block builder JavaScript
        self.fields['blocks_json'].widget = forms.HiddenInput(attrs={'data-blocks-input': ''})


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'cover_image',
            'categories', 'tags', 'body_json', 'blocks_json',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_json'].required = False
        self.fields['body_json'].widget = forms.HiddenInput()
        # Hide the URL inputs for cover_image and primary_image - the custom upload widget handles file uploads
        self.fields['cover_image'].widget = forms.HiddenInput()
        self.fields['primary_image'].widget = forms.HiddenInput()
        # Add data-blocks-input attribute for the block builder JavaScript
        self.fields['blocks_json'].widget = forms.HiddenInput(attrs={'data-blocks-input': ''})


class NavMenuForm(forms.ModelForm):
    class Meta:
        model = NavMenu
        fields = ['name', 'items_json', 'header_buttons_json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.HiddenInput()
        if not self.instance or not self.instance.name:
            self.initial['name'] = 'Primary'
        # Hide the JSON fields - will be managed by JavaScript
        self.fields['items_json'].widget = forms.HiddenInput()
        self.fields['header_buttons_json'].widget = forms.HiddenInput(attrs={'data-header-buttons-input': ''})


class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = [
            'label', 'columns_json', 'cta_title', 'cta_body',
            'cta_button_label', 'cta_button_url', 'legal_text',
        ]
