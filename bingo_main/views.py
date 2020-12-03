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
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from control.models import Control
from .forms import ContactForm, HostSignupForm, LoginForm
from .models import ContentPage
from .utils import get_image_from_data_url
from game.models import Picture, Album, Game, Player, Board
from game.utils import check_players, random_game_id
from users.models import User
from users.utils import send_mail

logger = logging.getLogger(__file__)


def bingo_main(request):
    context = {}
    try:
        section_a = ContentPage.objects.get(section='a')
        context['section_a'] = section_a
        section_b = ContentPage.objects.get(section='b')
        context['section_b'] = section_b
        section_c = ContentPage.objects.get(section='c')
        context['section_c'] = section_c
    except Exception as e:
        pass

    return render(request, 'bingo_main/index.html', context)


def bingo_main_register(request):
    context = {}
    if request.method == 'POST':
        form = HostSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # add employer to db with is_active as False
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
                messages.error(request, f"Wrong Credentials")
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
            messages.success(
                request, 'Your message was sent. We will be in touch soon')
            # return redirect(request.META['HTTP_REFERER'])
            return redirect('bingo_main:bingo_main')
        else:
            messages.error(
                request, 'Your message was not sent. Please try again later')
            logger.error('>> BING MAIN: Error sending contact us message')
            return redirect('bingo_main:bingo_main')

    return render(request, 'bingo_main/contact.html')


@login_required
def update_profile(request):
    print(f'>> VIEWS MAIN: Profile data: {request.POST}')
    if request.method == 'POST':
        name = request.POST.get('name')
        company_name = request.POST.get('company')
        # country = request.POST.get('country')
        vat = request.POST.get('vat')
        profile_pic = request.FILES.get("complogo")

        user = request.user
        if name != '':
            user.name = name

        if company_name != '':
            print(f'COMPANY NAME: {company_name}')
            user.company_name = company_name

        # if country != 'none':
        #     user.country = country

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

    # if request.method == 'POST':
    # try:
    #     pictures = Picture.objects.filter(public=True)
    # except Exception as e:
    #     messages.info(request, '>> VIEWS MAIN: Failed getting pictures from DB. ERROR: {e}')
    #     logger.error(f'>> VIEWS MAIN: Failed getting pictures from DB. ERROR: {e}')
    #     return render(request, 'bingo_main/dashboard/index.html', context)

    # if len(pictures) >= 18:
    #     public_3x3 = []
    #     for i in range(18):
    #         public_3x3.append(pictures[i])
    # else:
    #     public_3x3 = 'none'

    # if len(pictures) >= 32:
    #     public_4x4 = []
    #     for i in range(32):
    #         public_4x4.append(pictures[i])
    # else:
    #     public_4x4 = 'none'

    # if len(pictures) >= 54:
    #     public_5x5 = []
    #     for i in range(54):
    #         public_5x5.append(pictures[i])
    # else:
    #     public_5x5 = 'none'

    # # print(f'P3: {public_3x3} P4: {public_4x4} P5: {public_5x5}')
    # logger.info(f'P3: {public_3x3} P4: {public_4x4} P5: {public_5x5}')
    # context['public_3x3'] = public_3x3
    # context['public_4x4'] = public_4x4
    # context['public_5x5'] = public_5x5

    return render(request, 'bingo_main/dashboard/index.html', context)


@login_required(login_url='bingo_main:bingo_main_login')
def create_bingo(request, album_id=''):
    context = {}

    if album_id != '':
        album = Album.objects.get(pk=album_id)
        print(f'ALBUM: {album}')
        context['current_album'] = album

    if request.method == 'POST':
        if 'updateProfile' in request.POST:
            print(f'UPDATE: {request.POST}')
        else:
            images_dict = json.loads(request.POST.get('images'))
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
                    name=album_name
                )

                print(f'>>> BINGO MAIN: Album created {album.album_id}')
                logger.info(f'>>> BINGO MAIN: Album created {album.album_id}')

                if album_type == 'public':
                    # Send email to admin for approval
                    print(">>> BINGO MAIN: Send email to admin for approval")
                    logger.info(
                        ">>> BINGO MAIN: Send email to admin for approval")

                    messages.info(
                        request, "Your new Bingo Album is pending approval for public view")

                    try:
                        subject = "Public Images Approval Request"
                        title = "Public images approval"
                        album = album

                        message = {
                            'title': title,
                            'user': request.user,
                            'album': album,
                        }

                        send_mail(subject, email_template_name=None,
                                  context=message, to_email=[
                                      settings.ADMIN_EMAIL],
                                  html_email_template_name='bingo_main/emails/admin_email.html')
                    except Exception as e:
                        logger.error(
                            f'>>> BINGO MAIN: Failed sending admin email for public album approval. ERROR: {e}')

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
    user = request.user
    albums = Album.objects.filter(user=user)
    albums_images = []
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


