from rest_framework import serializers
from .models import InitializePaymentModel, TransactionsModel

class InitializePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitializePaymentModel
        fields ="__all__"
        extra_kwargs = {'wallet_private_key': {'write_only': True}, 'wallet_public_key':{'write_only':True}}
        
class TransactionsModelSerializer(serializers.ModelSerializer):
    amount_to_pay = serializers.SerializerMethodField()
    class Meta:
        model = TransactionsModel
        fields ="__all__"
        # extra_kwargs = {'wallet_private_key': {'write_only': True}, 'wallet_public_key':{'write_only':True}}
    def get_amount_to_pay(self, obj):
        instance = InitializePaymentModel.objects.filter(transaction_reference=obj.transaction_reference).first()
        data = {
            "usd": instance.amount,
            "xrp": instance.xrp_amount,
            "eur": instance.eur,
            "jpy":instance.jpy
        }
        return data


        