# Django Authentication

## JWT Authentication

### Setup with SimpleJWT
```python
# config/settings/base.py
from datetime import timedelta

INSTALLED_APPS += ["rest_framework_simplejwt"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
```

### Token Views
```python
# apps/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
```

### Custom Token Claims
```python
# apps/users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add custom claims to JWT tokens."""
    
    @classmethod
    def get_token(cls, user) -> dict:
        token = super().get_token(user)
        
        # Add custom claims
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["first_name"] = user.first_name
        
        return token
    
    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        
        # Add user info to response
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        
        return data

# Custom view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

## User Registration

### Registration View
```python
# apps/users/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer

class RegisterView(APIView):
    """User registration endpoint."""
    
    permission_classes = [AllowAny]
    
    def post(self, request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password_confirm"]
    
    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match"
            })
        return attrs
    
    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)
```

## Logout with Token Blacklist

```python
# apps/users/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class LogoutView(APIView):
    """Logout by blacklisting refresh token."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request) -> Response:
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

# Add to settings
INSTALLED_APPS += ["rest_framework_simplejwt.token_blacklist"]
```

## Custom Authentication Backend

```python
# apps/users/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(BaseBackend):
    """Authenticate with email instead of username."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get("email")
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# Add to settings
AUTHENTICATION_BACKENDS = [
    "apps.users.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```

## Permissions

### Custom Permissions
```python
# apps/core/permissions.py
from rest_framework import permissions

class IsAuthenticatedAndActive(permissions.BasePermission):
    """User must be authenticated and active."""
    
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin can write, others can read."""
    
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwner(permissions.BasePermission):
    """Only owner can access."""
    
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user

class IsOwnerOrAdmin(permissions.BasePermission):
    """Owner or admin can access."""
    
    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.is_staff:
            return True
        return obj.user == request.user

class HasRole(permissions.BasePermission):
    """Check user has specific role."""
    
    role = None
    
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name=self.role).exists()
        )

class IsManager(HasRole):
    role = "Managers"
```

## Password Reset

### Using Django's Built-in Password Reset
```python
# apps/users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
```

### API-based Password Reset
```python
# apps/users/views.py
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class PasswordResetRequestView(APIView):
    """Request password reset email."""
    
    permission_classes = [AllowAny]
    
    def post(self, request) -> Response:
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
            # Send email with reset link
            from django.core.mail import send_mail
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            reset_url = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
            
            send_mail(
                "Password Reset",
                f"Click here to reset: {reset_url}",
                "noreply@example.com",
                [email],
            )
            
        except User.DoesNotExist:
            pass  # Don't reveal if user exists
        
        return Response({"message": "If email exists, reset link sent"})

class PasswordResetConfirmView(APIView):
    """Confirm password reset with token."""
    
    permission_classes = [AllowAny]
    
    def post(self, request) -> Response:
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        
        from django.utils.http import urlsafe_base64_decode
        
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"})
            
        except (User.DoesNotExist, ValueError):
            pass
        
        return Response(
            {"error": "Invalid reset link"},
            status=status.HTTP_400_BAD_REQUEST
        )
```

## Social Authentication

### Using django-allauth
```python
# config/settings/base.py
INSTALLED_APPS += [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
```

### Social Login Callback
```python
# apps/users/views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginView(APIView):
    """Google OAuth login."""
    
    permission_classes = [AllowAny]
    
    def post(self, request) -> Response:
        access_token = request.data.get("access_token")
        
        from allauth.socialaccount.providers.google.provider import GoogleProvider
        from allauth.socialaccount.helpers import complete_social_login
        
        # Verify with Google and get user info
        # ... implementation ...
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })