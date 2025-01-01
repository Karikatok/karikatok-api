from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import datetime

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('outlet_manager', 'Outlet Manager'),
    )

    user_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, null=False, blank=False, default='Unknown')
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=False, blank=False, default='')  # No choices
    address = models.TextField(default='unknown address')
    date_created = models.DateTimeField(default=now, editable=False)
