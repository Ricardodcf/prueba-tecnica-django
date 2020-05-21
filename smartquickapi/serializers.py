from rest_framework import serializers
from .models import User, Client, Bill, Product, BillProduct


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'token', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # bill = BillSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class BillProductSerializer(serializers.ModelSerializer):
    # bill = BillSerializer(many=True, read_only=True)

    class Meta:
        model = BillProduct
        fields = '__all__'
        depth = 1
