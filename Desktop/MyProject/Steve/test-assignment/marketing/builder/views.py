"""
API views for page builder.
Handles builder CRUD operations, publishing, templates, and assets.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from marketing.models import Page
from .models import BuilderTemplate, ComponentRegistry, BuilderAsset, BuilderPageSettings
from .serializers import (
    BuilderPageSerializer,
    BuilderPageUpdateSerializer,
    PublishPageSerializer,
    BuilderTemplateSerializer,
    ComponentRegistrySerializer,
    BuilderAssetSerializer
)
from .permissions import CanUseBuilder, CanPublishPages
from .file_utils import upload_file_local


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanUseBuilder])
def get_builder_page(request, page_id):
    """
    Get page with builder data.
    GET /api/builder/pages/{id}/
    """
    page = get_object_or_404(Page, id=page_id)

    # Ensure user has access
    if not can_use_builder(request.user):
        return Response(
            {'error': 'You do not have permission to use the builder'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Create or get builder settings
    builder_settings, created = BuilderPageSettings.objects.get_or_create(page=page)

    serializer = BuilderPageSerializer(page)
    return Response({
        'success': True,
        'page': serializer.data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanUseBuilder])
def update_builder_page(request, page_id):
    """
    Update page builder data.
    PUT /api/builder/pages/{id}/
    """
    page = get_object_or_404(Page, id=page_id)

    # Ensure user has access
    if not can_use_builder(request.user):
        return Response(
            {'error': 'You do not have permission to use the builder'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Validate and update builder data
    serializer = BuilderPageUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update page
    page.builder_data = serializer.validated_data['builder_data']
    page.save()

    return Response({
        'success': True,
        'page_id': page.id,
        'message': 'Page builder data updated'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, CanPublishPages])
def publish_builder_page(request, page_id):
    """
    Publish a page created with the builder.
    POST /api/builder/pages/{id}/publish/
    """
    page = get_object_or_404(Page, id=page_id)

    # Validate user can publish
    if not can_publish_pages(request.user):
        return Response(
            {'error': 'You do not have permission to publish pages'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Validate slug
    serializer = PublishPageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    slug = serializer.validated_data['slug']

    # Update page
    page.slug = slug
    page.status = 'published'
    page.save()

    # Generate URL
    url = f'/{slug}/'

    return Response({
        'success': True,
        'url': url,
        'page_id': page.id,
        'message': 'Page published successfully'
    })


@api_view(['GET'])
def get_component_registry(request):
    """
    Get available components for the builder.
    GET /api/builder/components/

    Public endpoint - returns metadata about available builder components.
    """
    # Get enabled components ordered by display order
    components = ComponentRegistry.objects.filter(
        is_enabled=True
    ).order_by('order', 'name')

    serializer = ComponentRegistrySerializer(components, many=True)
    return Response({
        'success': True,
        'components': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanUseBuilder])
def get_builder_templates(request):
    """
    Get available page templates.
    GET /api/builder/templates/
    """
    # Ensure user has access
    if not can_use_builder(request.user):
        return Response(
            {'error': 'You do not have permission to use the builder'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Get public templates or all templates for staff
    if request.user.is_staff:
        templates = BuilderTemplate.objects.filter(is_active=True)
    else:
        templates = BuilderTemplate.objects.filter(
            is_active=True,
            is_public=True
        )

    serializer = BuilderTemplateSerializer(templates, many=True)
    return Response({
        'success': True,
        'templates': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, CanUseBuilder])
def upload_builder_asset(request):
    """
    Upload asset to Cloudinary through the builder.
    POST /api/builder/assets/upload/
    """
    from .cloudinary_utils import upload_image

    # Ensure user has access
    if not can_use_builder(request.user):
        return Response(
            {'error': 'You do not have permission to upload assets'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Check for file in request
    if 'file' not in request.FILES:
        return Response({
            'success': False,
            'error': 'No file provided'
        }, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    asset_type = request.POST.get('asset_type', 'image')

    # Upload to local storage
    try:
        result = upload_file_local(file, folder='builder', optimize=True)
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create asset record
    asset = BuilderAsset.objects.create(
        asset_type=asset_type,
        file=result['url'],
        original_filename=file.name,
        metadata={
            'width': result.get('width'),
            'height': result.get('height'),
            'format': result.get('format'),
            'alt_text': request.POST.get('alt_text', ''),
        },
        upload_source='builder',
        uploaded_by=request.user
    )

    serializer = BuilderAssetSerializer(asset)
    return Response({
        'success': True,
        'asset': serializer.data,
        'message': 'Asset uploaded successfully'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanUseBuilder])
def get_user_assets(request):
    """
    Get assets uploaded by current user.
    GET /api/builder/assets/
    """
    # Ensure user has access
    if not can_use_builder(request.user):
        return Response(
            {'error': 'You do not have permission to use the builder'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Get user's assets, most recent first
    assets = BuilderAsset.objects.filter(
        uploaded_by=request.user
    ).order_by('-created_at')[:50]

    serializer = BuilderAssetSerializer(assets, many=True)
    return Response({
        'success': True,
        'assets': serializer.data
    })
