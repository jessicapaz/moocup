import six
import pytz
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, Product


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',) 

class CreateUserSerializer(serializers.ModelSerializer):
    product_uuid = serializers.UUIDField(format='hex_verbose', required=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'auth_token', 'product_uuid')
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_uuid'))

        email = validated_data['email']
        password = validated_data['password']
        user = User(email=email,product_code=product)
        user.set_password(password)
        user.save()

        return user

    def to_representation(self, obj):
        data = {
            "email": obj.email
        }
        return data

