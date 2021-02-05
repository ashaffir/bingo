from .tokens import account_activation_token
from .models import User
from . import serializers
import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core import serializers as d_serializers
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import gettext as _
from django.conf import settings

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
from administration.decorators import superuser_required
from bingo_main.models import ContentPage
from newsletter.models import Newsletter
from game.models import Album, Player, Game
from bingo_main.utils import alert_admin
from membership.models import Plan

logger = logging.getLogger(__file__)


# from .utils import get_and_authenticate_user, create_user_account

@login_required
def profile_test(request):
    context = {}
    # Contact us form
    user = request.user
    return render(request, 'users/profile_test.html', context)

@login_required
def profile(request):
    context = {}
    user = request.user
    print(f'>> VIEWS MAIN: Profile data: {request.POST}')
    try:
        context['user_albums'] = Album.objects.filter(user=request.user)
    except:
        context['user_albums'] = []

    try:
        context['user_games'] = Game.objects.filter(user=request.user)
    except:
        context['user_games'] = []

    try:
        context['user_plan'] = Plan.objects.get(name=user.plan_name)
    except:
        context['user_plan'] = Plan.objects.get(name='free')

    ### Populate the plans ###
    try:
        if settings.DEBUG:
            context['free_plan'] = Plan.objects.get(name='free')
            context['basic_plan'] = Plan.objects.get(name='basic')
            context['expert_plan'] = Plan.objects.get(name='expert')
        else:
            context['free_plan'] = Plan.objects.get(name='free')
            context['basic_plan'] = Plan.objects.get(name='basic')
            context['expert_plan'] = Plan.objects.get(name='expert')        
    except Exception as e:
        print(f">>> USERS @ profile: Failed to get plans. ERROR: {e}")
        logger.error(f">>> USERS @ profile: Failed to get plans. ERROR: {e}")
        alert_admin(f"Failed to get plans. ERROR: {e}",'Profile')



    if request.method == 'POST':
        if 'update_personal' in request.POST:
            print(f"POST: {request.POST}")
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            phone = request.POST.get('phone')
            mobile = request.POST.get('mobile')
            company_name = request.POST.get('company')
            country = request.POST.get('country')
            vat = request.POST.get('vat')
            profile_pic = request.FILES.get("complogo")

            user = request.user
            if fname != '':
                user.first_name = fname

            if lname != '':
                user.last_name = lname

            if company_name != '':
                user.company_name = company_name

            if country:
                user.country = country

            if vat != '':
                user.vat_number = vat

            if profile_pic:
                user.profile_pic = profile_pic

            if phone:
                user.phone = phone

            if mobile:
                user.mobile_phone = mobile

            user.save()

            messages.success(request, _('Your profile was successfuly updated'))
            # return redirect('bingo_main:bingo_main')
            # return redirect(request.META['HTTP_REFERER'])       
    
    
    return render(request, 'users/profile.html', context)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def restricted(request, *args, **kwargs):
    return Response(data='WELCOME', status=status.HTTP_200_OK)


@api_view(['POST', ])
def registration_view(request):
    '''
    Register a new user with the API
    '''
    print(f'USERS VIEWS: Register')
    logger.info(f'USERS VIEWS: Register')
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

            return redirect('bingo_main:bingo_main')

        else:
            data = serializer.errors
            print(f'Registration info: {data}')

        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def auth_view(request):
    data = {}
    if request.method == 'POST':
        user_info = User.objects.get(pk=request.user.pk)

        data['username'] = user_info.username
        data['email'] = user_info.username
        data['phone'] = user_info.phone
        data['first_name'] = user_info.first_name
        data["last_name"] = user_info.last_name

        # TODO: Return all user data
        return Response(data, status=200)


class LoginView(APIView):
    def post(self, request):
        data = {}

        print(f'USERS VIEWS: Login')
        logger.info(f'USERS VIEWS: Login')

        serializer = serializers.LoginSerializer(data=request.data)
        # Block the code from continue if raised exception
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_info = User.objects.get(pk=user.pk)

        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        data['username'] = user_info.username
        data['email'] = user_info.username
        data['phone'] = user_info.phone
        data['first_name'] = user_info.first_name
        data["last_name"] = user_info.last_name
        data['token'] = token.key

        return redirect('bingo_main:dashboard')

        # TODO: Return all user data
        return Response(data, status=200)


@api_view(['POST', ])
def logout_view(request):
    django_logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)


def password_change(request):
    # serializer = serializers.PasswordChangeSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # request.user.set_password(serializer.validated_data['new_password'])
    # request.user.save()
    # return Response(status=status.HTTP_204_NO_CONTENT)
    reset_password_serializer = serializers.UserResetPasswordSerializer(
        request.user, data=request.data)

    if reset_password_serializer.is_valid():
        if not request.user.check_password(request.data.get('password')):
            return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(request.data.get('new_password'))
        request.user.save()
        return Response({"Message": ["Password reset successfully"]}, status=status.HTTP_200_OK)

    return Response(reset_password_serializer.error_messages)


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('login_email')
        user = User.objects.filter(email=email).first()
        if email:
            if '@' in email:

                if user is not None:
                    print(f"USER {user}")
                    token_generator = default_token_generator

                    context = {
                        'domain': request._current_scheme_host,
                        'uidb64':  urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': token_generator.make_token(user),
                        'user': user
                    }

                    try:
                        send_mail('Polybingo - Reset Password', email_template_name=None, attachement='',
                                  context=context, to_email=[email],
                                  html_email_template_name='users/change-password-email.html')

                        messages.success(request, _("Check your mail inbox to reset password"))
                        return redirect('bingo_main:bingo_main')

                    except Exception as e:
                        print(f">>> USERS @ forgot_password: Failed to send recovery email. ERROR: {e}")
                        logger.error(f">>> USERS @ forgot_password: Failed to send recovery email. ERROR: {e}")
                        messages.error(request, _("Something went wrong. Please try again later."))
                        return redirect(request.META['HTTP_REFERER'])

                else:
                    messages.error(request, _("This email is not registered to us. Please register first"))
                    # return Response('The email enteres in not registered. Please register.')
                    return redirect('bingo_main:bingo_main')
            else:
                messages.error(request, _("Please enter a valid email"))
                return redirect(request.META['HTTP_REFERER'])
                
        else:
            enter_email_msg = gettext("Please do enter the email")
            messages.error(request, enter_email_msg)
            return redirect(request.META['HTTP_REFERER'])
            
    else:
        return render(request, 'users/forgot_password.html', {})

@superuser_required
def test_welcome_email(request):
    context = {}
    context['content'] = Newsletter.objects.get(name='welcome_email')
    user = request.user
    return render(request, 'users/welcome-email.html', context)