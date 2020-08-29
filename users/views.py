from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login as django_login, logout as django_logout

from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)
from django.shortcuts import render

from . import serializers
# from .utils import get_and_authenticate_user, create_user_account

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def restricted(request, *args, **kwargs):
    return Response(data='WELCOME', status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    '''
    Register a new user with the API
    '''
    if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # Creating the new User account
            account = serializer.save()
            data['response'] = 'Success registration.'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors
            print(f'DATA: {data}')
        
        return Response(data)
        
class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Block the code from continue if raised exception
        user = serializer.validated_data['user']
        django_login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key}, status=200)

@api_view(['POST',])
def logout_view(request):
    django_logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def password_change(request):
    # serializer = serializers.PasswordChangeSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # request.user.set_password(serializer.validated_data['new_password'])
    # request.user.save()
    # return Response(status=status.HTTP_204_NO_CONTENT)
    reset_password_serializer = serializers.UserResetPasswordSerializer(request.user, data=request.data)

    if reset_password_serializer.is_valid():
        print('HERE')
        if not request.user.check_password(request.data.get('password')):
            return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(request.data.get('new_password'))
        request.user.save()
        return Response({"Message": ["Password reset successfully"]}, status=status.HTTP_200_OK)
    
    return Response(reset_password_serializer.error_messages)