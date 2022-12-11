from django.db import models
import uuid
from django_tenants.models import TenantMixin
from django.contrib.auth.models import AbstractUser

# here is a Tenant model
class Company(TenantMixin):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

