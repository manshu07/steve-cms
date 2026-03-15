###############################################################################
# Local File Storage Utilities for Page Builder
# Handles file uploads locally instead of Cloudinary
###############################################################################

import os
import uuid
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io


def get_upload_path(folder='builder', filename=None):
    """
    Generate upload path with date-based folder structure.

    Args:
        folder: Base folder name (e.g., 'builder', 'assets')
        filename: Optional filename to append

    Returns:
        Full path relative to MEDIA_ROOT
    """
    date_path = datetime.now().strftime('%Y/%m/%d')
    path_parts = [folder, date_path]

    if filename:
        path_parts.append(filename)

    return os.path.join(*path_parts)


def generate_unique_filename(original_filename):
    """
    Generate unique filename while preserving extension.

    Args:
        original_filename: Original uploaded filename

    Returns:
        Unique filename with same extension
    """
    name, ext = os.path.splitext(original_filename)
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{unique_id}{ext}"


def validate_image_file(file):
    """
    Validate uploaded image file.

    Args:
        file: Uploaded file object

    Returns:
        tuple: (is_valid, error_message)

    Raises:
        ValueError: If file is invalid
    """
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValueError(f"File too large. Maximum size is 10MB")

    # Check file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    name, ext = os.path.splitext(file.name.lower())

    if ext not in valid_extensions:
        raise ValueError(f"Invalid file type. Allowed types: {', '.join(valid_extensions)}")

    return True, None


def process_image(file, max_width=1920, max_height=1080, quality=85):
    """
    Process and optimize image.

    Args:
        file: Uploaded file object
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)

    Returns:
        Processed image file
    """
    # Open image
    img = Image.open(file)

    # Convert to RGB if necessary (for JPEG compatibility)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize while maintaining aspect ratio
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # Save to buffer
    buffer = io.BytesIO()
    img_format = 'JPEG' if file.name.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
    img.save(buffer, format=img_format, quality=quality, optimize=True)

    # Create new file from buffer
    buffer.seek(0)
    return ContentFile(buffer.read(), name=file.name)


def upload_file_local(file, folder='builder', optimize=True):
    """
    Upload file to local storage.

    Args:
        file: Uploaded file object
        folder: Base folder for uploads
        optimize: Whether to optimize images

    Returns:
        dict: Upload result with keys:
            - url: Public URL of uploaded file
            - path: Local file path
            - filename: Generated filename
            - size: File size in bytes
            - width: Image width (if image)
            - height: Image height (if image)
            - format: File format

    Raises:
        ValueError: If file validation fails
        Exception: If upload fails
    """
    try:
        # Validate image file
        validate_image_file(file)

        # Generate unique filename
        filename = generate_unique_filename(file.name)
        upload_path = get_upload_path(folder, filename)

        # Process image if requested and it's an image
        width, height = None, None
        file_format = os.path.splitext(file.name)[1][1:].upper()

        if optimize and file.content_type.startswith('image/'):
            processed_file = process_image(file)
            width, height = Image.open(processed_file).size
            saved_path = default_storage.save(upload_path, processed_file)
        else:
            saved_path = default_storage.save(upload_path, file)

            # Get dimensions for images
            if file.content_type.startswith('image/'):
                try:
                    with Image.open(file) as img:
                        width, height = img.size
                except:
                    pass

        # Get file URL
        url = default_storage.url(saved_path)

        # Get file size
        full_path = default_storage.path(saved_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
        else:
            size = file.size

        return {
            'url': url,
            'path': saved_path,
            'filename': filename,
            'size': size,
            'width': width,
            'height': height,
            'format': file_format
        }

    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")


def delete_file_local(file_path):
    """
    Delete file from local storage.

    Args:
        file_path: Path to file relative to MEDIA_ROOT

    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def get_file_stats():
    """
    Get statistics about uploaded files.

    Returns:
        dict: Statistics including total files, total size, etc.
    """
    media_root = Path(settings.MEDIA_ROOT)
    builder_dir = media_root / 'builder'

    if not builder_dir.exists():
        return {
            'total_files': 0,
            'total_size': 0,
            'total_size_mb': 0
        }

    total_files = 0
    total_size = 0

    for file_path in builder_dir.rglob('*'):
        if file_path.is_file():
            total_files += 1
            total_size += file_path.stat().st_size

    return {
        'total_files': total_files,
        'total_size': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2)
    }


def cleanup_old_files(days=30):
    """
    Clean up files older than specified days.

    Args:
        days: Delete files older than this many days

    Returns:
        int: Number of files deleted
    """
    media_root = Path(settings.MEDIA_ROOT)
    builder_dir = media_root / 'builder'

    if not builder_dir.exists():
        return 0

    deleted_count = 0
    cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

    for file_path in builder_dir.rglob('*'):
        if file_path.is_file():
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    return deleted_count
