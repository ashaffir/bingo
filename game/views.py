import logging
import random
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
from .utils import check_players
from control.models import Control
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

        album_id = request.data['album_id']
        album = Album.objects.get(pk=album_id)
        # print(f'ALBUM_SER: {album_ser}')
        
        serializer = serializers.GameSerializer(data=request.data)

        if serializer.is_valid():
            game = serializer.save()

            game.album = album
            game.pictures_pool = album.pictures
            game.user = user
            game.save()

            data['response'] = "Game is ready"
            data['game_id'] = game.game_id
            data['album_id'] = game.album.pk
            data['winning_conditions'] = game.winning_conditions
            data['is_public'] = game.is_public
            data['prizes'] = game.prizes
            data['user_id'] = user.pk

            return Response(data)
        else:
            data['response'] = "Failed preping the game."
            data['errors'] = serializer.errors
            return Response(data)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

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

            try:
                base_price = Control.objects.get(name='base_price').value_float
            except:
                base_price = 0.1

            if players:
                if len(players) < 21:
                    game_cost = round(len(players) * base_price,2)
                elif len(players) < 41:
                    game_cost = round(len(players) * base_price*0.80,2)
                else:
                    game_cost = round(len(players) * base_price*0.66,2)
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


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def game_info(request):
    data = {}
    if request.method == 'GET':
        game_id = request.GET.get('game_id')
        user = request.user
        game = Game.objects.get(user=user, game_id=game_id)
        serializer = serializers.GameSerializer(game)
        data = serializer.data
        return Response(data)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def game_play(request):
    '''
    Handles the process for every click on the NEXT button
    1) Get the pictures from the pictures_pool
    2) Get a random picture from the pool
    3) Pop that picture from the pool and write it back to the DB
    4) Check which players met the winning condition
    5) Continue until "BINGO" or untill all pictures were drawn

    Request:
    - game id (error if there is no such game for the user)
    
    Return:
    - Picture ID for display
    - number of pictures pooled
    - number of pictures left
    - player IDs those who have winning conditions

    '''
    data = {}
    if request.method == 'GET':
        try:
            game_id = request.GET.get('game_id')
            game = Game.objects.get(user=request.user.pk, game_id=game_id)
        except Exception as e:
            print('No such game for this player')
            logger.error(f'No such game for this player. ERROR: {e}')
            return Response('Error game request', status=status.HTTP_400_BAD_REQUEST)


        pictures_pool_dict = game.pictures_pool[0]
        pictures_pool_list = []
        items_list = []

        # Creating a list of all keys in the dict
        if len(pictures_pool_dict) > 0:
            for pic in pictures_pool_dict:
                items_list.append(pic)

            # Drawing a random key from the dict
            picture_draw_index = random.randint(0,len(items_list)-1)
            rand_item = items_list[picture_draw_index]
            picture_draw = pictures_pool_dict.pop(rand_item)

            # Updating the DB with the reduced list of pictures
            pictures_pool_list.append(pictures_pool_dict)
            game.pictures_pool = pictures_pool_list

            current_shown_pictures = game.shown_pictures
            current_shown_pictures.append({rand_item:picture_draw})
            game.shown_pictures = current_shown_pictures

            game.save()

            data['remaining_pictures'] = len(pictures_pool_dict)
            data['picture'] = picture_draw
            data['pic_index'] = rand_item

            # Check the players' boards:
            active_boards = check_players(picture_id=picture_draw['remote_id'], game_id=game_id)
            print(f'ACTIVE BOARDS: {active_boards}')

            picture_draw_id = picture_draw["remote_id"]

            for board in active_boards:
                print(f'>> Pic: {picture_draw_id}')
                print(f'>> B: {board.pictures}')
                x_count_full = 0
                for i in range(board.size):
                    x_count_row = 0
    
                    # 1) Replace the hits with an X
                    board.pictures[i] = [pic if pic != picture_draw_id else 'X' for pic in board.pictures[i]]

                    # Count the 'X's are on the row
                    x_count_row += board.pictures[i].count('X')
                    if x_count_row == board.size:
                        player = Player.objects.get(board_id=board.pk)
                        player.winnings.append(f'row_{i}')
                        player.save()
                        print(f'BINGO: Player {player.nickname} Row {i} board {board}!!!')

                    # Count the 'X's are on the board
                    x_count_full += board.pictures[i].count('X')

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
                        if board.pictures[row][column] == 'X':
                            x_count_column += 1
                            player.winnings.append(f'row_{row}_col_{column}')

                    if x_count_column == board.size:
                        player.winnings.append(f'col_{column}')
                        print(f'BINGO: Player {player.nickname} Column {i} board {board}!!!')

                    if board.pictures[column][column] == 'X':
                        x_count_diag_left_to_right += 1

                    if x_count_diag_left_to_right == board.size:
                        player.winnings.append('diag_l2r')
                        print(f'BINGO: Player {player.nickname} Diagonal L2R board {board}!!!')


                    if board.pictures[-column-1][-column-1] == 'X':
                        x_count_diag_right_to_left += 1

                    if x_count_diag_right_to_left == board.size:
                        player.winnings.append('diag_r2l')
                        print(f'BINGO: Player {player.nickname} Diagonal R2L board {board}!!!')

                    player.save()


                # print(f'>> UPDATED B: {board.pictures}')
                # print(f'>> X-FULL Count: {x_count_full}')
                if x_count_full == board.size ** 2:
                    player = Player.objects.get(board_id=board.pk)
                    player.winnings.append('FULL')
                    player.save()
                    print(f'BINGO FULLLLL!!! Player {player.nickname} Board: {board}')
                

            return Response(data)
        else:
            game.ended = True
            game.is_finished = True
            game.save()

            return Response('Game Finished. No more pictures')
    else:
        print('Bad request at game play')
        logger.error('Bad request at game play')
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def game_winnings(request):
    """Checks the winnings for particular player

    Args:
        player_id (str):

    Returns:
        list: List of all the winnings that the player currently has
    """
    if request.method == 'GET':
        winnings_set = set()
        board_id = request.GET.get('board_id')
        game_id = request.GET.get('game_id')
        try:
            player = Player.objects.get(board_id=board_id)
            for win in player.winnings:
                winnings_set.add(win)
            
            if len(winnings_set) == 0:
                return Response('No winnings')
            else:
                return Response(winnings_set)
        except Exception as e:
            print(f'There is no such player for that game. ERROR: {e}')
            logger.error(f'There is no such player for that game. ERROR: {e}')
            return Response('Player not found.', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_players(request):
    ''' Getting the current players listed for a game
    '''
    data = {}
    if request.method == 'GET':
        game_id = request.GET.get('game_id')
        game_players = []
        _players = Player.objects.filter(game_id=game_id)
        for player in _players:
            player_obj = {}
            player_obj['id'] = player.pk
            player_obj['nickname'] = player.nickname
            player_obj['approved'] = player.approved
            game_players.append(player_obj)
        data['players'] = game_players
        return Response(data)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT',])
@permission_classes((IsAuthenticated,))
def player(request):
    """Get information about a particular player, and update his approved status

    Args:
        player_id (str): 
        game_id (str): 

    Returns:
        approved: bool
        board_id: str
    """
    if request.method == 'GET':
        player_id = request.GET.get('player_id')
        game_id = request.GET.get('game_id')
        print(f"Getting Player: {player_id}")

        data = {}
        player = Player.objects.get(player_game_id=game_id, pk=player_id)
        data['approved'] = player.approved
        data['board_id'] = player.board_id
        return Response(data)
    elif request.method == 'PUT':
        print(f'PU: {request.data}')
        player_id = request.data['player_id']
        game_id = request.data['game_id']
        player = Player.objects.get(player_game_id=game_id, pk=player_id)
        if request.data['approved'] == 'True':
            player.approved = True
        elif request.data['approved'] == 'False':
            player.approved = False
        else:
            return Response('Bad data formating', status.HTTP_400_BAD_REQUEST)
        player.save()

        return Response(f'Player approved status: {player.approved}', status=status.HTTP_200_OK)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


#################
# DEMO ONLY
#################

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