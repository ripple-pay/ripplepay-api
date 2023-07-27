from django.db import models
from apps.users.models import User
from apps.common.models import TimeStampedUUIDModel

# Create your models here.

# This model is stores generated wallets tied to an order transaction reference
class InitializePaymentModel(TimeStampedUUIDModel):
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_public_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_private_key = models.CharField(max_length=255, blank=True, null=True)
    business = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    xrp_amount = models.CharField(max_length=255, blank=True, null=True)
    customers_email = models.CharField(max_length=155, blank=True, null=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.business.email} || {self.amount} "
    

class TransactionsModel(TimeStampedUUIDModel):
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    business = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    xrp_amount = models.CharField(max_length=255, blank=True, null=True)
    customers_email = models.CharField(max_length=155, blank=True, null=True)
    def __str__(self):
        return f"{self.business.email} || {self.amount} "
    
    
    