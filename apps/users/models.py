from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
import uuid
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel



class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(verbose_name=_("is staff"), default=False)
    phone_number = models.CharField(max_length=120, unique=True, blank=True, null=True)
    business_name = models.CharField(max_length=120, unique=True, blank=True, null=True)
    business_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    api_key = models.CharField(max_length=255, unique=True, blank=True, null=True)
    api_key_expiration = models.DateField(blank=True, null=True)
    webhook = models.CharField(max_length=255, unique=True, blank=True, null=True)
    private_key = models.CharField(max_length=255, unique=True, blank=True, null=True)
    public_key= models.CharField(max_length=255, unique=True, blank=True, null=True)
    classic_address = models.CharField(max_length=255, unique=True, blank=True, null=True)
    xrp_balance =  models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_administrator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_activated = models.BooleanField(default=False)
   
  
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email