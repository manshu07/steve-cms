"""
Cloudinary image upload utilities.

Handles uploading images to Cloudinary and returning the URL.
All CMS images are stored on Cloudinary and referenced via URLField.
"""

import cloudinary
import cloudinary.uploader
from django.conf import settings


def _configure():
    """Ensure cloudinary is configured from Django settings."""
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


def upload_image(file, folder='cms', public_id=None):
    """
    Upload an image file to Cloudinary.

    Args:
        file: A file-like object (e.g. request.FILES['image']) or a file path string.
        folder: Cloudinary folder to upload into.
        public_id: Optional public_id override.

    Returns:
        dict with 'url', 'secure_url', 'public_id', 'width', 'height'.
    """
    _configure()
    options = {
        'folder': folder,
        'resource_type': 'image',
        'overwrite': True,
        'quality': 'auto',
        'fetch_format': 'auto',
    }
    if public_id:
        options['public_id'] = public_id

    result = cloudinary.uploader.upload(file, **options)
    return {
        'url': result.get('url'),
        'secure_url': result.get('secure_url'),
        'public_id': result.get('public_id'),
        'width': result.get('width'),
        'height': result.get('height'),
    }
