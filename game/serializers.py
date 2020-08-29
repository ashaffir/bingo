from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

from .models import Album, Picture

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        # fields = (
        #     'id','username','password1', 'password2','email',
        # )
        fields = '__all__'
        depth=1 

class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        