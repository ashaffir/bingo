import json
import random
import itertools
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.signals import request_finished
from django.conf import settings

from .models import Player, Album

@receiver(post_save, sender=Player)
def new_player_signal(sender, instance, update_fields, **kwargs):  
    """Handling the tasks for creating the board per each new user

    Args:
        sender (Player): new player created
        instance (Player)
    """
    if kwargs['created']:
        print(f'SIGNAL: Player {instance.pk} created')
        game = instance.game
        print(f'GAME: {game}')
        player_game_id = instance.player_game_id
        print(f'Game ID: {player_game_id}')
        board_size = game.board_size
        print(f'Board size: {board_size}')
        album = game.album
        print(f'Album: {album}')
        pictures = album.pictures[0]
        print(f'>> Pictures len: {len(pictures)}')
        pictures_list = []
        for i in range(1,len(pictures)+1):
            pictures_list.append(pictures[f'pic{i}'])

        shuffle_board = shuffle_pictures(pictures_list, board_size)
        if shuffle_board:
            print(f"Shuffled Board Size: {len(shuffle_board)}")
            instance.board = shuffle_board
            instance.save()
        else:
            print('Not enough pictures')
            # TODO: take care of this situation



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
            shuffled_board.append(pictures[i])
    else:
        print('ERROR: Not enough images in the album')
        return None
    
    
    return shuffled_board


