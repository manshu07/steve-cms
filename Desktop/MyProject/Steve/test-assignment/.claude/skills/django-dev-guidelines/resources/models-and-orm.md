# Django Models and ORM

## Model Design Patterns

### Base Model with Timestamps
```python
# apps/core/models.py
from django.db import models

class TimestampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

### Model with Soft Delete
```python
# apps/core/models.py
from django.db import models
from django.utils import timezone

class SoftDeleteModel(models.Model):
    """Model with soft delete capability."""
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False) -> None:
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
    
    def hard_delete(self, using=None, keep_parents=False) -> tuple:
        return super().delete(using, using, keep_parents)
    
    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

# Manager for soft delete
class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Include deleted
    
    class Meta:
        abstract = True
```

### Complete Model Example
```python
# apps/orders/models.py
from django.db import models
from django.conf import settings
from apps.core.models import TimestampedModel

class Order(TimestampedModel):
    """Customer order model."""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user", "status"]),
        ]
    
    def __str__(self) -> str:
        return f"Order {self.id} - {self.status}"
    
    @property
    def item_count(self) -> int:
        return self.items.count()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = "order_items"
    
    def __str__(self) -> str:
        return f"{self.quantity}x {self.product_name}"
```

## QuerySet Patterns

### Custom QuerySet
```python
# apps/orders/models.py
from django.db import models

class OrderQuerySet(models.QuerySet):
    def pending(self) -> "OrderQuerySet":
        return self.filter(status=Order.Status.PENDING)
    
    def for_user(self, user) -> "OrderQuerySet":
        return self.filter(user=user)
    
    def recent(self, days: int = 7) -> "OrderQuerySet":
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
    
    def with_total_items(self) -> "OrderQuerySet":
        return self.annotate(
            total_items=models.Sum("items__quantity")
        )

class Order(models.Model):
    # ... fields ...
    
    objects = OrderQuerySet.as_manager()

# Usage
pending_orders = Order.objects.pending().for_user(request.user)
recent_orders = Order.objects.recent(days=30).with_total_items()
```

### Complex Queries
```python
from django.db.models import Q, F, Count, Sum, Avg, Case, When, Value

# Complex filter with Q objects
orders = Order.objects.filter(
    Q(status="pending") | Q(status="confirmed"),
    created_at__gte=start_date,
)

# Annotations
orders = Order.objects.annotate(
    item_count=Count("items"),
    total_quantity=Sum("items__quantity"),
    avg_item_price=Avg("items__price"),
)

# Conditional expressions
orders = Order.objects.annotate(
    is_large=Case(
        When(total_amount__gt=1000, then=Value(True)),
        default=Value(False),
        output_field=models.BooleanField(),
    )
)

# Using F for field references
Order.objects.filter(
    total_amount__gt=F("discount_amount") * 2
)

# Select related (foreign key)
Order.objects.select_related("user").all()

# Prefetch related (reverse foreign key, m2m)
Order.objects.prefetch_related("items").all()

# Combined
Order.objects.select_related(
    "user"
).prefetch_related(
    Prefetch("items", queryset=OrderItem.objects.select_related("product"))
)
```

## Migrations

### Custom Migration
```python
# apps/orders/migrations/0002_add_status_index.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]
    
    operations = [
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["status"], name="order_status_idx"),
        ),
    ]
```

### Data Migration
```python
# apps/users/migrations/0003_populate_initial_data.py
from django.db import migrations

def create_initial_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create([
        Group(name="Admins"),
        Group(name="Managers"),
        Group(name="Editors"),
    ])

class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_options"),
    ]
    
    operations = [
        migrations.RunPython(create_initial_groups),
    ]
```

## Model Validation

### Clean Method
```python
from django.core.exceptions import ValidationError

class Order(models.Model):
    # ... fields ...
    
    def clean(self) -> None:
        if self.total_amount < 0:
            raise ValidationError({"total_amount": "Amount cannot be negative"})
        
        if self.status == "cancelled" and self.items.exists():
            raise ValidationError("Cannot cancel order with items")
    
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)
```

### Custom Validators
```python
from django.core.validators import RegexValidator, MinValueValidator

phone_validator = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be 9-15 digits with optional country code.",
)

class User(models.Model):
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )
```

## Signals

### Order Signals
```python
# apps/orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """Send confirmation email when order is created."""
    if created:
        from apps.orders.tasks import send_confirmation_email
        send_confirmation_email.delay(instance.id)

@receiver(post_save, sender=Order)
def update_user_order_count(sender, instance, created, **kwargs):
    """Update user's order count cache."""
    if created:
        instance.user.order_count = instance.user.orders.count()
        instance.user.save(update_fields=["order_count"])
```

## Admin Configuration

### ModelAdmin
```python
# apps/orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_amount", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__email", "id"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [OrderItemInline]
    
    fieldsets = (
        ("Order Info", {
            "fields": ("user", "status", "total_amount")
        }),
        ("Details", {
            "fields": ("notes", "created_at", "updated_at")
        }),
    )
    
    actions = ["mark_as_shipped"]
    
    @admin.action(description="Mark selected orders as shipped")
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status=Order.Status.SHIPPED)
        self.message_user(request, f"{updated} orders marked as shipped.")