"""
Cloudinary utilities for builder asset uploads.
"""

import os
import cloudinary
import cloudinary.uploader


def upload_image(file, folder='builder'):
    """
    Upload an image to Cloudinary.

    Args:
        file: Uploaded file object
        folder: Cloudinary folder name

    Returns:
        dict: {
            'url': Cloudinary URL,
            'secure_url': HTTPS URL,
            'public_id': Cloudinary public ID,
            'width': Image width,
            'height': Image height,
            'format': File format
        }
    """
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

    # Upload options
    upload_options = {
        'folder': folder,
        'resource_type': 'image',
        'transformation': [
            {'quality': 'auto', 'fetch_format': 'auto'}
        ]
    }

    try:
        result = cloudinary.uploader.upload_image(
            file,
            **upload_options
        )

        return {
            'url': result.get('url'),
            'secure_url': result.get('secure_url'),
            'public_id': result.get('public_id'),
            'width': result.get('width'),
            'height': result.get('height'),
            'format': result.get('format'),
        }
    except Exception as e:
        raise Exception(f"Cloudinary upload failed: {e}")


def get_upload_signature(folder='builder', public_id=None):
    """
    Generate upload signature for direct Cloudinary uploads from browser.

    Args:
        folder: Cloudinary folder name
        public_id: Optional public ID for the upload

    Returns:
        dict: {
            'signature': Cloudinary signature,
            'timestamp': Upload timestamp,
            'api_key': Cloudinary API key,
            'cloud_name': Cloudinary cloud name
        }
    """
    import time

    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

    timestamp = int(time.time())

    params = {
        'timestamp': timestamp,
        'folder': folder,
        'transformation': '{"quality": "auto", "fetch_format": "auto"}'
    }

    if public_id:
        params['public_id'] = public_id

    signature = cloudinary.utils.api_sign_request(
        params,
        os.getenv('CLOUDINARY_API_SECRET')
    )

    return {
        'signature': signature,
        'timestamp': timestamp,
        'api_key': os.getenv('CLOUDINARY_API_KEY'),
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'folder': folder,
        'public_id': public_id
    }
