from django.contrib import admin
from .models import InitializePaymentModel, TransactionsModel,WithdrawalModel

# Register your models here.
admin.site.register(InitializePaymentModel)
admin.site.register(WithdrawalModel)
admin.site.register(TransactionsModel)