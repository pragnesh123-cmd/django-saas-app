from django.db import models
from apps.tenant.models import Company


# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.CharField(max_length=256)
    is_deleted = models.BooleanField(default=False)
    