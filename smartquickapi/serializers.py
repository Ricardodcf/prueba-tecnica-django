from rest_framework import serializers
from .models import User, Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'token', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
