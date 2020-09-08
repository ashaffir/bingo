from datetime import datetime
from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import gettext

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)

from .utils import send_mail


from . import serializers
from .models import User
from .tokens import account_activation_token
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
            data['name'] = account.name
            data['europeCitizenship'] = account.europeCitizenship
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
        
        # TODO: Return all user data
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

@api_view(['POST',])
def forgot_password(request):
    if request.method == "POST":
        email = request.data["email"]

        if email:
            print(f"EMAIL: ***************{email}****************")
            if '@' in email: 

                user = User.objects.filter(email=email).first()
                print(f'>>>>>>>  USER: {user}')
                # return HttpResponse(user)
                if user is not None :
                    token_generator = default_token_generator

                    context = {
                        'domain': request._current_scheme_host,
                        'uidb64':  urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': token_generator.make_token(user),
                        'user': user
                    }

                    try:
                        send_mail('Reset Password', email_template_name=None,
                                  context=context, to_email=[email],
                                  html_email_template_name='users/change-password-email.html')
                        
                        check_email_message = gettext("Check your mail inbox to reset password")
                        messages.success(request, check_email_message)
                        # return redirect('dndsos:home')
                        return Response('check your email')

                    except Exception as ex:
                        print(ex)
                        # messages.error(request, "Email configurations Error !!!")
                        return Response('Failed to send email')
                    
                    # return redirect('core:login')
                else:
                    not_registered_message = gettext("This email is not registered to us. Please register first ")
                    messages.error(request, not_registered_message)
                    return Response('The email enteres in not registered. Please register.')
                    # return redirect('dndsos:home')
            else:
                valid_email_message = gettext("Please enter a valid email")
                # messages.error(request, valid_email_message)
                return Response('Please enter a valid email')
                # return redirect('core:forgot-password')
        else:
            enter_email_msg =  gettext("Please do enter the email")
            messages.error(request, enter_email_msg)
            return Response('Please do enter the email')
            # return redirect('core:forgot-password')
    else:
        # return render(request, 'core/forgot_password.html', {})
        return Response(status.HTTP_400_BAD_REQUEST)
        