@api_view(['GET', ])
def check_game_id(request):
    print(f'GAME REQUEST: {request.GET.keys()}')
    try:
        game = Game.objects.get(game_id=request.GET.get("code"))
        name = request.GET.get("name")
        print(f'NAME: {request.GET.get("name")}. TYPE: {type(name)}')
        game_id = game.game_id
        print(f'GAME ID: {game_id}')

        if game.is_finished or game.started or game.ended:
            return Response(data={"message": "Game entry finished"}, status=400)

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
        return Response(data=player.pk, status=200)
    except Exception as e:
        print(f'NO GAME: {e}')
        return Response(data={'message': "Game ID does not exist"}, status=400)
    # return redirect(request.META['HTTP_REFERER'])


def players_approval_list(request, game_id):
    context = {}
    unapproved_players_list = Player.objects.filter(
        player_game_id=game_id, approved=False, not_approved=False)
    context['unapproved_players_list'] = unapproved_players_list

    return render(request, 'bingo_main/partials/_players_approval_list.html', context=context)


@login_required
def game_status(request, game_id):
    context = {}
    game = Game.objects.get(user=request.user, game_id=game_id)

    # Collecting the Players
    try:
        if game.auto_join_approval:
            players = Player.objects.filter(player_game_id=game_id)
        else:
            players = Player.objects.filter(
                player_game_id=game_id, approved=True)

        players_list = []
        for player in players:
            player_data = {}
            player_data['nickname'] = player.nickname
            player_data['player_id'] = str(player.player_id)
            players_list.append(player_data)

        game.players_list = players_list

        game.number_of_players = len(players)

        # Setting up the price for the game
        # TODO: Define pricing accurately

        try:
            base_price = Control.objects.get(name='base_price').value_float
        except:
            base_price = 0.1

        if players:
            if len(players) <= Control.objects.get(name="free_players").value_integer:
                game_cost = 0.0
            elif len(players) < 21:
                game_cost = round(len(players) * base_price, 2)
            elif len(players) < 41:
                game_cost = round(len(players) * base_price*0.80, 2)
            else:
                game_cost = round(len(players) * base_price*0.66, 2)
        else:
            game_cost = 0

        game.game_cost = game_cost
        game.save()

    except Exception as e:
        print(f'>> BING MAIN: There are no players. ERROR: {e}')
        logger.error(
            f'>> BINGO MAIN: No players found for this game. ERROR: {e}')

    context['num_players'] = len(game.players_list)
    context['game_cost'] = game.game_cost

    return render(request, 'bingo_main/partials/_game_status.html', context)


