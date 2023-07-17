
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
  
    path('register-business', business, name="register-business"),
    path('business', business, name="business-info"),
  
    
    
]
