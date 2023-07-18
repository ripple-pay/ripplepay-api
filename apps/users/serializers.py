from rest_framework import serializers
from .models import User


class RegisterBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only':True}, 
            'user_permissions': {'read_only':True},
            'is_superuser': {'read_only':True},
            'last_login': {'write_only':True},
            'api-key': {'read_only':True},
            "private_key": {'read_only':True} ,
            "public_key": {'read_only':True} ,
            "classic_address": {'read_only':True} ,
            "api_key": {'read_only':True} ,
            "business_id": {'read_only':True} ,
            "api_key_expiration": {'read_only':True} ,
            "is_administrator": {'read_only':True} ,
            "xrp_balance": {'read_only':True} ,
            "webhook": {'read_only':True} ,
            
    
                        }