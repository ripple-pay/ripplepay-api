from django.contrib import admin
from .models import InitializePaymentModel, TransactionsModel

# Register your models here.
admin.site.register(InitializePaymentModel)
admin.site.register(TransactionsModel)