import logging

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action

from users.models import User
from .models import Album, Picture, Game, Player
from . import serializers

logger = logging.getLogger(__file__)

@api_view(['GET','POST',],)
@permission_classes((IsAuthenticated,))
def pictures(request):
    data = {}

    if request.method == 'POST':
        album = request.data['album_id']
    elif request.method == 'GET':
        album = request.GET.get('album_id')
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

    pictures = Picture.objects.filter(album=album).values()
    pictures_list = []
    for picture in pictures:
        print(f'PICTURE: {picture}')
        serializer = serializers.PicturesSerializer(picture, data=request.data)
        if serializer.is_valid():
            pictures_list.append(picture)
        else:
            print(f'Failed picture serializing. ERROR: {serializer.errors}')
    data['pictures'] = pictures_list
    data['response'] = f'Picture for album: {album}'

    if len(pictures_list) == 0:
        return Response(data='No Pictures', status=status.HTTP_200_OK)
    else:
        return Response(data)


@api_view(['GET',],)
def public_albums(request):
    """Access to public albums
    """
    data = {}
    if request.method == 'GET':
        _public_albums = Album.objects.filter(is_public=True)
        albums_list = []
        for album in _public_albums:
            serializer = serializers.AlbumSerializer(album, data=request.data) 
            if serializer.is_valid():
                albums_list.append(serializer.data)
            else:
                print(f'Failed picture serializing. ERROR: {serializer.errors}')
                logger.error(f'Failed picture serializing. ERROR: {serializer.errors}')

        data['response'] = 'Public albums'
        data['albums'] = albums_list
        return Response(data)

@api_view(['POST', 'GET', 'PUT'],)
@permission_classes((IsAuthenticated,))
def albums(request):
    '''
    Retreive albums: either public ones or per user
    API endpoints: 
    /api/game/albums/album_id=<ALBUM ID> for particular user album (the one that is logged in)
    /api/game/albums/ for all user albums

    Create 
    '''
    data = {}
    if request.method == 'GET':
        query = request.GET.get('album_id')

        if query is not None:
            user_album = Album.objects.get(pk=query)
            serializer = serializers.AlbumSerializer(user_album, data=request.data)
            if serializer.is_valid():
                data['response'] = f'User album id {query}'
                data['album'] = serializer.data
                return Response(data)
            else:
                print(f'Failed picture serializing. ERROR: {serializer.errors}')
                data['response'] = f'No album found for id {query}'
                return Response(data)
        else:
            print('>> Getting all user albums')
            user_albums = Album.objects.filter(Q(user=request.user))
            albums_list = []
            for album in user_albums:
                serializer = serializers.AlbumSerializer(album, data=request.data)
                if serializer.is_valid():
                    albums_list.append(serializer.data)
            data['response'] = f'All albums for user: {request.user}'

            # print(f'ERROR GETTNIG ALL ALBUMS')
            # data = serializer.errors
            data['albums'] = albums_list
            return Response(data)

    # Update album
    elif request.method == 'PUT':

        try:
            album = Album.objects.get(album_id=request.GET.get('album_id'))
        except Album.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.AlbumSerializer(album, data=request.data)
        data = {}
        if serializer.is_valid():
            updated_album = serializer.save()
            data = serializer.data
            data['response'] = 'Update successful'
        else:
            data['response'] = "Update failed."        
        
        return Response(data)


    # Create new album
    elif request.method == 'POST':
        data = {}
        print(f'New Album request: {request.data}')
        album_name = request.data['name']
        user = request.user
        pictures = request.data['pictures']
        board = request.data['board']
        
        album = Album()
        album.name = album_name
        album.user = user
        album.pictures = pictures
        album.board = board
        album.number_of_pictures = len(pictures[0])
        album.save()

        for pic in pictures[0]:
            image = Picture()
            image.name = pic
            image.album = album
            image.url = pictures[0][f'{pic}']['url']
            image.remove_id = pictures[0][f'{pic}']['remote_id']
            image.save()


        serializer = serializers.AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            data = serializer.data
        else:
            return Response('ERROR SERIALIZING NEW ALBUM')

        return Response(data)

    return Response(status.HTTP_400_BAD_REQUEST)
 

    # return Response(data='Images loaded', status=status.HTTP_200_OK)