@login_required
def player_approval(request, player_id, approval):
    context = {}
    player = Player.objects.get(pk=player_id)
    print(f'Player: {player}')
    print(f'Approval: {approval}')
    if approval == 'ok':
        player.approved = True
    elif approval == 'no':
        player.not_approved = True

    player.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def start_bingo(request):
    context = {}

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
                messages.success(request, 'A new bingo game was created')
            except Exception as e:
                print(
                    f'>>> bingo main: failed creating a new game. ERROR: {e}')
                logger.error(
                    f'>>> bingo main: failed creating a new game. ERROR: {e}')
                messages.error(
                    request, 'Failed creating the new bingo game. Please try again later')
                return render(request, 'bingo_main/dashboard/start-bingo.html')
        else:
            game = Game.objects.last()
            print(f'START BROADCAST DATA')

            join_status = json.loads(request.POST.get('game_data'))[
                'joinStatus']  # Auto/Request
            game.auto_join_approval = True if join_status == 'Auto' else False

            prizes = json.loads(request.POST.get('game_data'))['prizes']
            if len(prizes) == 1:
                game.prize_1_name = prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(
                    prizes[0]["prizeImage"]['dataURL'])[0]
                game.winning_conditions = 'bingo'
                logger.info('One prize game selected')
                print('One prize game selected')
            elif len(prizes) == 2:
                game.prize_1_name = prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(
                    prizes[0]["prizeImage"]['dataURL'])[0]
                game.prize_2_name = prizes[1]["prizeName"]
                game.prize_2_image_file = get_image_from_data_url(
                    prizes[1]["prizeImage"]['dataURL'])[0]
                game.winning_conditions = '1line'
                logger.info('Two prize game selected')
                print('Two prize game selected')
            elif len(prizes) == 3:
                game.prize_1_name = prizes[0]["prizeName"]
                game.prize_1_image_file = get_image_from_data_url(
                    prizes[0]["prizeImage"]['dataURL'])[0]
                game.prize_2_name = prizes[1]["prizeName"]
                game.prize_2_image_file = get_image_from_data_url(
                    prizes[1]["prizeImage"]['dataURL'])[0]
                game.prize_3_name = prizes[2]["prizeName"]
                game.prize_3_image_file = get_image_from_data_url(
                    prizes[2]["prizeImage"]['dataURL'])[0]
                game.winning_conditions = '2line'
                logger.info('Three prize game selected')
                print('Three prize game selected')

            game.save()

    return render(request, 'bingo_main/dashboard/start-bingo.html')


