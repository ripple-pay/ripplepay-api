
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
  
    path('register-business', business, name="register-business"),
    path('balance-customers-count', balance_customer_count, name="balance-customers-count"),
    path('login', login_view, name="login"),
    path('activate-account', activate_account, name="activate_account"),
  
    
    
]
