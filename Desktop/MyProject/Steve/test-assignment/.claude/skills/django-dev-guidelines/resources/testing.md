# Django Testing

## pytest-django Setup

### Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --reuse-db"
testpaths = ["tests"]

[tool.coverage.run]
source = ["apps"]
branch = true
omit = ["*/migrations/*", "*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
```

### Test Settings
```python
# config/settings/testing.py
from .base import *

DEBUG = True
SECRET_KEY = "test-secret-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Faster password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging in tests
LOGGING = {}
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py
├── factories.py
├── unit/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_serializers.py
└── integration/
    ├── __init__.py
    └── test_api.py
```

## Fixtures

### conftest.py
```python
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated API client."""
    return APIClient()

@pytest.fixture
def authenticated_client(user) -> APIClient:
    """Authenticated API client."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(admin_user) -> APIClient:
    """Admin API client."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="test@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="User",
    )

@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpassword123",
    )

@pytest.fixture
def order(user):
    """Create a test order."""
    from apps.orders.models import Order
    return Order.objects.create(
        user=user,
        status=Order.Status.PENDING,
        total_amount=100.00,
    )
```

## Model Tests

```python
# tests/unit/test_models.py
import pytest
from django.core.exceptions import ValidationError

from apps.orders.models import Order

class TestOrderModel:
    """Tests for Order model."""
    
    def test_create_order(self, user):
        """Test order creation."""
        order = Order.objects.create(
            user=user,
            status=Order.Status.PENDING,
            total_amount=100.00,
        )
        
        assert order.id is not None
        assert order.status == Order.Status.PENDING
        assert order.total_amount == 100.00
        assert order.created_at is not None
    
    def test_order_str(self, order):
        """Test order string representation."""
        assert str(order) == f"Order {order.id} - {order.status}"
    
    def test_order_default_status(self, user):
        """Test order default status is pending."""
        order = Order.objects.create(user=user, total_amount=50.00)
        assert order.status == Order.Status.PENDING
    
    def test_order_clean_validates_negative_amount(self, user):
        """Test negative amount validation."""
        order = Order(
            user=user,
            total_amount=-10.00,
        )
        
        with pytest.raises(ValidationError):
            order.full_clean()
    
    @pytest.mark.parametrize("status", [
        Order.Status.PENDING,
        Order.Status.CONFIRMED,
        Order.Status.SHIPPED,
    ])
    def test_order_status_transitions(self, order, status):
        """Test valid status values."""
        order.status = status
        order.save()
        order.refresh_from_db()
        assert order.status == status
```

## API Tests

```python
# tests/integration/test_api.py
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.models import Order

class TestOrderAPI:
    """Tests for Order API endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client):
        self.client = authenticated_client
    
    def test_list_orders(self, order):
        """Test listing orders."""
        response = self.client.get("/api/v1/orders/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == order.id
    
    def test_create_order(self, user):
        """Test creating an order."""
        data = {
            "status": "pending",
            "total_amount": "150.00",
            "items": [
                {
                    "product_name": "Product 1",
                    "quantity": 2,
                    "price": "50.00",
                }
            ]
        }
        
        response = self.client.post("/api/v1/orders/", data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["total_amount"] == "150.00"
        assert Order.objects.count() == 1
    
    def test_get_order_detail(self, order):
        """Test getting order detail."""
        response = self.client.get(f"/api/v1/orders/{order.id}/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == order.id
    
    def test_get_order_not_found(self):
        """Test getting non-existent order."""
        response = self.client.get("/api/v1/orders/999/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_order(self, order):
        """Test updating an order."""
        data = {"status": "confirmed"}
        
        response = self.client.patch(
            f"/api/v1/orders/{order.id}/",
            data,
            format="json"
        )
        
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == "confirmed"
    
    def test_delete_order(self, order):
        """Test deleting an order."""
        response = self.client.delete(f"/api/v1/orders/{order.id}/")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.count() == 0
    
    def test_cancel_order_action(self, order):
        """Test custom cancel action."""
        response = self.client.post(f"/api/v1/orders/{order.id}/cancel/")
        
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == Order.Status.CANCELLED
    
    def test_unauthenticated_access(self):
        """Test unauthenticated access denied."""
        client = APIClient()
        response = client.get("/api/v1/orders/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_other_user_order_access_denied(self, order, db):
        """Test user cannot access other user's order."""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="password123",
        )
        client = APIClient()
        client.force_authenticate(user=other_user)
        
        response = client.get(f"/api/v1/orders/{order.id}/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
```

## Serializer Tests

```python
# tests/unit/test_serializers.py
import pytest
from apps.users.serializers import UserSerializer, UserRegistrationSerializer

class TestUserSerializer:
    """Tests for UserSerializer."""
    
    def test_serialize_user(self, user):
        """Test user serialization."""
        serializer = UserSerializer(user)
        
        assert serializer.data["id"] == user.id
        assert serializer.data["email"] == user.email
        assert "password" not in serializer.data
    
    def test_full_name_computed_field(self, user):
        """Test full_name computed field."""
        serializer = UserSerializer(user)
        
        expected = f"{user.first_name} {user.last_name}"
        assert serializer.data["full_name"] == expected

class TestUserRegistrationSerializer:
    """Tests for UserRegistrationSerializer."""
    
    def test_valid_registration(self):
        """Test valid registration data."""
        data = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        }
        
        serializer = UserRegistrationSerializer(data=data)
        
        assert serializer.is_valid(), serializer.errors
    
    def test_password_mismatch(self):
        """Test password confirmation validation."""
        data = {
            "email": "new@example.com",
            "password": "password123",
            "password_confirm": "different123",
        }
        
        serializer = UserRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert "password_confirm" in serializer.errors
    
    @pytest.mark.django_db
    def test_duplicate_email(self, user):
        """Test duplicate email validation."""
        data = {
            "email": user.email,  # Existing email
            "password": "password123",
            "password_confirm": "password123",
        }
        
        serializer = UserRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert "email" in serializer.errors
```

## Factory Boy

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["email"]
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    
    @classmethod
    def create_user(cls, password: str = "password123", **kwargs):
        user = cls(**kwargs)
        user.set_password(password)
        user.save()
        return user

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    status = Order.Status.PENDING
    total_amount = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem
    
    order = factory.SubFactory(OrderFactory)
    product_name = factory.Faker("sentence", nb_words=3)
    quantity = factory.Faker("random_int", min=1, max=10)
    price = factory.Faker(
        "pydecimal",
        left_digits=2,
        right_digits=2,
        positive=True,
    )

# Usage in tests
def test_with_factory(db):
    order = OrderFactory()
    assert order.id is not None
    
    orders = OrderFactory.create_batch(5)
    assert len(orders) == 5
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test class
pytest tests/unit/test_models.py::TestOrderModel

# Run specific test
pytest tests/unit/test_models.py::TestOrderModel::test_create_order

# Run tests matching pattern
pytest -k "order"

# Run tests in parallel
pytest -n auto

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Verbose output
pytest -vv

# Stop on first failure
pytest -x