@login_required
def broadcast(request):
    context = {}
    current_game = Game.objects.filter(user=request.user).last()
    context['current_game'] = current_game

    unapproved_players_list = Player.objects.filter(
        player_game_id=current_game.game_id, approved=False, not_approved=False)
    context['unapproved_players_list'] = unapproved_players_list

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
        messages.error(request, 'Game already played.')
        # return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect(reverse('bingo_main:game_over', args=[game.game_id]))

    host = request.user

    # Checking if there are minimum players
    try:
        min_players = Control.objects.get(name='min_players').value_integer
    except Exception as e:
        min_players = 2

    if len(game.players_list) < min_players:
        messages.error(
            request, f"Not enough players... Need at leaset {min_players} tikets")
        return redirect(request.META['HTTP_REFERER'])

    # print(f'GAME COST: {game.game_cost}')

    # Billing: Check user's balance and deduct the amount
    current_balance = host.balance
    game_cost = game.game_cost
    new_balance = current_balance - game_cost
    if new_balance > 0:
        # Updating user new balance
        host.balance = new_balance
        host.save()

    else:
        messages.error(
            request, 'There is not enough funding for this game. Please deposit more funds.')
        return redirect('bingo_main:add_money')

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

            current_shown_pictures_id = game.shown_pictures
            current_shown_pictures_id.append(rand_item)
            game.shown_pictures = current_shown_pictures_id
            game.current_picture = Picture.objects.get(pk=picture_draw)

            game.save()

            current_shown_pictures = []
            for p in current_shown_pictures_id:
                current_shown_pictures.append(Picture.objects.get(pk=p))

            context['remaining_pictures'] = len(pictures_pool_list)
            context['current_picture'] = Picture.objects.get(pk=picture_draw)
            # context['current_shown_pictures'] = current_shown_pictures
            context['current_shown_pictures'] = current_shown_pictures if len(
                current_shown_pictures) <= 6 else current_shown_pictures[-6:]

            context['current_shown_pictures_count'] = len(
                current_shown_pictures)

            # Check the players' boards:
            active_boards = check_players(
                picture_id=picture_draw, game_id=game_id)
            print(f'ACTIVE BOARDS: {active_boards}')

            picture_draw_id = picture_draw

            for board in active_boards:
                # print(f'>> Pic: {picture_draw_id}')
                # print(f'>> B: {board.pictures_draw}')
                player = Player.objects.get(board_id=board.pk)
                x_count_full = 0
                for i in range(board.size):
                    x_count_row = 0

                    # 1) Replace the hits with an X
                    board.pictures_draw[i] = [
                        pic if pic != picture_draw_id else 'X' for pic in board.pictures_draw[i]]

                    # Count the 'X's are on the board
                    x_count_full += board.pictures_draw[i].count('X')
                    print(f'X count: {x_count_full} Player: {player.nickname}')

                    # Count the 'X's are on the row
                    x_count_row += board.pictures_draw[i].count('X')

                    if x_count_row == board.size:

                        print(
                            f'BINGO ROW: Player {player.nickname} Row {i} board {board} Ticket: {board.board_number}!!!')

                        if game.prizes_won == []:
                            game.prizes_won.append('1line')
                            player.winnings.append('1line')

                        elif '1line' in player.winnings and x_count_full % board.size == 0:
                            player.winnings.append('2line')
                            game.prizes_won.append('2line')
                            print(
                                f'BINGO TWO ROWS: Player {player.nickname} board {board}!!!')

                        else:
                            player.winnings.append('1line')

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

                # print(f'>> UPDATED B: {board.pictures_draw}')
                # print(f'>> X-FULL Count: {x_count_full}')
                if x_count_full == board.size ** 2:
                    player = Player.objects.get(board_id=board.pk)
                    player.winnings.append('bingo')
                    player.save()
                    print(
                        f'BINGO FULLLLL!!! Player {player.nickname} Board: {board}')
                    logger.info(
                        f'BINGO FULLLLL!!! Player {player.nickname} Board: {board}')

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

        # Validating ticket number
        if ticket_number == '' or int(ticket_number) < 0:
            messages.error(request, "Please enter a valid card number")
            return render(request, 'bingo_main/broadcast/check_board.html', context)
        elif int(ticket_number) > len(current_game.players_list):
            messages.error(request, "Ticket is not a part of this game")
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
                    elif '1line' in winning_player.winnings and not current_game.prize_2_locked:
                        context['prize_2'] = True
                        win = True
                        current_game.prize_2_won = True

                    current_game.save()

                else:
                    win = False

                if win:
                    print(f'RESULT: WIN')
                    context['check_result'] = 'WIN'
                    return render(request, 'bingo_main/broadcast/checkResult.html', context)

        print(f'RESULT: Wrong')
        context['check_result'] = 'Wrong'
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
            board_pictures.append(Picture.objects.get(pk=pic))
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


@api_view(['GET', ])
def player_card(request, game_id, player_id, user_id):
    print('Polling game start status....')
    context = {}
    host = User.objects.get(pk=user_id)
    try:
        game = Game.objects.get(user=host, game_id=game_id)
    except Exception as e:
        print(f'ERROR: {e}')
    # player = Player.objects.get(pk=player_id)
    # board = Board.objects.get(player=player)
    # context['game'] = game
    # context['board'] = board
    if game.started:
        return Response(status=200)
    else:
        return Response(status=500)
    # return render(request, 'bingo_main/partials/_player_board.html', context)


@login_required
def add_money(request):
    context = {}
    if request.method == 'POST':
        if 'paypal_payment' in request.POST:
            money = request.POST.get('money')
            if money:
                amount = money
            else:
                amount = request.POST.get('deposit_amount')

            if amount != '':
                return HttpResponseRedirect(reverse('payments:paypal_payment', args=[amount]))
            else:
                messages.error(
                    request, 'Please enter an amount, or pick pf the predefined amounts.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif 'stripe_payment' in request.POST:
            money = request.POST.get('money')
            if money:
                amount = money
            else:
                amount = request.POST.get('deposit_amount')

            if amount != '':
                return HttpResponseRedirect(reverse('payments:stripe_payment', args=[amount]))
            else:
                messages.error(
                    request, 'Please enter an amount, or pick pf the predefined amounts.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'bingo_main/dashboard/add-money.html')


@login_required
def logout_view(request):
    context = {}
    logout(request)
    return redirect('bingo_main:bingo_main')


def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
