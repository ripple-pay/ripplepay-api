from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('initialize-payment', initialize_payment, name="initialize-payment"),
    path("payment/tx-ref=<str:ref>", transactionsview, name="transactions-view")
    
    
]
