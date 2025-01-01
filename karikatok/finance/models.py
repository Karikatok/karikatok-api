from django.contrib.auth import get_user_model


User = get_user_model()

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    account_reference = models.CharField(max_length=100, unique=True)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(
        max_length=20, 
        unique=True, 
        validators=[RegexValidator(r'^\d{10}$', "Account number must be 10 digits.")]
    )
    bank_name = models.CharField(max_length=100, null=True, blank=True, default="Unknown Bank")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} - {self.account_number}"
