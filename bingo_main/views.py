import logging
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .forms import ContactForm, HostSignupForm, LoginForm
from .models import ContentPage
from .utils import get_image_from_data_url
from game.models import Picture, Album, Game, Player
from users.models import User

logger = logging.getLogger(__file__)

def bingo_main(request):
    context = {}
    section_a = ContentPage.objects.get(section='a')
    context['section_a'] = section_a
    section_b = ContentPage.objects.get(section='b')
    context['section_b'] = section_b
    section_c = ContentPage.objects.get(section='c')
    context['section_c'] = section_c

    return render(request, 'bingo_main/index.html', context)

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
        
        if country != 'none':
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

    albums = Album.objects.filter(is_public=True)
    print(f'ALBUMS: {albums}')

    context['albums'] = albums

    # if request.method == 'POST':
    try:
        pictures = Picture.objects.filter(public=True)
    except Exception as e:
        messages.info(request, '>> VIEWS MAIN: Failed getting pictures from DB. ERROR: {e}')
        logger.error(f'>> VIEWS MAIN: Failed getting pictures from DB. ERROR: {e}')
        return render(request, 'bingo_main/dashboard/index.html', context)

    if len(pictures) >= 18:    
        public_3x3 = []
        for i in range(18):
            public_3x3.append(pictures[i])
    else:
        public_3x3 = 'none'

    if len(pictures) >= 32:    
        public_4x4 = []
        for i in range(32):
            public_4x4.append(pictures[i])
    else:
        public_4x4 = 'none'
    
    if len(pictures) >= 54:    
        public_5x5 = []
        for i in range(54):
            public_5x5.append(pictures[i])
    else:
        public_5x5 = 'none'

    # print(f'P3: {public_3x3} P4: {public_4x4} P5: {public_5x5}')
    logger.info(f'P3: {public_3x3} P4: {public_4x4} P5: {public_5x5}')
    context['public_3x3'] = public_3x3
    context['public_4x4'] = public_4x4
    context['public_5x5'] = public_5x5

    return render(request, 'bingo_main/dashboard/index.html', context)

@login_required(login_url='bingo_main:bingo_main_login')
def create_bingo(request):
    context = {}
    if request.method == 'POST':
        if 'updateProfile' in request.POST:
            print(f'UPDATE: {request.POST}')
        else:
            images_dict = json.loads(request.POST.get('images'))
            album_type = images_dict["saveLocation"] # Private or public
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
                    picture.public = True if album_type == 'public' else False
                    picture.save()

                    album_images.append(str(picture.image_file.url))
                
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
                    logger.info(f'Album for user {request.user} name >> {album_name} << created')
                    print(f'Album for user {request.user} name >> {album_name} << created')
                    return redirect(request.META['HTTP_REFERER'])

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

@api_view(['GET',])
def check_game_id(request):
    print(f'GAME REQUEST: {request.GET.keys()}')
    try:
        game = Game.objects.get(game_id=request.GET.get("code"))
        name = request.GET.get("name")
        print(f'NAME: {request.GET.get("name")}. TYPE: {type(name)}')
        game_id = game.game_id
        print(f'GAME ID: {game_id}')
        
        # If game exists, create new player and add it to the game players list
        player = Player.objects.create(
            nickname=name,
            game=game,
            player_game_id=game_id
        )

        # print(f'PLAYER: {player}')
        # if game.players_list:
        #     game.players_list.append(player.pk)
        #     game.save()
        # else:
        #     game.players_list = []
        #     game.players_list.append(player.pk)
        #     game.save()
        
        print(f'GAME: {game}')
        return Response(status=200)
    except Exception as e:
        print(f'NO GAME: {e}')
        return Response(data={'message':"Game ID does not exist"} , status=400)
    # return redirect(request.META['HTTP_REFERER'])
    


@login_required
def start_bingo(request):
    context = {}

    if request.method == 'POST':
        if 'make_game' in request.POST:
            # Create a game
            try:
                print(f'ID: {request.POST["make_game"]}')
                album_id = request.POST["make_game"]
                album = Album.objects.filter(board_size=album_id).last()

                game = Game()
                game.album = album
                game.board_size = album.board_size
                game.pictures_pool = album.pictures
                game.user = request.user
                game.save()
                messages.success(request, 'A new bingo game was created')
            except Exception as e:
                print(f'>>> bingo main: failed creating a new game. ERROR: {e}')
                logger.error(f'>>> bingo main: failed creating a new game. ERROR: {e}')
                messages.error(request, 'Failed creating the new bingo game. Please try again later')
                return render(request, 'bingo_main/dashboard/start-bingo.html')
        else:
            game = Game.objects.last()
            print(f'START BROADCAST DATA')

            join_status = json.loads(request.POST.get('game_data'))['joinStatus']  # Auto/Request
            game.auto_join_approval = True if join_status == 'Auto' else False   

            prizes = json.loads(request.POST.get('game_data'))['prizes']
            if len(prizes) == 1:
                game.prize_1_name =prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(prizes[0]["prizeImage"]['dataURL'])[0]
                logger.info('One prize game selected')
                print('One prize game selected')
            elif len(prizes) == 2:    
                game.prize_1_name =prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(prizes[0]["prizeImage"]['dataURL'])[0]
                game.prize_2_name =prizes[1]["prizeName"]
                game.prize_2_image_file = get_image_from_data_url(prizes[1]["prizeImage"]['dataURL'])[0]
                logger.info('Two prize game selected')
                print('Two prize game selected')
            elif len(prizes) == 3: 
                game.prize_1_name =prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(prizes[0]["prizeImage"]['dataURL'])[0]
                game.prize_2_name =prizes[1]["prizeName"]
                game.prize_2_image_file = get_image_from_data_url(prizes[1]["prizeImage"]['dataURL'])[0]
                game.prize_3_name =prizes[2]["prizeName"]
                game.prize_3_image_file = get_image_from_data_url(prizes[2]["prizeImage"]['dataURL'])[0]
                logger.info('Three prize game selected')
                print('Three prize game selected')

            game.save()

    return render(request, 'bingo_main/dashboard/start-bingo.html')

@login_required
def broadcast(request):
    context = {}
    current_game = Game.objects.filter(user=request.user).last()
    context['current_game'] = current_game
    return render(request, 'bingo_main/broadcast/index.html', context=context)


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


def game(request, game_id):
    context = {}
    return render(request, 'bingo_main/broadcast/game.html')

@login_required
def check_card(request):
    context = {}
    return render(request, 'bingo_main/broadcast/checkCard.html')



def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)