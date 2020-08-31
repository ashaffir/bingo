# from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

from .models import User

class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id','username','password1', 'password2','email','name','europeCitizenship',
            # 'is_employee', 'is_employer','phone_number',
        )
        read_only_fields = ('id',)

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

import django.contrib.auth.password_validation as validators
class UserResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='user.password', style={'input_type': 'password'},
        max_length=20, min_length=8)
    new_password = serializers.CharField(style={'input_type': 'password'},
        max_length=20, min_length=8)
    class Meta:
        model = User
        fields =("password", 'new_password')

class EmptySerializer(serializers.Serializer):
    pass


##########
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', "")
        password = data.get('password', "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'User is not active'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Unable to login with given credentials'
                raise exceptions.ValidationError(msg)

        else:
            msg = 'Username and Password must be entered'
            raise exceptions.ValidationError(msg)
        
        return data
