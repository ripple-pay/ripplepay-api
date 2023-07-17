from rest_framework import serializers
from .models import User


class RegisterBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'write_only':True}, 
            'user_permissions': {'write_only':True},
            'is_superuser': {'write_only':True},
            'last_login': {'write_only':True},
            'api-key': {'read_only':True},
            
    
                        }