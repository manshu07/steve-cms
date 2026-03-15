from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def cms_admin_required(view_func):
    """Decorator requiring user to be logged in and in the 'CMS Admins' group."""
    @login_required
    def _wrapped(request, *args, **kwargs):
        if request.user.groups.filter(name='CMS Admins').exists():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied('CMS access restricted')

    return _wrapped
