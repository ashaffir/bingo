from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)
from django.shortcuts import render

@api_view(['GET',])
def check_server(request):
    date = datetime.now().strftime(("%d/%m/%Y %H:%M:%S"))
    message = 'Current time on server'
    return Response(data=message + date, status=status.HTTP_200_OK)