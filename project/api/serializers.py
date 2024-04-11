from rest_framework import serializers
from .models import *

class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartsSer(serializers.ModelSerializer):
    product = ProductSer()
    class Meta:
        model = Carts
        fields = '__all__'


class OrderSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class LoginSer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','fio']

    def save(self, **kwargs):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            fio = self.validated_data['fio'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user