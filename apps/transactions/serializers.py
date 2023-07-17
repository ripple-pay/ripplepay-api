from rest_framework import serializers
from .models import InitializePaymentModel

class InitializePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitializePaymentModel
        fields ="__all__"