################ NOT USED ###################
class UserAlbumsView(viewsets.ModelViewSet):
    serializer_class = serializers.AlbumSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    # queryset = Order.objects.all()
    @action(methods=['POST', ], detail=False)
    def get_queryset(self, *args, **kwargs):
        # queryset_list = Album.objects.all()
        user = self.request.user
        queryset_list = queryset_list.filter(Q(user=user))
        print(f'USER {user}  Albums: {queryset_list}')

        return queryset_list

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def game_create(request):
    data = {}
    # info = {}
    if request.method == 'POST':
        user = request.user
        # album_id = Album.objects.get(user=request.user, name=request.data['album_name'])

        # info['winning_conditions'] = request.data['winning_conditions']
        # info['is_public'] = request.data['is_public']
        # info['prizes'] = request.data['prizes']

        
        serializer = serializers.GameSerializer(data=request.data)

        if serializer.is_valid():
            game = serializer.save()

            data['response'] = "Game is ready"
            data['game_id'] = game.game_id
            data['album_id'] = game.album
            data['winning_conditions'] = game.winning_conditions
            data['is_public'] = game.is_public
            data['prizes'] = game.prizes
            data['user_id'] = user.pk
            # data['album_id'] = album_id.pk

            game.user = user
            # game.album_id = album_id
            game.save()
            return Response(data)
        else:
            data['response'] = "Failed preping the game."
            data['errors'] = serializer.errors
            return Response(data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def game_request(request):
    '''
    Calculating the price for the game according to the number of players joined.
    '''
    data = {}
    if request.method == 'POST':

            game = Game.objects.get(user=request.user, game_id=request.data['game_id'])
            game.game_requested = True

            # Collecting the Players
            try:
                players = Player.objects.filter(player_game_id=request.data["game_id"])
                players_list = []
                for player in players:
                    player_data = {}
                    player_data['nickname'] = player.nickname
                    player_data['player_id'] = str(player.player_id)
                    players_list.append(player_data)

                game.players_list = players_list

                game.number_of_players = len(players)

                #Setting up the price for the game
                # TODO: Define pricing accurately
                if players:
                    if len(players) < 21:
                        game_cost = round(len(players) * 1/20,2)
                    elif len(players < 41):
                        game_cost = round(len(players) * 1/25,2)
                    else:
                        game_cost = round(len(players) * 1/30,2)
                else:
                    game_cost = 0
                
                data['game_cost'] = game_cost
                data['num_of_players'] = len(players)
                game.game_cost = game_cost
                game.save()
                return Response(data)
            except Exception as e:
                print(f'There are no players. ERROR: {e}')
                logger.error(f'No players found for this game. ERROR: {e}')
                return Response(status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response('Bad request', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def game_confirm(request):
    '''
    - Host to confirm the game
    - Checking that the user's balanace can cover the cost of the game
    '''
    data = {}
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        game = Game.objects.get(user=request.user.pk, game_id=request.data['game_id'])

        # Check user's balance and deduct the amount
        current_balance = user.balance
        game_cost = game.game_cost
        new_balance = current_balance - game_cost
        if new_balance > 0: 
            # Updating user new balance
            user.balance = new_balance
            user.save()

            # Start the game
            game.started = True
            game.save()
            data['response'] = 'Game Started'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['response'] = 'Not enough balance'
            return Response(data)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@login_required
def game_control(request):
    context = {}
    if request.method == 'POST':
        if 'gamePrep' in request.POST:
            album = Album.objects.filter(user=request.user).first()
            new_game = Game.objects.create(
                album_id=album,
                user = request.user,
                winning_conditions='ALL',
                is_public=True
            )

            try:
                context['game'] = new_game
                context['album'] = album.name
                context['winning_cond'] = 'ALL'
                context['is_public'] = 'Public Game'
            except Exception as e:
                context['game'] = new_game
                context['album'] = 'There are no albums for this user'
                context['winning_cond'] = 'ALL'
                context['is_public'] = 'Public Game'                
            
            # return redirect('game:game-room', new_game.game_id)

        elif 'startGame' in request.POST:
            # TODO: open a WS on start of game listening to the joining of players
            game = Game.objects.filter(user=request.user).last
            context['game'] = game


        # elif 'enterGame' in request.POST:
        #     try:
        #         playerGameId = request.POST.get('playerGameId')
        #         playerNickname = request.POST.get('nickname')
        #         player = Player.objects.create(
        #             game_id = playerGameId,
        #             nickname = playerNickname if playerNickname != "" else "Bob"
        #         )
        #         print(f'Playing: {playerGameId}')
        #         context['played_game'] = playerGameId
        #     except Exception as e:
        #         messages.error(request, 'Please enter a valid game id')
        #         return redirect(request.META['HTTP_REFERER'])

        else:
            context['next'] = "NEXT IMAGE"

    #TODO: What happend on game complete?, e.g. is_finished is set to true

    return render(request, 'game/game-control.html', context)

def home(request):
    context = {}
    return render(request, 'game/home.html', context)


def game_room(request, game_id):
    ''' For testing purposes. Room game demo
    '''

    context = {}
    game = Game.objects.get(game_id=game_id)

    if request.method == 'POST':
        if 'requestGame' in request.POST:
            # TODO: Delete game data to oavoid future collisions
            
            # Setting game to started
            game = Game.objects.get(user=request.user.pk, game_id=game_id)
            game.game_requested = True

            # Collecting the Players
            _players = Player.objects.filter(player_game_id=game_id)
            game.player_list = _players

            game.number_of_players = len(_players)

            #Setting up the price for the game
            # TODO: Define pricing accurately
            if _players:
                if len(_players) < 21:
                    game.game_cost = round(len(_players) * 1/20,2)
                elif len(_players < 41):
                    game.game_cost = round(len(_players) * 1/25,2)
                else:
                    game.game_cost = round(len(_players) * 1/30,2)

            print(f'COST: {game.game_cost}')            
            game.save()
        elif 'conirmed' in request.POST:
            user = User.objects.get(pk=request.user.pk)
            game = Game.objects.get(user=request.user.pk, game_id=game_id)
            game.game_requested = False

            # Check user's balance and deduct the amount
            current_balance = user.balance
            game_cost = game.game_cost
            new_balance = current_balance - game_cost
            if new_balance > 0: 
                # Updating user new balance
                user.balance = new_balance
                user.save()

                # Start the game
                game.started = True
                game.save()
                print(f'GAME STARTED')            


    context['game'] = game

    return render(request, 'game/game_room.html',context)

def players(request, user_id, game_id):
    ''' For generating the dynamic players table created with websocket
    '''
    context = {}
    _players = Player.objects.filter(player_game_id=game_id)
    context['players'] = _players
    return render(request, 'game/players.html', context)