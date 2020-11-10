import json
import random
import logging
import itertools
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.signals import request_finished
from django.conf import settings

from .models import Player, Album, Board
from .utils import create_2d_array

logger = logging.getLogger(__file__)

@receiver(post_save, sender=Player)
def new_player_signal(sender, instance, update_fields, **kwargs):  
    """Handling the tasks for creating the board per each new user

    Args:
        sender (Player): new player created
        instance (Player)
    """
    if kwargs['created']:
        print(f'SIGNAL: Player {instance.pk} created')
        logger.info(f'SIGNAL: Player {instance.pk} created')
        
        game = instance.game
        player_game_id = instance.player_game_id
        board_size = game.board_size
        album = game.album
        pictures = album.pictures
        pictures_list = []
        print(f'PICTURES: {pictures}')
        for i in range(len(pictures)):
            # pictures_list.append(pictures[f'pic{i}']) # Cloudinary stuff
            pictures_list.append(pictures[i])

        # Randomize the board
        shuffle_board = shuffle_pictures(pictures_list, board_size)
        # print('SUFFLE', shuffle_board)

        try:
            board_array = create_2d_array(shuffle_board, board_size)
            print(f'PLAYER BOARD: {board_array}')
        except Exception as e:
            print(f'>>> SIGNALS: failed creating a board for a player. ERROR: {e}')
            logger.error(f'>>> SIGNALS: failed creating a board for a player. ERROR: {e}')
            board_array = []

        player_board = Board.objects.create(
        player = instance,
        game_id=player_game_id,
        size = board_size,
        pictures = board_array
        )

        logger.info(f'PLAYER BOARD CREATED: {board_array}')

        instance.board_id = player_board.pk
        # instance.board_dict = shuffle_board
        instance.save()
        
        



def shuffle_pictures(pictures, board_size):
    """Simple shuffle mechanism

    Args:
        pictures (list): list of pictures in a dict
        board_size (int): what is the size of the board

    Returns:
        [type]: [description]
    """
    # Shuffle the list
    random.shuffle(pictures)
    shuffled_board = []
    if len(pictures) > board_size**2:
        for i in range(board_size**2):
            shuffled_board.append(pictures[i]['remote_id'])
    else:
        print('ERROR: Not enough images in the album')
        return None
    
    
    return shuffled_board


