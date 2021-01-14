import logging
import random
import json
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from control.models import Control, Category
from .forms import ContactForm, HostSignupForm, LoginForm
from .models import ContentPage, ContactUs
from .utils import get_image_from_data_url
from game.models import Picture, Album, Game, Player, Board, DisplayPicture
from game.utils import check_players, random_game_id
from users.models import User
from users.utils import send_mail
from payments.models import Coupon
from newsletter.models import Newsletter

logger = logging.getLogger(__file__)


def bingo_main(request):
    context = {}
    try: 
        free_players = Control.objects.get(name='free_players')
        context['free_players'] = free_players.value_integer
    except Exception as e:
        print(f">>> BINGO MAIN@bingo_main: free_players is not set. ERROR: {e}")
        logger.error(f">>> BINGO MAIN@bingo_main: free_players is not set. ERROR: {e}")
        context['free_players'] = 5

    try:
        base_price = Control.objects.get(name='base_price')
        context['base_price'] = base_price.value_float
    except Exception as e:
        print(f">>> BINGO MAIN@bingo_main: base_price is not set. ERROR: {e}")
        logger.error(f">>> BINGO MAIN@bingo_main: base_price is not set. ERROR: {e}")
        context['base_price'] = 0.1
    
    if request.LANGUAGE_CODE == 'he':
        try:
            section_a = ContentPage.objects.get(name='home', section='a', language='Hebrew')
            context['section_a'] = section_a
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section A. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section A. ERROR: {e}")

        try:
            section_b = ContentPage.objects.get(name='home', section='b', language='Hebrew')
            context['section_b'] = section_b
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section B. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section B. ERROR: {e}")

        try:
            section_c = ContentPage.objects.get(name='home', section='c', language='Hebrew')
            context['section_c'] = section_c
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section C. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section C. ERROR: {e}")

        try:
            section_d = ContentPage.objects.get(name='home', section='d', language='Hebrew')
            context['section_d'] = section_d
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section C. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage HEBREW section C. ERROR: {e}")

    elif request.LANGUAGE_CODE == 'es':
        try:
            section_a = ContentPage.objects.get(name='home', section='a', language='Spanish')
            context['section_a'] = section_a
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section A. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section A. ERROR: {e}")

        try:
            section_b = ContentPage.objects.get(name='home', section='b', language='Spanish')
            context['section_b'] = section_b
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section B. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section B. ERROR: {e}")

        try:
            section_c = ContentPage.objects.get(name='home', section='c', language='Spanish')
            context['section_c'] = section_c
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section C. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section C. ERROR: {e}")
        try:
            section_d = ContentPage.objects.get(name='home', section='d', language='Spanish')
            context['section_d'] = section_d
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section C. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage SPANISH section C. ERROR: {e}")
    else:
        try:
            section_a = ContentPage.objects.get(name='home', section='a', language='English')
            context['section_a'] = section_a
            section_b = ContentPage.objects.get(name='home', section='b', language='English')
            context['section_b'] = section_b
            section_c = ContentPage.objects.get(name='home', section='c', language='English')
            context['section_c'] = section_c
            section_d = ContentPage.objects.get(name='home', section='d', language='English')
            context['section_d'] = section_d
        except Exception as e:
            print(f">>> BINGO MAIN@main_bingo: Failed loading homepage ENGLISH sections. ERROR: {e}")
            logger.error(f">>> BINGO MAIN@main_bingo: Failed loading homepage ENGLISH sections. ERROR: {e}")

    if request.LANGUAGE_CODE == 'he':
        try:
            context['instructions_a'] = ContentPage.objects.get(name='home', section='instructions_a', language='Hebrew')
        except Exception as e:
            context['instructions_a'] = None
        try:
            context['instructions_b'] = ContentPage.objects.get(name='home', section='instructions_b', language='Hebrew')
        except Exception as e:
            context['instructions_b'] = None
        try:
            context['instructions_c'] = ContentPage.objects.get(name='home', section='instructions_c', language='Hebrew')
        except Exception as e:
            context['instructions_c'] = None
        try:
            context['instructions_d'] = ContentPage.objects.get(name='home', section='instructions_d', language='Hebrew')
        except Exception as e:
            context['instructions_d'] = None
        try:
            context['instructions_e'] = ContentPage.objects.get(name='home', section='instructions_e', language='Hebrew')
        except Exception as e:
            context['instructions_e'] = None
    
    elif request.LANGUAGE_CODE == 'es':
        try:
            context['instructions_a'] = ContentPage.objects.get(name='home', section='instructions_a', language='Spanish')
        except Exception as e:
            context['instructions_a'] = None
        try:
            context['instructions_b'] = ContentPage.objects.get(name='home', section='instructions_b', language='Spanish')
        except Exception as e:
            context['instructions_b'] = None
        try:
            context['instructions_c'] = ContentPage.objects.get(name='home', section='instructions_c', language='Spanish')
        except Exception as e:
            context['instructions_c'] = None
        try:
            context['instructions_d'] = ContentPage.objects.get(name='home', section='instructions_d', language='Spanish')
        except Exception as e:
            context['instructions_d'] = None
        try:
            context['instructions_e'] = ContentPage.objects.get(name='home', section='instructions_e', language='Spanish')
        except Exception as e:
            context['instructions_e'] = None
    else:
        try:
            context['instructions_a'] = ContentPage.objects.get(name='home', section='instructions_a', language='English')
        except Exception as e:
            context['instructions_a'] = None

        try:
            context['instructions_b'] = ContentPage.objects.get(name='home', section='instructions_b', language='English')
        except Exception as e:
            context['instructions_b'] = None
        try:
            context['instructions_c'] = ContentPage.objects.get(name='home', section='instructions_c', language='English')
        except Exception as e:
            context['instructions_c'] = None
        try:
            context['instructions_d'] = ContentPage.objects.get(name='home', section='instructions_d', language='English')
        except Exception as e:
            context['instructions_d'] = None
        try:
            context['instructions_e'] = ContentPage.objects.get(name='home', section='instructions_e', language='English')
        except Exception as e:
            context['instructions_e'] = None

    # Contact us form
    print('>>> SENDING CONTACT')
    if request.method == 'POST':
        contact = ContactUs()
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.message = request.POST.get('message')
        contact.save()

        # Send email to admin
        try:
            subject = "Contact request from Polybingo"
            title = "Contact form details"

            message = {
                'title': title,
                'contact': True,
                'name': request.POST.get('name'),
                'subject': request.POST.get('subject'),
                'email': request.POST.get('email'),
                'message': request.POST.get('message'),
            }

            send_mail(subject, email_template_name=None,attachement='',
                        context=message, to_email=[
                            settings.ADMIN_EMAIL],
                        html_email_template_name='bingo_main/emails/admin_email.html')
        except Exception as e:
            logger.error(
                f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')
            print(
                f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')

            messages.error(
                request, _('Oops, your message was not sent. Please try again later'))

            return redirect(request.META['HTTP_REFERER'])


        messages.success(
            request, _('Your message was sent. We will be in touch soon'))

        return redirect(request.META['HTTP_REFERER'])    

    return render(request, 'bingo_main/index.html', context)

@login_required
def album(request, album_id):
    context = {}
    context['dashboard'] = True

    try:
        album = Album.objects.get(pk=album_id)
        context['album'] = album
        pictures = []
        for pic in album.pictures:
            pictures.append(Picture.objects.get(pk=pic))

        context['pictures'] = pictures

    except Exception as e:
        logger.info(f">>> BINGO MAIN @ album: Failed getting album. E: {e}")
        messages.error(request, _("Sorry, the requested album was not found"))
    return render(request, 'bingo_main/dashboard/album.html', context)

def play(request):
    context = {}
    return render(request,'bingo_main/play.html', context)

def bingo_main_register(request):
    context = {}
    if request.method == 'POST':
        form = HostSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # add employer to db with is_active as False
            
            user.newsletter_optin = True if request.POST.get('newsletter') == 'on' else False
            user.language = request.LANGUAGE_CODE
            try:
                user.country = request.POST.get('country')
            except:
                pass
            user.username = user.email
            user.save()


            # Send welcome message to the new user
            try:
                current_site = request._current_scheme_host
                try:
                    if request.LANGUAGE_CODE == 'he':
                        email_obj = Newsletter.objects.get(name='welcome_email', language='Hebrew')
                        context['lang'] = 'he'
                    elif request.LANGUAGE_CODE == 'es':
                        email_obj = Newsletter.objects.get(name='welcome_email', language='Spanish')
                    else:
                        email_obj = Newsletter.objects.get(name='welcome_email', language='English')
                except Exception as e:
                    logger.error('>>> BINGO MAIN @ bingo_main_register: Missing welcome email language. ERROR:{e}')
                    email_obj = Newsletter.objects.get(name='welcome_email', language='English')

                subject = _('Welcome to Polybingo')

                message = {
                    'user': user,
                    'domain': current_site,
                    'email_obj': email_obj
                }

                send_mail(subject, email_template_name=None, attachement='',
                        context=message, to_email=[user.email],
                        html_email_template_name='users/welcome-email.html')
            
            except Exception as e:
                logger.error(f'>>> BINGO MAIN @ bingo_main_register: Failed sending welcome email. ERROR: {e}')
            
            # print(f"USERNAME: {form.cleaned_data['email']}")
            # print(f"PASS: {form.cleaned_data['password1']}")

            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            print(f"USER: {new_user}")

            login(request, new_user)
            
            return redirect('bingo_main:dashboard')
            # return HttpResponseRedirect("/dashboard/")
        else:
            for error in form.errors:
                messages.error(request, f'Error: {error}')

    else:
        form = HostSignupForm()
        context['form'] = form

    return render(request, 'bingo_main/register.html')


def bingo_main_login(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('bingo_main:dashboard')
            else:
                messages.error(request, f"Wrong Credentials")
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "bingo_main/login.html", {"form": form, "msg": msg})


def about(request):
    context = {}
    if request.LANGUAGE_CODE == 'he':
        try:
            about = ContentPage.objects.get(name='about', language='Hebrew')
            context['about'] = about
        except Exception as e:
            messages.error(request, 'This page content is not ready')
            logger.error('>>> Bingo main: no content for the About section')
    
    elif request.LANGUAGE_CODE == 'es':
        try:
            about = ContentPage.objects.get(name='about', language='Spanish')
            context['about'] = about
        except Exception as e:
            messages.error(request, 'This page content is not ready')
            logger.error('>>> Bingo main: no content for the About section')

    else:
        try:
            about = ContentPage.objects.get(name='about', language='English')
            context['about'] = about
        except Exception as e:
            messages.error(request, 'This page content is not ready')
            logger.error('>>> Bingo main: no content for the About section')


    return render(request, 'bingo_main/about.html', context)


def terms(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='terms')
        context['terms'] = terms
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the Terms section')
    return render(request, 'bingo_main/terms.html', context)

def privacy(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='privacy')
        context['privacy'] = terms
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the Privacy section')
    return render(request, 'bingo_main/privacy.html', context)


def pricing(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='pricing')
        context['pricing'] = pricing
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the pricing section')
    return render(request, 'bingo_main/pricing.html', context)


def why_and_how(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='why_and_how')
        context['why_and_how'] = why_and_how
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the why_and_how section')
    return render(request, 'bingo_main/why_and_how.html', context)


def contact(request):
    context = {}
    print('>>> SENDING CONTACT')
    if request.method == 'POST':
        contact = ContactUs()
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.message = request.POST.get('message')
        contact.save()

        # Send email to admin
        try:
            subject = "Contact request from Polybingo"
            title = "Contact form details"

            message = {
                'title': title,
                'contact': True,
                'name': request.POST.get('name'),
                'subject': request.POST.get('subject'),
                'email': request.POST.get('email'),
                'message': request.POST.get('message'),
            }

            send_mail(subject, email_template_name=None, attachement='',
                        context=message, to_email=[
                            settings.ADMIN_EMAIL],
                        html_email_template_name='bingo_main/emails/admin_email.html')
        except Exception as e:
            logger.error(
                f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')
            print(
                f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')

            messages.error(
                request, _('Oops, your message was not sent. Please try again later'))

            return redirect(request.META['HTTP_REFERER'])


        messages.success(
            request, _('Your message was sent. We will be in touch soon'))

        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'bingo_main/contact.html')


@login_required
def update_profile(request):
    print(f'>> VIEWS MAIN: Profile data: {request.POST}')
    if request.method == 'POST':
        name = request.POST.get('name')
        company_name = request.POST.get('company')
        country = request.POST.get('country')
        vat = request.POST.get('vat')
        profile_pic = request.FILES.get("complogo")

        user = request.user
        if name != '':
            user.name = name

        if company_name != '':
            print(f'COMPANY NAME: {company_name}')
            user.company_name = company_name

        if country:
            user.country = country

        if vat != '':
            user.vat_number = vat

        if profile_pic:
            user.profile_pic = profile_pic

        user.save()

        messages.success(request, 'Profile Updated')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def dashboard(request):
    context = {}
    context['dashboard'] = True
    albums = Album.objects.filter(is_public=True, public_approved=True)
    albums_images = []
    for album in albums:
        pictures = []
        for pic in album.pictures:
            pictures.append(Picture.objects.get(pk=pic))

        albums_images.append({'album_name': album.name, 'album_id': str(
            album.pk), 'board_size': album.board_size, 'pictures': pictures})

    context['albums_images'] = albums_images

    print(f'ALBUMS: {albums}')

    context['albums'] = albums

    return render(request, 'bingo_main/dashboard/index.html', context)


@login_required(login_url='bingo_main:bingo_main_login')
def create_bingo(request, album_id=''):
    context = {}
    context['dashboard'] = True

    try:
        context['categories'] = Category.objects.all()
    except Exception as e:
        print(f'>>> BINGO MAIN @ create_bingo: Categories are not set yet. ERROR: {e}')
        logger.error(f'>>> BINGO MAIN @ create_bingo: Categories are not set yet. ERROR: {e}')
        context['categories'] = []


    if album_id:
        album = Album.objects.get(pk=album_id)
        context['current_album'] = album

        album_pictures = []
        for pic in album.pictures:
            album_pictures.append(Picture.objects.get(pk=pic))
        context['current_album_pictures'] = album_pictures

    if request.method == 'POST':
        if album_id:
            # Update an existing album
            album.name = request.POST.get("name")
            images_dict = json.loads(request.POST.get('images'))
            
            album_description = images_dict["album_description"] 
            album_category = Category.objects.get(name=images_dict["album_category"])

            album_type = images_dict["saveLocation"]  # Private or public
            album.is_public = True if album_type == 'public' else False
            album.album_category = album_category
            album.description = album_description

            album_images = album.pictures
            for image in images_dict['images']:
                if 'pk' not in image:
                    picture = Picture()
                    picture.image_file = get_image_from_data_url(
                        image['image']['dataURL'])[0]
                    picture.name = image['image']['name']
                    picture.title = image["imageName"]
                    picture.album_id = album.album_id
                    picture.public = True if album_type == 'public' else False
                    picture.save()
                    # album_images.append(str(picture.image_file.url))
                    album_images.append(str(picture.pk))
                else:
                    # Update existing image
                    picture = Picture.objects.get(pk=image['pk'])
                    picture.title = image['imageName']
                    picture.save()

            for pk in request.POST.get('delete_images').split(','):
                if pk:
                    Picture.objects.get(pk=pk).delete()

            album_images = list(set(album_images) -
                                set(request.POST.get('delete_images').split(',')))
            album.pictures = album_images
            album.number_of_pictures = len(album_images)
            if len(album_images) <= 33:
                album.board_size = 3
            elif len(album_images) <= 66 and len(album_images) >= 34:
                album.board_size = 4
            else:
                album.board_size = 5

            # If public, setting public_approved back to Flase and updating admin
            if album_type == 'public':
                album.public_approved = False
                album.public_rejected = False

                messages.info(
                    request, _(f"Your updated Bingo Album is pending approval for public view"))

                # Sending request to admin for images approval
                try:
                    subject = "Public Images Approval Request"
                    title = "Public images approval"
                    album = album

                    message = {
                        'title': title,
                        'user': request.user,
                        'album': album,
                    }

                    send_mail(subject, email_template_name=None, attachement='',
                              context=message, to_email=[
                                  settings.ADMIN_EMAIL],
                              html_email_template_name='bingo_main/emails/admin_email.html')
                except Exception as e:
                    logger.error(
                        f'>>> BINGO MAIN: Failed sending admin email for public album approval. ERROR: {e}')

            album.save()
        else:
            images_dict = json.loads(request.POST.get('images'))

            album_description = images_dict["album_description"] 
            album_category = Category.objects.get(name=images_dict["album_category"])  
            album_type = images_dict["saveLocation"]  # Private or public
            album_name = images_dict['album_name']

            print(
                f'Creating a {album_type} album for user: {request.user} name {album_name}')
            logger.info(
                f'Creating an {album_type} album for user: {request.user}')

            try:
                album = Album.objects.create(
                    user=request.user,
                    is_public=True if album_type == 'public' else False,
                    name=album_name,
                    album_category=album_category,
                    description=album_description
                )

                print(f'>>> BINGO MAIN: Album created {album.album_id}')
                logger.info(f'>>> BINGO MAIN: Album created {album.album_id}')

                if album_type == 'public':
                    # Send email to admin for approval
                    print(">>> BINGO MAIN: Send email to admin for approval")
                    logger.info(">>> BINGO MAIN: Send email to admin for approval")

                    messages.info(request, "Your new Bingo Album is pending approval for public view")

                    # Sending request to admin for images approval
                    try:
                        subject = "Public Images Approval Request"
                        title = "Public images approval"
                        album = album

                        message = {
                            'title': title,
                            'user': request.user,
                            'album': album,
                        }

                        send_mail(subject, email_template_name=None,attachement='',
                                  context=message, to_email=[
                                      settings.ADMIN_EMAIL],
                                  html_email_template_name='bingo_main/emails/admin_email.html')
                    except Exception as e:
                        print(f'>>> BINGO MAIN: Failed sending admin email for public album approval. ERROR: {e}')
                        logger.error(f'>>> BINGO MAIN: Failed sending admin email for public album approval. ERROR: {e}')

                album_images = []
                for image in images_dict['images']:
                    picture = Picture()
                    picture.image_file = get_image_from_data_url(
                        image['image']['dataURL'])[0]
                    picture.name = image['image']['name']
                    picture.title = image["imageName"]
                    picture.album_id = album.album_id
                    picture.public = True if album_type == 'public' else False
                    picture.save()

                    # album_images.append(str(picture.image_file.url))
                    album_images.append(str(picture.pk))

                try:
                    album.pictures = album_images
                    album.number_of_pictures = len(album_images)
                    if len(album_images) < 32:
                        album.board_size = 3
                    elif len(album_images) < 54 and len(album_images) > 31:
                        album.board_size = 4
                    else:
                        album.board_size = 5

                    album.save()
                    messages.success(request, 'Album saved')
                    logger.info(
                        f'Album for user {request.user} name >> {album_name} << created')
                    print(
                        f'Album for user {request.user} name >> {album_name} << created')
                    return redirect(request.META['HTTP_REFERER'])

                except Exception as e:
                    print(
                        f'>>> Bingo main: failed to save the pictures to the album. ERROR: {e}')
                    logger.error(
                        f'>>> Bingo main: failed to save the pictures to the album. ERROR: {e}')
            except Exception as e:
                print(
                    f'>>> bingo main: failed to create the album for {request.user}. ERROR: {e}')
                logger.error(
                    f'>>> bingo main: failed to create the album for {request.user}. ERROR: {e}')

    return render(request, 'bingo_main/dashboard/create-bingo.html', context)


@login_required
def my_bingos(request):
    context = {}
    context['dashboard'] = True

    user = request.user
    albums = Album.objects.filter(user=user)
    albums_images = []

    # Album delete
    if request.method == 'POST':
        album_id = request.POST.get('delete_album')
        try:
            Album.objects.get(album_id=album_id).delete()
            messages.success(request, _(f"Album deleted"))
        except Exception as e:
            print(f">>> BINGO MAIN: Failed deleting album. ERROR: {e}")
            logger.error(f">>> BINGO MAIN: Failed deleting album. ERROR: {e}")
            messages.error(request, _(f"Failed deleting the album. Please try again later"))
        print(f">>> BINGO MAIN: Delete Album {album_id}")

    for album in albums:
        pictures = []
        for pic in album.pictures:
            pictures.append(Picture.objects.get(pk=pic))

        albums_images.append({'album_name': album.name, 'album_id': str(
            album.pk), 'board_size': album.board_size, 'pictures': pictures})

    context['albums_images'] = albums_images
    # print(f'ALBUMS: {albums_images}')

    # Get the 3x3 album pictures
    try:
        album_3x3 = Album.objects.filter(user=user, board_size=3).last()
        albums_3x3 = Album.objects.filter(user=user, board_size=3)
        context['albums_3x3'] = albums_3x3
        pictures_3x3 = []
        for pic in album_3x3.pictures:
            pictures_3x3.append(pic)
            context['pictures_3x3'] = pictures_3x3
    except Exception as e:
        # There are no 3x3 album pictures
        logger.error(f'No 3x3 album pictures found. ERROR: {e}')
        print(f'No 3x3 album pictures found. ERROR: {e}')
        context['pictures_3x3'] = 'none'

    # Get the 4x4 album pictures
    try:
        album_4x4 = Album.objects.filter(user=user, board_size=4).last()
        pictures_4x4 = []
        for pic_id in album_4x4.pictures:
            pictures_4x4.append(Picture.objects.get(pk=pic_id))
            context['pictures_4x4'] = pictures_4x4
    except:
        # There are no 4x4 album pictures
        logger.info('No 4x4 album pictures found')
        print('No 4x4 album pictures found')
        context['pictures_4x4'] = 'none'

    # Get the 5x5 album pictures
    try:
        album_5x5 = Album.objects.filter(user=user, board_size=5).last()
        pictures_5x5 = []
        for pic_id in album_5x5.pictures:
            pictures_5x5.append(Picture.objects.get(pk=pic_id))
            context['pictures_5x5'] = pictures_5x5
    except:
        # There are no 5x5 album pictures
        logger.info('No 5x5 album pictures found')
        print('No 5x5 album pictures found')
        context['pictures_5x5'] = 'none'


    return render(request, 'bingo_main/dashboard/my-bingos.html', context)

def instructions(request):
    context = {}

    if request.LANGUAGE_CODE == 'he':
        try:
            context['section_a'] = ContentPage.objects.get(name='instructions', section='a', language='Hebrew')
        except Exception as e:
            context['section_a'] = None
        try:
            context['section_b'] = ContentPage.objects.get(name='instructions', section='b', language='Hebrew')
        except Exception as e:
            context['section_b'] = None
        try:
            context['section_c'] = ContentPage.objects.get(name='instructions', section='c', language='Hebrew')
        except Exception as e:
            context['section_c'] = None
        try:
            context['section_d'] = ContentPage.objects.get(name='instructions', section='d', language='Hebrew')
        except Exception as e:
            context['section_d'] = None
        try:
            context['section_e'] = ContentPage.objects.get(name='instructions', section='e', language='Hebrew')
        except Exception as e:
            context['section_e'] = None
    
    elif request.LANGUAGE_CODE == 'es':
        try:
            context['section_a'] = ContentPage.objects.get(name='instructions', section='a', language='Spanish')
        except Exception as e:
            context['section_a'] = None
        try:
            context['section_b'] = ContentPage.objects.get(name='instructions', section='b', language='Spanish')
        except Exception as e:
            context['section_b'] = None
        try:
            context['section_c'] = ContentPage.objects.get(name='instructions', section='c', language='Spanish')
        except Exception as e:
            context['section_c'] = None
        try:
            context['section_d'] = ContentPage.objects.get(name='instructions', section='d', language='Spanish')
        except Exception as e:
            context['section_d'] = None
        try:
            context['section_e'] = ContentPage.objects.get(name='instructions', section='e', language='Spanish')
        except Exception as e:
            context['section_e'] = None    
    else:
        try:
            context['section_a'] = ContentPage.objects.get(name='instructions', section='a', language='English')
        except Exception as e:
            context['section_a'] = None
        try:
            context['section_b'] = ContentPage.objects.get(name='instructions', section='b', language='English')
        except Exception as e:
            context['section_b'] = None
        try:
            context['section_c'] = ContentPage.objects.get(name='instructions', section='c', language='English')
        except Exception as e:
            context['section_c'] = None
        try:
            context['section_d'] = ContentPage.objects.get(name='instructions', section='d', language='English')
        except Exception as e:
            context['section_d'] = None
        try:
            context['section_e'] = ContentPage.objects.get(name='instructions', section='e', language='English')
        except Exception as e:
            context['section_e'] = None


    return render(request, 'bingo_main/dashboard/instructions.html', context)



@api_view(['GET', ])
def check_game_id(request):
    print(f'GAME REQUEST: {request.GET.keys()}')
    try:
        game = Game.objects.get(game_id=request.GET.get("code"))
        nickname = request.GET.get("name")
        game_id = game.game_id
        print(f'>>> BINGO MAIN: GAME ID: {game_id}')

        if game.is_finished or game.started or game.ended:
            return Response(data={"message": "Game entry finished"}, status=400)

        # If game exists, create new player and add it to the game players list
        player = Player.objects.create(
            game=game,
            nickname=nickname,
            player_game_id=game_id
        )

        print(f'GAME: {game}')
        return Response(data=player.pk, status=200)
    except Exception as e:
        print(f'>>> BINGO MAIN: NO GAME: {e}')
        return Response(data={'message': "Game ID does not exist"}, status=400)
    # return redirect(request.META['HTTP_REFERER'])


def players_approval_list(request, game_id):
    context = {}

    game = Game.objects.get(user=request.user, game_id=game_id)
    context['current_game'] = game

    if game.auto_join_approval:
        players_list = Player.objects.filter(player_game_id=game_id)
        context['players_list'] = players_list
    else:
        unapproved_players_list = Player.objects.filter(player_game_id=game_id, approved=False, not_approved=False)
        context['players_list'] = unapproved_players_list

    return render(request, 'bingo_main/partials/_players_approval_list.html', context=context)

def bingo_players_list(request, game_id):
    context = {}
    bingo_players_shouts_list = Player.objects.filter(Q(player_game_id=game_id) & ~Q(bingo_shouts=0) & Q(active_shout=True))
    active_tickets = []
    for player in bingo_players_shouts_list:
        active_tickets.append(Board.objects.get(player=player).board_number)
    context['active_tickets'] = active_tickets
    return render(request, 'bingo_main/partials/_bingo_players_list.html', context)

@login_required
def player_approval(request, player_id, approval):
    context = {}
    player = Player.objects.get(pk=player_id)
    print(f'>>> BINGO MAIN@player_approval: Player {player}')
    print(f'>>> BINGO MAIN@player_approval:Approval {approval}')
    if approval == 'ok':
        player.approved = True
    elif approval == 'no':
        player.not_approved = True

    player.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def start_bingo(request):
    context = {}
    context['dashboard'] = True

    if request.method == 'POST':
        if 'make_game' in request.POST:
            # Check if there is apositive balance in the host account
            host = request.user
            if host.balance < 0:
                messages.error(
                    request, 'Please deposit funds before creating games')
                return HttpResponseRedirect('bingo_main:add_money')

            # Create a game
            try:
                print(f'ID: {request.POST["make_game"]}')
                album_id = request.POST["make_game"]
                album = Album.objects.get(pk=album_id)

                game = Game()
                game.album = album
                game.board_size = album.board_size

                # Check if there are enough images in the Album
                if len(album.pictures) < 18:
                    print(
                        f'>>> bingo main: failed creating a new game. ERROR: Not enough images in Album {album.name}')
                    logger.error(
                        f'>>> bingo main: failed creating a new game. ERROR: Not enough images in Album {album.name}')
                    messages.error(
                        request, f'Failed creating the new bingo game. Not enough images in Album {album.name}')
                    return redirect(request.META['HTTP_REFERER'])

                game.pictures_pool = album.pictures
                game.user = request.user
                game.game_id = random_game_id(request.user)
                game.save()
                print(
                    f'>>> BINGO MAIN@start_bingo: A new bingo game was created. Game ID {game.game_id}')
                logger.info(
                    f'>>> BINGO MAIN@start_bingo: A new bingo game was created. Game ID {game.game_id}')
            except Exception as e:
                print(
                    f'>>> bingo main: failed creating a new game. ERROR: {e}')
                logger.error(
                    f'>>> bingo main: failed creating a new game. ERROR: {e}')
                messages.error(
                    request, 'Failed creating the new bingo game. Please try again later')
                return render(request, 'bingo_main/dashboard/start-bingo.html')
        else:
            game = Game.objects.filter(user=request.user).last()
            print(f'>>> BINGO MAIN@start_bingo: START BROADCAST DATA')
            logger.info(f'>>> BINGO MAIN@start_bingo: START BROADCAST DATA')
            
            try:
                join_status = json.loads(request.POST.get('game_data'))['joinStatus']  # Auto/Request            
                auto_matching = json.loads(request.POST.get('game_data'))['autoMatching']  # Auto/Request            
                game.auto_join_approval = True if join_status == 'Auto' else False
                game.auto_matching = True if auto_matching == 'autoMatching' else False
                prizes = json.loads(request.POST.get('game_data'))['prizes']
            except Exception as e:
                print(f">>> BINGO MAIN@start_bingo: Failed uploading prizes data. ERROR: {e}")
                logger.error(f">>> BINGO MAIN@start_bingo: Failed uploading prizes data. ERROR: {e}")
                messages.error(request, _("There was an error uploading the images prizes. Please try reducing the images sizes."))
                return redirect(request.META['HTTP_REFERER'])


            try:
                if len(prizes) == 1:
                    game.prize_1_name = prizes[0]["prizeName"]
                    game.prize_1_image_file = get_image_from_data_url(
                        prizes[0]["prizeImage"]['dataURL'])[0]
                    game.winning_conditions = 'bingo'
                    logger.info('One prize game selected')
                    print(f'>>> BINGO MAIN@start_bingo: One prize game selected')
                    logger.info(f'>>> BINGO MAIN@start_bingo: One prize game selected')
                elif len(prizes) == 2:
                    game.prize_1_name = prizes[1]["prizeName"]
                    game.prize_1_image_file = get_image_from_data_url(prizes[1]["prizeImage"]['dataURL'])[0]
                    game.prize_2_name = prizes[0]["prizeName"]
                    game.prize_2_image_file = get_image_from_data_url(prizes[0]["prizeImage"]['dataURL'])[0]
                    game.winning_conditions = '1line'
                    game.current_winning_conditions = '1line'
                    print(f'>>> BINGO MAIN@start_bingo: Two prizes game selected')
                    logger.info(f'>>> BINGO MAIN@start_bingo: Two prizes game selected')
                elif len(prizes) == 3:
                    game.prize_1_name = prizes[2]["prizeName"]
                    game.prize_1_image_file = get_image_from_data_url(prizes[2]["prizeImage"]['dataURL'])[0]
                    game.prize_2_name = prizes[0]["prizeName"]
                    game.prize_2_image_file = get_image_from_data_url(prizes[0]["prizeImage"]['dataURL'])[0]
                    game.prize_3_name = prizes[1]["prizeName"]
                    game.prize_3_image_file = get_image_from_data_url(prizes[1]["prizeImage"]['dataURL'])[0]
                    game.winning_conditions = '2line'
                    game.current_winning_conditions = '1line'
                    print(f'>>> BINGO MAIN@start_bingo: Three prizes game selected')
                    logger.info(f'>>> BINGO MAIN@start_bingo: Three prizes game selected')

                game.save()

            except Exception as e:
                print(f">>> BINGO MAIN: Failed loading the prize images. ERROR: {e}")
                logger.error(f">>> BINGO MAIN: Failed loading the prize images. ERROR: {e}")

    return render(request, 'bingo_main/dashboard/start-bingo.html', context)


@login_required
def broadcast(request):
    context = {}
    host = request.user
    current_game = Game.objects.filter(user=request.user).last()
    context['current_game'] = current_game

    if current_game.auto_join_approval:
        players_list = Player.objects.filter(player_game_id=current_game.game_id)
        context['players_list'] = players_list
    else:
        unapproved_players_list = Player.objects.filter(player_game_id=current_game.game_id, approved=False, not_approved=False)
        context['players_list'] = unapproved_players_list

    if request.method == 'POST':
        # Checking if there are minimum players
        try:
            min_players = Control.objects.get(name='min_players').value_integer
        except Exception as e:
            min_players = 2

        if len(current_game.players_list) < min_players:
            messages.error(
                request, f"Not enough players... Need at leaset {min_players} tikets")
            return redirect(request.META['HTTP_REFERER'])
        else:
            # Start the game
            current_game.started = True
            current_game.save()

            # print(f'GAME COST: {game.game_cost}')
            # Billing: Check user's balance and deduct the amount
            current_balance = host.balance
            game_cost = current_game.game_cost
            new_balance = current_balance - game_cost
            if new_balance > 0:
                # Updating user new balance
                host.balance = new_balance
                host.spent += round(game_cost,2)
                host.save()

            else:
                messages.error(
                    request, _('There are not enough funds in your account. Please make a deposit'))
                return redirect('bingo_main:add_money')

            return HttpResponseRedirect(reverse('bingo_main:game', args=[current_game.game_id]))

    return render(request, 'bingo_main/broadcast/index.html', context=context)


@api_view(['GET', ])
def player_approval_status(request, game_id, player_id):
    print('Polling player approval status....')
    context = {}
    try:
        player = Player.objects.get(pk=player_id)
    except Exception as e:
        print(f'ERROR: {e}')
    if player.approved:
        return Response(status=200)
    else:
        return Response(status=500)


def game(request, game_id):
    context = {}
    game = Game.objects.get(user=request.user, game_id=game_id)

    if game.is_finished or game.ended:
        context['game_ended'] = True
        messages.error(request, _('Game already played'))
        # return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect(reverse('bingo_main:game_over', args=[game.game_id]))

    host = request.user

    # Checking if there are minimum players
    # try:
    #     min_players = Control.objects.get(name='min_players').value_integer
    # except Exception as e:
    #     min_players = 2

    # if len(game.players_list) < min_players:
    #     messages.error(
    #         request, _(f"Not enough players. Need at least" + str(min_players) + _("tickets")))
    #     return redirect(request.META['HTTP_REFERER'])

    # Locking prizes already won
    if game.prize_2_won:
        game.prize_2_locked = True

    if game.prize_3_won:
        game.prize_3_locked = True

    game.save()

    if request.method == 'POST' or not game.in_progress:
        # Game Play
        pictures_pool_list = game.pictures_pool
        items_list = []
        if len(pictures_pool_list) > 0:
            for pic in pictures_pool_list:
                items_list.append(pic)

            # Drawing a random key from the dict
            picture_draw_index = random.randint(0, len(items_list)-1)
            rand_item = items_list[picture_draw_index]
            picture_draw = pictures_pool_list.pop(picture_draw_index)

            # Updating the DB with the reduced list of pictures
            game.pictures_pool = pictures_pool_list

            current_shown_pictures_ids = game.shown_pictures
            current_shown_pictures_ids.append(rand_item)
            game.shown_pictures = current_shown_pictures_ids
            game.current_picture = Picture.objects.get(pk=picture_draw)

            game.save()

            current_shown_pictures = []
            for p in current_shown_pictures_ids:
                current_shown_pictures.append(Picture.objects.get(pk=p))

            context['remaining_pictures'] = len(pictures_pool_list)
            context['current_picture'] = Picture.objects.get(pk=picture_draw)
            context['current_shown_pictures'] = current_shown_pictures if len(current_shown_pictures) <= 6 else current_shown_pictures[-6:]
            context['current_shown_pictures_count'] = len(current_shown_pictures)

            # Check the players' boards:
            ############################
            disp_pic_drawn_appearances = DisplayPicture.objects.filter(image=Picture.objects.get(pk=picture_draw), game_id=game.game_id)
            print(f'APPEAR: {disp_pic_drawn_appearances}')
            # active_boards = check_players(picture_id=picture_draw, game_id=game_id)
            active_boards = []
            for disp_pic in disp_pic_drawn_appearances:
                active_boards.append(disp_pic.board)

            print(f'ACTIVE BOARDS: {active_boards}')

            picture_draw = Picture.objects.get(pk=picture_draw)

            for board in active_boards:
                # print(f'>> Pic: {picture_draw_id}')
                # print(f'>> B: {board.pictures_draw}')
                player = Player.objects.get(board_id=board.pk)
                x_count_full = 0
                line_count = 0

                for i in range(board.size):
                    x_count_row = 0
                    board_row = []
                    for pic in board.pictures_draw[i]:
                        if 'XXX' not in pic:
                            if picture_draw == DisplayPicture.objects.get(pk=pic).image:
                                board_row.append('XXX'+pic)
                            else:
                                board_row.append(pic)
                        else:
                            board_row.append(pic)
                        
                    board.pictures_draw[i] = board_row

                    # 1) Replace the hits with an X
                    # board.pictures_draw[i] = [pic if pic != picture_draw_id else 'XXX'+pic for pic in board.pictures_draw[i]]

                    # Count the 'X's are on the board
                    for p in board.pictures_draw[i]:
                        if 'XXX' in p:
                            x_count_full += 1
                            x_count_row += 1
                    
                        if x_count_row == board.size:
                            line_count += 1

                    # x_count_full += board.pictures_draw[i].count('X')
                    print(f'Ticket: {board.board_number} | X count: {x_count_full} | line count {line_count}')

                    # Count the 'X's are on the row
                    # x_count_row += board.pictures_draw[i].count('X')

                    if game.current_winning_conditions == '1line' and line_count > 0:
                            print(f'BINGO ROW: Player {player.nickname} Row {i} board {board} Ticket: {board.board_number}!!!')
                            logger.info(f'BINGO ROW: Player {player.nickname} Row {i} board {board} Ticket: {board.board_number}!!!')

                            game.prizes_won.append('1line')
                            player.winnings.append('1line')

                    elif game.current_winning_conditions == '2line' and line_count > 1:
                        if x_count_full % board.size == 0 and x_count_full < board.size ** 2:
                            print('TWO ROWS BINGO')
                            player.winnings.append('2line')
                            game.prizes_won.append('2line')
                            print(f'BINGO TWO ROWS: Player {player.nickname} board {board} Ticket: {board.board_number}!!!')
                            logger.info(f'BINGO TWO ROWS: Player {player.nickname} board {board} Ticket: {board.board_number}!!!')

                    elif x_count_full == board.size ** 2:
                        player.winnings.append('bingo')
                        player.save()
                        game.prizes_won.append('2line')
                        print(f'BINGO FULLLLL!!! Player {player.nickname} Board: {board} Ticket: {board.board_number}')
                        logger.info(f'BINGO FULLLLL!!! Player {player.nickname} Board: {board} Ticket: {board.board_number}')


                    player.save()
                    game.save()

                    # Update the board with the hits
                    board.save()

                    # Reset the row count for the next row
                    x_count_row = 0

                # Columns and diagnals winning condition check
                x_count_diag_left_to_right = 0
                x_count_diag_right_to_left = 0

                for column in range(board.size):
                    player = Player.objects.get(board_id=board.pk)
                    x_count_column = 0

                    for row in range(board.size):
                        if board.pictures_draw[row][column] == 'X':
                            x_count_column += 1
                            # player.winnings.append(f'row_{row}_col_{column}') #Appending all points for later special bingo forms

                    if x_count_column == board.size:
                        # player.winnings.append(f'col_{column}') # Column bingo support
                        # print(f'BINGO Column! Player {player.nickname} Column {i} board {board}!!!')
                        # logger.info(f'BINGO Column! Player {player.nickname} Column {i} board {board}!!!')
                        pass

                    if board.pictures_draw[column][column] == 'X':
                        x_count_diag_left_to_right += 1

                    if x_count_diag_left_to_right == board.size:
                        # player.winnings.append('diag_l2r') # L2R Diagonal bingo support
                        # print(f'BINGO Left 2 Right Diagonal! Player {player.nickname} Diagonal L2R board {board}!!!')
                        # logger.info(f'BINGO Left 2 Right Diagonal! Player {player.nickname} Diagonal L2R board {board}!!!')
                        pass

                    if board.pictures_draw[-column-1][-column-1] == 'X':
                        x_count_diag_right_to_left += 1

                    if x_count_diag_right_to_left == board.size:
                        # player.winnings.append('diag_r2l') # R2L Diagonal bingo support
                        # print(f'BINGO Right to Left Diagonal! Player {player.nickname} Diagonal R2L board {board}!!!')
                        # logger.info(f'BINGO Right to Left Diagonal! Player {player.nickname} Diagonal R2L board {board}!!!')
                        pass

                    player.save()


        else:
            game.ended = True
            game.is_finished = True
            game.save()
            return HttpResponseRedirect(reverse('bingo_main:game_over', args=[game.game_id]))

    else:
        current_shown_pictures = []
        for p in game.shown_pictures:
            current_shown_pictures.append(Picture.objects.get(pk=p))

        context['current_shown_pictures'] = current_shown_pictures if len(
            current_shown_pictures) <= 6 else current_shown_pictures[-6:]
        context['current_picture'] = game.current_picture
        context['current_shown_pictures_count'] = len(current_shown_pictures)

    # Clearing the bingo shouts if there are any.
    bingo_players_shouts_list = Player.objects.filter(Q(player_game_id=game_id) & ~Q(bingo_shouts=0) & Q(active_shout=True))
    for player in bingo_players_shouts_list:
        player.active_shout = False
        player.save()

    context['current_game'] = game
    return render(request, 'bingo_main/broadcast/game.html', context)

@login_required
def check_board(request, game_id):
    context = {}

    host = request.user

    current_game = Game.objects.get(user=host, game_id=game_id)
    current_game.in_progress = True
    current_game.save()

    context['current_game'] = current_game
    context['host'] = host

    game_winning_conditions = current_game.winning_conditions

    if request.method == 'POST':

        ticket_number = request.POST.get('cardNumber')
        context['board_number'] = ticket_number

        try:
            board = Board.objects.get(board_number=ticket_number, game_id=game_id)
            context['board'] = board

            context['player'] = Player.objects.get(board_id=board.pk)
            
            matched_count = 0
            board_pictures = []
            for row in board.pictures:
                for pic in row:
                    disp_pic = DisplayPicture.objects.get(pk=pic)
                    # print(f"pic: {pic} drawn: {board.pictures_draw} ")
                    for p_draw in board.pictures_draw:
                        if str('XXX'+pic) in str(p_draw):
                            disp_pic.matched = True
                            disp_pic.save()
                            matched_count += 1
                    

                    board_pictures.append(disp_pic)
            # Ending the game on Bingo
            if matched_count == board.size ** 2:
                current_game.ended = True
                current_game.is_finished = True
                current_game.save()
                print(f">>> BINGO MAIN @ check_board: Full bingo on game {current_game.game_id} board ticket {board.board_number}")
                logger.info(f">>> BINGO MAIN @ check_board: Full bingo on game {current_game.game_id} board ticket {board.board_number}")


            context['board_pictures'] = board_pictures
        except Exception as e:
            print(f">>> BINGO MAIN @ check_board: Ticket entered does not exists. E: {e}")
            logger.info(f">>> BINGO MAIN @ check_board: Ticket entered does not exists. E: {e}")


        # Validating ticket number
        if ticket_number == '' or int(ticket_number) < 0:
            messages.error(request, _("Please enter a valid card number"))
            return render(request, 'bingo_main/broadcast/check_board.html', context)
        elif int(ticket_number) > len(current_game.players_list):
            messages.error(request, _("The ticket is not a part of this game"))
            return render(request, 'bingo_main/broadcast/check_board.html', context)

        # Collecting the winning players/boards so far
        winning_players = []
        winning_boards = []
        winning_boards_id = []
        for player in Player.objects.filter(player_game_id=game_id):
            if player.winnings != []:
                winning_players.append(player)
                winning_boards.append(Board.objects.get(pk=player.board_id))
                winning_boards_id.append(player.board_id)

        # Checking ticket
        win = False
        for b in winning_boards:
            if b.board_number == int(ticket_number):
                print(f'Winning Ticket {ticket_number}')
                winning_board = b
                winning_player = Player.objects.get(board_id=b.pk)

                context['player'] = winning_player

                if game_winning_conditions == 'bingo':
                    if 'bingo' in winning_player.winnings:
                        context['prize_1'] = True
                        win = True

                        current_game.is_finished = True

                    current_game.save()

                elif game_winning_conditions == '1line':
                    if 'bingo' in winning_player.winnings:
                        context['prize_1'] = True
                        win = True
                        current_game.is_finished = True
                    elif '1line' in winning_player.winnings and not current_game.prize_2_locked:
                        context['prize_2'] = True
                        win = True
                        current_game.prize_2_won = True
                        current_game.current_winning_conditions = 'bingo'

                    current_game.save()

                elif game_winning_conditions == '2line':
                    if 'bingo' in winning_player.winnings:
                        context['prize_1'] = True
                        win = True
                        current_game.is_finished = True
                        current_game.save()
                    elif '2line' in winning_player.winnings and not current_game.prize_3_locked:
                        context['prize_3'] = True
                        win = True
                        current_game.prize_3_won = True
                        current_game.current_winning_conditions = 'bingo'
                    elif '1line' in winning_player.winnings and not current_game.prize_2_locked:
                        context['prize_2'] = True
                        win = True
                        current_game.prize_2_won = True
                        current_game.current_winning_conditions = '2line'

                    current_game.save()

                else:
                    win = False

                if win:
                    print(f'>>> BINGO MAIN@check_board: result WIN')
                    logger.info(f'>>> BINGO MAIN@check_board: result WIN')
                    context['check_result'] = 'WIN'
                    current_shown_pictures = []
                    for p in current_game.shown_pictures:
                        current_shown_pictures.append(Picture.objects.get(pk=p))

                    context['current_shown_pictures'] = current_shown_pictures

                    return render(request, 'bingo_main/broadcast/checkResult.html', context)

        print(f'>>> BINGO MAIN@check_board: result Wrong')
        logger.info(f'>>> BINGO MAIN@check_board: result Wrong')
        context['check_result'] = 'Wrong'


        current_shown_pictures = []
        for p in current_game.shown_pictures:
            current_shown_pictures.append(Picture.objects.get(pk=p))

        context['current_shown_pictures'] = current_shown_pictures
        return render(request, 'bingo_main/broadcast/checkResult.html', context)

    return render(request, 'bingo_main/broadcast/check_board.html', context)


@login_required
def game_over(request, game_id):
    context = {}
    host = request.user
    context['current_game'] = Game.objects.get(user=host, game_id=game_id)
    return render(request, 'bingo_main/broadcast/game_over.html', context)


# Player's bingo card/ticket/board
def bingo(request, player_id):
    context = {}
    print(f'>>> BINGO MAIN @ bingo: player ID {player_id}')
    logger.info(f'>>> BINGO MAIN @ bingo: player ID {player_id}')

    player = Player.objects.get(pk=player_id)
    board = Board.objects.get(pk=player.board_id)
    game = Game.objects.get(pk=player.game.pk)
    host = game.user
    host_logo = host.profile_pic
    context['host_logo'] = host_logo

    context['player'] = player

    context['board'] = board

    board_pictures = []
    for row in board.pictures:
        for pic in row:
            disp_pic = DisplayPicture.objects.get(pk=pic)
            # print(f"pic: {pic} drawn: {board.pictures_draw} ")
            for p_draw in board.pictures_draw:
                if str('XXX'+pic) in str(p_draw):
                    disp_pic.matched = True
                    disp_pic.save()

            board_pictures.append(disp_pic)
    context['board_pictures'] = board_pictures

    if game.is_public:
        context['approval_required'] = 'false'
    elif not game.is_public and player.approved:
        context['approval_required'] = 'false'
    else:
        context['approval_required'] = 'true'

    context['game'] = game
    shown_pictures_ids = game.shown_pictures
    shown_pictures = []
    print(f'>>> MAIN: SHOWN PICS: {shown_pictures}')
    if len(shown_pictures_ids) >= 1:
        for pic in shown_pictures_ids:
            shown_pictures.append(Picture.objects.get(pk=pic))
        context['current_picture'] = shown_pictures[-1]
    else:
        context['current_picture'] = None

    # pictures = []
    # for pic in board.pictures:
    #     for p in pic:
    #         pictures.append(p)

    # # print(f'{pictures} \n')
    # context['pictures'] = pictures
    return render(request, 'bingo_main/bingo.html', context)


def current_displayed_picture(request, game_id):
    context = {}
    host = request.user
    try:
        game = Game.objects.get(user=host, game_id=game_id)
        context['game'] = game
    except Exception as e:
        logger.error(
            f'>>> Bingo Main: Failed to find game with ID {game_id} for host {host}. ERROR: {e}')
        print(
            f'>>> Bingo Main: Failed to find game with ID {game_id} for host {host}. ERROR: {e}')

    return render(request, 'bingo_main/partials/_current_displayed_picture.html', context)


def player_board(request, player_id):
    context = {}
    print(f'>>> BINGO MAIN @ player_board: player ID {player_id}')
    logger.info(f'>>> BINGO MAIN @ player_board: player ID {player_id}')

    player = Player.objects.get(pk=player_id)
    board = Board.objects.get(pk=player.board_id)
    game = Game.objects.get(pk=player.game.pk)
    host = game.user

    context['board'] = board
    board_pictures = []
    for row in board.pictures:
        for pic in row:
            disp_pic = DisplayPicture.objects.get(pk=pic)
            board_pictures.append(disp_pic)

    context['board_pictures'] = board_pictures

    context['game'] = game
    return render(request, 'bingo_main/partials/_player_board.html', context)

@login_required
def add_money(request):
    context = {}
    context['dashboard'] = True
    try:
        min_deposit = Control.objects.get(name='min_deposit').value_float
        max_deposit = Control.objects.get(name='max_deposit').value_float
        context['min_deposit'] = min_deposit
        context['max_deposit'] = max_deposit
    except Exception as e:
        print(f">>> MAIN BINGO @ add_money: CONTROL min/max deposit was not defined. ERROR: {e}")
        logger.error(f">>> MAIN BINGO @ add_money: CONTROL min/max deposit was not defined. ERROR: {e}")
        min_deposit = 5
        max_deposit = 200
        context['min_deposit'] = 5
        context['max_deposit'] = 200

    if request.method == 'POST':
        if 'make_payment' in request.POST:
            money = request.POST.get('money')
            
            coupon = request.POST.get('coupon') if request.POST.get('coupon') else "no_coupon"
            
            try:
                coupons = Coupon.objects.filter(active=True)
                coupons_ids = []
                for c in coupons:
                    coupons_ids.append(c.coupon_id)

                if coupon in coupons_ids and 'ONME' in coupon:
                    amount = 0
                    return HttpResponseRedirect(reverse('payments:payment', args=[amount, coupon]))
            except Exception as e:
                logger.info(">>> BING MAIN @ add_money: No coupon defined")

            try:
                if money and float(money) >= min_deposit and float(money) <= max_deposit:
                    amount = money
                elif request.POST.get('deposit_amount'):
                    amount = request.POST.get('deposit_amount')
                else:
                    messages.error(request, _(f"The amount entered is not valid. Please make sure the deposit is above $") + str(min_deposit) + _(" and below $") + str(max_deposit))
                    return redirect(request.META['HTTP_REFERER'])
            except Exception as e:
                print(f"AMOUNT ERROR: {e}")
                messages.error(request, _('Please enter a valid amount'))
                return redirect(request.META['HTTP_REFERER'])

            if amount != '':
                return HttpResponseRedirect(reverse('payments:payment', args=[amount, coupon]))
            else:
                messages.error(request, _('Please enter an amount, or pick one of the predefined amounts.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'bingo_main/dashboard/add-money.html', context)

@login_required
def search(request):
    context = {}
    context['dashboard'] = True
    if request.method == 'POST':
        search_string = request.POST.get('search')
        print(f"SEARCH Q: {search_string}")
        albums = Album.objects.all().filter(name__contains=search_string,is_public=True)
        context['albums'] = albums
        print(f"SEARCH RES: {albums}")
        return render(request, 'bingo_main/dashboard/search_results.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def logout_view(request):
    context = {}
    logout(request)
    return redirect('bingo_main:bingo_main')


def handler500(request, *args, **argv):
    return redirect('bingo_main:bingo_main')


def handler403(request, *args, **argv):
    return redirect('bingo_main:bingo_main')


def handler404(request, *args, **argv):
    return render(request, 'bingo_main/404.html')
