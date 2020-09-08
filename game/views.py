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

@api_view(['GET','POST',],)
@permission_classes((IsAuthenticated,))
def pictures(request):
    if request.method == 'GET':
        data = {}
        album = request.data['album_id']
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
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    if len(pictures_list) == 0:
        return Response(data='No Pictures', status=status.HTTP_200_OK)
    else:
        return Response(data)

@api_view(['POST', 'GET'],)
@permission_classes((IsAuthenticated,))
def albums(request):
    '''
    Retreive albums: either public ones or per user
    API endpoints: 
    /api/game/albums/ for particular user (the one that is logged in)
    /api/game/albums/?albums=all for all public

    Create 
    '''
    data = {}
    if request.method == 'GET':
        query = request.GET.get('albums')
        if query == 'public':
            public_albums = Album.objects.filter(isPublic=True)
            albums_list = []
            for album in public_albums:
                serializer = serializers.AlbumSerializer(album, data=request.data) 
                if serializer.is_valid():
                    albums_list.append(serializer.data)
                else:
                    print(f'Failed picture serializing. ERROR: {serializer.errors}')

            data['response'] = 'Public albums'
        else:
            albums = Album.objects.filter(Q(user=request.user))
            albums_list = []
            for album in albums:
                serializer = serializers.AlbumSerializer(album, data=request.data) 
                if serializer.is_valid():
                    albums_list.append(serializer.data)
            data['response'] = f'Albums for user: {request.user}'

            # print(f'ERROR GETTNIG ALL ALBUMS')
            # data = serializer.errors
        data['albums'] = albums_list
        return Response(data)

    # Create new album
    elif request.method == 'POST':
        data = {}
        print(f'DATA: {request.data}')
        album_name = request.data['name']
        user = request.user
        pictures = request.data['pictures']
        board = request.data['board']
        
        album = Album()
        album.name = album_name
        album.user = user
        album.pictures = pictures
        album.board = board
        album.number_of_images = len(pictures[0])
        album.save()

        for pic in pictures[0]:
            image = Picture()
            image.name = pic
            image.album = album
            image.url = pictures[0][f'{pic}']['url']
            image.save()


        serializer = serializers.AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            data = serializer.data
        else:
            return Response('ERROR SERIALIZING NEW ALBUM')

        # Card:{
        # Row:nubmer,
        # Column: number,
        # isEmptyCenter: boolean

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

            context['game'] = new_game
            context['album'] = album.name
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
    context = {}
    game = Game.objects.get(game_id=game_id)

    if request.method == 'POST':
        if 'requestGame' in request.POST:
            # TODO: Delete game data to oavoid future collisions
            
            # Setting game to started
            game = Game.objects.get(user=request.user.pk, game_id=game_id)
            game.game_requested = True

            # Collecting the Players
            players = Player.objects.filter(player_game_id=game_id)
            game.player_list = players

            game.number_of_players = len(players)

            #Setting up the price for the game
            # TODO: Define pricing accurately
            if len(players) < 21:
                game.game_cost = round(len(players) * 1/20,2)
            elif len(players < 41):
                game.game_cost = round(len(players) * 1/25,2)
            else:
                game.game_cost = round(len(players) * 1/30,2)

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
    context = {}
    players = Player.objects.filter(player_game_id=game_id)
    context['players'] = players
    return render(request, 'game/players.html', context)