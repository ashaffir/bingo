from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

from .models import Album, Picture, Player, Game

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

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
        depth = 1