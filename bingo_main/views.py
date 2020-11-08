import logging
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import ContactForm, HostSignupForm, LoginForm
from .models import ContentPage
from .utils import get_image_from_data_url
from game.models import Picture, Album

logger = logging.getLogger(__file__)

def bingo_main(request):
    context = {}
    return render(request, 'bingo_main/index.html')

def bingo_main_register(request):
    context = {}
    if request.method == 'POST':
        form = HostSignupForm(request.POST)
        if form.is_valid():
            user = form.save() # add employer to db with is_active as False
            user.username = user.email
            user.save()
            
            # send employer a accout activation email
            # current_site = request._current_scheme_host
            # subject = gettext('Activate PickNdell Account')

            # message = {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user)
            # }

            # send_mail(subject, email_template_name=None,
            #         context=message, to_email=[user.email],
            #         html_email_template_name='registration/account_activation_email.html')


            messages.success(request, 'An accout activation link has been sent to your email: ' + user.email +
                                '. Check your email and click the link to activate your account.')
            return redirect('bingo_main:bingo_main')
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
                messages.error(request,f"Wrong Credentials" )
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "bingo_main/login.html", {"form": form, "msg": msg})


def about(request):
    context = {}
    try:
        about = ContentPage.objects.get(name='about')
        context['about'] = about
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the About section')
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
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message was sent. We will be in touch soon')
            # return redirect(request.META['HTTP_REFERER'])
            return redirect('bingo_main:bingo_main')
        else:
            messages.error(request, 'Your message was not sent. Please try again later')
            logger.error('>> BING MAIN: Error sending contact us message')
            return redirect('bingo_main:bingo_main')

    return render(request, 'bingo_main/contact.html')

@login_required
def dashboard(request):
    context = {}
    return render(request, 'bingo_main/dashboard/index.html')

@login_required(login_url='bingo_main:bingo_main_login')
def create_bingo(request):
    context = {}
    if request.method == 'POST':
        if 'updateProfile' in request.POST:
            print(f'UPDATE: {request.POST}')
        else:
            images_dict = json.loads(request.POST.get('images'))
            album_type = images_dict["saveLocation"] # Rovate or public
            album_name = images_dict['album_name']
            
            print(f'Creating a {album_type} album for user: {request.user} name {album_name}')
            logger.info(f'Creating an {album_type} album for user: {request.user}')
            
            try:
                album = Album.objects.create(
                        user=request.user,
                        is_public= True if album_type == 'public' else False,
                        name=album_name
                    )
                print(f'ALBUM: {album.album_id}')
                album_images = []
                for image in images_dict['images']:
                    picture = Picture()
                    picture.image_file = get_image_from_data_url(image['image']['dataURL'])[0]
                    picture.name = image['image']['name']
                    picture.album_id = album.album_id
                    picture.save()

                    album_images.append(str(picture.image_id))
                
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
                    # return redirect(request.META['HTTP_REFERER'])
                    return redirect(redirect, 'bingo_main:create_bingo')

                except Exception as e:
                    print(f'>>> Bingo main: failed to save the pictures to the album. ERROR: {e}')
                    logger.error(f'>>> Bingo main: failed to save the pictures to the album. ERROR: {e}')
            except Exception as e:
                print(f'>>> bingo main: failed to create the album for {request.user}. ERROR: {e}')
                logger.error(f'>>> bingo main: failed to create the album for {request.user}. ERROR: {e}')
            
    return render(request, 'bingo_main/dashboard/create-bingo.html')

@login_required
def my_bingos(request):
    context = {}
    user = request.user

    # Get the 3x3 album pictures
    try:
        album_3x3 = Album.objects.get(user=user, board_size=3)
        pictures_3x3 = []
        for pic_id in album_3x3.pictures:
            pictures_3x3.append(Picture.objects.get(pk=pic_id))
            context['pictures_3x3'] = pictures_3x3
    except:
        # There are no 3x3 album pictures
        logger.info('No 3x3 album pictures found')
        print('No 3x3 album pictures found')
        pass

    # Get the 4x4 album pictures
    try:
        album_4x4 = Album.objects.get(user=user, board_size=4)
        pictures_4x4 = []
        for pic_id in album_4x4.pictures:
            pictures_4x4.append(Picture.objects.get(pk=pic_id))
            context['pictures_4x4'] = pictures_4x4
    except:
        # There are no 4x4 album pictures
        logger.info('No 4x4 album pictures found')
        print('No 4x4 album pictures found')
        pass

    # Get the 5x5 album pictures
    try:
        album_5x5 = Album.objects.get(user=user, board_size=5)
        pictures_5x5 = []
        for pic_id in album_5x5.pictures:
            pictures_5x5.append(Picture.objects.get(pk=pic_id))
            context['pictures_5x5'] = pictures_5x5
    except:
        # There are no 5x5 album pictures
        logger.info('No 5x5 album pictures found')
        print('No 5x5 album pictures found')
        pass


    return render(request, 'bingo_main/dashboard/my-bingos.html', context)

@login_required
def start_bingo(request):
    context = {}
    return render(request, 'bingo_main/dashboard/start-bingo.html')


@login_required
def bingo(request):
    context = {}
    return render(request, 'bingo_main/bingo.html')

@login_required
def add_money(request):
    context = {}
    return render(request, 'bingo_main/dashboard/add-money.html')

@login_required
def logout_view(request):
    context = {}
    logout(request)
    return redirect('bingo_main:bingo_main')


def game_index(request):
    context = {}
    return render(request, 'bingo_main/broadcast/index.html')

def game(request, game_id):
    context = {}
    return render(request, 'bingo_main/broadcast/game.html')

def check_card(request):
    context = {}
    return render(request, 'bingo_main/broadcast/checkCard.html')



def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)