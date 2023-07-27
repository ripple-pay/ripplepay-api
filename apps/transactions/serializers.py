from rest_framework import serializers
from .models import InitializePaymentModel, TransactionsModel

class InitializePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitializePaymentModel
        fields ="__all__"
        extra_kwargs = {'wallet_private_key': {'write_only': True}, 'wallet_public_key':{'write_only':True}}
        
class TransactionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionsModel
        fields ="__all__"
        # extra_kwargs = {'wallet_private_key': {'write_only': True}, 'wallet_public_key':{'write_only':True}}


        