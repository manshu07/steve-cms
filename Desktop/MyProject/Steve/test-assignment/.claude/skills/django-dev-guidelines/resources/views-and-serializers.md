# Django Views and Serializers

## DRF Serializers

### ModelSerializer
```python
# apps/users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer with computed fields."""
    
    full_name = serializers.SerializerMethodField()
    orders_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone",
            "orders_count", "is_active", "created_at"
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value.lower()).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()
    
    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
```

### Nested Serializers
```python
# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    class Meta:
        model = Order
        fields = [
            "id", "user_email", "status", "status_display",
            "total_amount", "items", "created_at"
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ["user", "status", "total_amount", "items"]
    
    def create(self, validated_data: dict) -> Order:
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
```

### Dynamic Fields Serializer
```python
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """Serializer that allows dynamic field selection."""
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# Usage
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone"]

# In view
UserSerializer(user, fields=["id", "email"])
```

## DRF Views

### ViewSet
```python
# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """Order API ViewSet."""
    
    queryset = Order.objects.select_related("user").prefetch_related("items")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
    search_fields = ["user__email", "id"]
    ordering_fields = ["created_at", "total_amount"]
    ordering = ["-created_at"]
    
    def get_serializer_class(self) -> type[serializers.Serializer]:
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self) -> models.QuerySet[Order]:
        """Filter orders by user for non-admin users."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer) -> None:
        """Set user from request."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None) -> Response:
        """Cancel an order."""
        order = self.get_object()
        if order.status == Order.Status.CANCELLED:
            return Response(
                {"error": "Order already cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = Order.Status.CANCELLED
        order.save()
        return Response({"status": "cancelled"})
    
    @action(detail=False, methods=["get"])
    def my_orders(self, request) -> Response:
        """Get current user's orders."""
        orders = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(orders)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
```

### Generic Views
```python
from rest_framework import generics

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> models.QuerySet[Order]:
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> models.QuerySet[Order]:
        return Order.objects.filter(user=self.request.user)
```

### Function-Based Views
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def order_list_create(request) -> Response:
    """List orders or create new order."""
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def order_detail(request, pk: int) -> Response:
    """Retrieve, update or delete order."""
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## Permissions

### Custom Permissions
```python
# apps/core/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access only to owner or admin."""
    
    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.is_staff:
            return True
        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """Allow access only to owner."""
    
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user

# Usage in view
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
```

## Filtering

### Django Filter
```python
# apps/orders/filters.py
import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=Order.Status.choices,
    )
    min_amount = django_filters.NumberFilter(
        field_name="total_amount",
        lookup_expr="gte",
    )
    max_amount = django_filters.NumberFilter(
        field_name="total_amount",
        lookup_expr="lte",
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    search = django_filters.CharFilter(
        method="filter_search",
    )
    
    class Meta:
        model = Order
        fields = ["status", "user"]
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) | Q(user__email__icontains=value)
        )

# In view
class OrderViewSet(viewsets.ModelViewSet):
    filterset_class = OrderFilter
```

## Pagination

### Custom Pagination
```python
# config/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    
    def get_paginated_response(self, data) -> Response:
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

# In settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "config.pagination.StandardPagination",
    "PAGE_SIZE": 20,
}
```

## URL Routing

### Router Configuration
```python
# apps/orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]

# For nested routes (using drf-nested-routers)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

users_router = routers.NestedDefaultRouter(
    router, r"users", lookup="user"
)
users_router.register(r"orders", OrderViewSet, basename="user-orders")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(users_router.urls)),
]