import json
import random
import logging
import itertools
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal
from django.core.signals import request_finished
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Player, Album, Board, Game, DisplayPicture
from control.models import Control

from .utils import create_2d_array

logger = logging.getLogger(__file__)

# @receiver(post_save, sender=Game)


@receiver(pre_save, sender=Game)
def game_start(sender, instance, update_fields, **kwargs):
    ''' Triggers when game starts
    '''
    if instance.pk is None:
        print(">>> SIGNALS: Game not created yet. Skipping")

    else:
        previous = Game.objects.get(id=instance.id)
        if previous.started != instance.started:
            # if instance.started:
            print(f">>> SIGNALS: Game started ID {instance.game_id}")
            logger.info(f">>> SIGNALS: Games started ID {instance.game_id}")
            # Updating WS
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(instance.game_id), {
                    'type': 'game.message',
                    'data': {
                            'game_status': 'game_started'
                    }
                }
            )
        elif previous.ended != instance.ended:
            # if instance.started:
            print(f">>> SIGNALS: Game ended ID {instance.game_id}")
            logger.info(f">>> SIGNALS: Games ended ID {instance.game_id}")
            # Updating WS
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(instance.game_id), {
                    'type': 'game.message',
                    'data': {
                            'game_status': 'game_ended_status'
                    }
                }
            )

        # if len(previous.players_list) != len(instance.players_list):
        #     print(
        #         f">>> SIGNALS: Updating number of players to {len(instance.players_list)} and price to {instance.price}")
        #     logger.info(
        #         f">>> SIGNALS: Updating number of players to {len(instance.players_list)} and price to {instance.price}")
        #     # Updating WS
        #     channel_layer = get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         str(instance.game_id), {
        #             'type': 'game.message',
        #             'data': {
        #                     'players_count': len(instance.players_list),
        #                     'price': instance.price
        #             }
        #         }
        #     )


@receiver(pre_save, sender=Game)
def next_picture(sender, instance: Game, **kwargs):
    if instance.pk is None:
        pass
    else:
        previous = Game.objects.get(game_id=instance.game_id)
        if previous.current_picture != instance.current_picture:
            if instance.game_in_progress:
                print(f'Game in progress.....')
                game_status = 'running' # no meaning, just for show
            elif instance.started:
                game_status = 'game_started'
                instance.game_in_progress = True
                instance.save()

            # Updating WS
            try:
                drawn_pics = instance.shown_pictures
                # Extracting the display pictures list
                drawn_obj_list = []
                for pic in drawn_pics:
                    drawn_obj_list.append(DisplayPicture.objects.filter(image=pic, game_id=instance.game_id))

                drawn_list = []
                for disp_list in drawn_obj_list:
                    for disp in disp_list:
                        try:
                            drawn_list.append(disp.pk)
                        except:
                            pass

                print(f"DRAWN LIST: {drawn_list}")    

                display_pics = DisplayPicture.objects.filter(image=instance.current_picture, game_id=instance.game_id)
                disp_ids = []
                for disp_pic in display_pics:
                    disp_pic.matched = True
                    disp_pic.save()
                    disp_ids.append(disp_pic.pk)
                
                active_boards = [pic.board for pic in display_pics]
                print(f"ACTIVE BORDS: {active_boards}")
            except Exception as e:
                print(f"DISP NOT FOUND: {e} INSTANCE PIC: {instance.current_picture}  GAME ID: {instance.game_id}")
                disp_ids = 'none'
            

            print(f">>> SIGNALS @next_picture: PIC: {instance.current_picture} DISP_ID: {disp_ids}")
            logger.info(f">>> SIGNALS @next_picture: PIC: {instance.current_picture}, URL {instance.current_picture.image_file.url}")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(instance.game_id), {
                    'type': 'game.message',
                    'data': {
                            'data': instance.current_picture.image_file.url,
                            'disp_ids': disp_ids,
                            'drawn_list':drawn_list,
                            'auto_match': instance.auto_matching,
                            'title': instance.current_picture.title,
                            'current_winning_conditions': instance.current_winning_conditions,
                            'game_status': game_status
                        }
                    }
                )

        else:
            pass
    
    


@receiver(pre_save, sender=Player)
def player_approval_signal(sender, instance: Player, **kwargs):
    ''' 
    This check is only for the non-public games
    When a new player created this check will get to default because
    the previous and currnet states of approved and not approved are same.
    '''
    if instance.pk is None:
        print(f"Skip Player Instance")

    else:
        # print(f">>> SIGNALS@approval: Checking player approval: {instance}")
        # logger.info(f">>> SIGNALS: Checking player approval: {instance}")
        try:
            previous = Player.objects.get(pk=instance.pk)
            game = instance.game
            if previous.approved != instance.approved:
                print(f">>> SIGNALS@approval: Player: {instance.pk} approved")
                logger.info(
                    f">>> SIGNALS@approval: Player: {instance.pk} approved")

                # Updating game
                game.number_of_players += 1
                game_cost = cost_calculation(game.number_of_players)
                game.game_cost = game_cost
                game.save()

                # Updating the board number (Ticket number)
                player_board = Board.objects.get(player=instance)
                player_board.board_number = game.number_of_players
                player_board.save()

                # Updating WS
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(instance.player_game_id), {
                        'type': 'game.message',
                        'data': {
                                'player_id': str(instance.pk),
                                'player_status': 'approved',
                                'players_count': game.number_of_players,
                                'price': game_cost
                        }
                    }
                )
                # print(f">>> SINGLAS@approval: WS message sent {instance.pk}")
                # logger.info(f">>> SINGLAS@approval: WS message sent {instance.pk}")

            elif previous.not_approved != instance.not_approved:
                print(
                    f">>> SIGNALS @approval: Player: {instance.pk} NOT approved")
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(instance.player_game_id), {
                        'type': 'game.message',
                        'data': {
                                'data': {
                                    'player_id': str(instance.pk),
                                    'player_status': 'not_approved'
                                }

                        }
                    }
                )
            else:
                pass
        except Exception as e:
            print(f">> SIGNALS@approval: player approval check. E: {e}")
            logger.info(f">> SIGNALS@approval: player approval check. E: {e}")


@receiver(post_save, sender=Player)
def new_player_signal(sender, instance, update_fields, **kwargs):
    """Handling the tasks for creating the board per each new user

    Args:
        sender (Player): new player created
        instance (Player)
    """
    if kwargs['created']:
        print(f'>>> SIGNALS@new_player: Player {instance.pk} created')
        logger.info(f'>>> SIGNALS@new_player: Player {instance.pk} created')

        game = instance.game

        # Updating game players list
        if game.auto_join_approval:
            instance.approved = True
            instance.save()

        game.players_list.append(str(instance.player_id))
        player_game_id = instance.player_game_id
        board_size = game.board_size
        album = game.album
        pictures = album.pictures

        game_approved_players = Player.objects.filter(game=game, approved=True)
        players_count = len(game_approved_players)
        free_players = Control.objects.get(name='free_players').value_integer

        players_count_for_cost = players_count - free_players
        game_cost = cost_calculation(players_count_for_cost)

        game.game_cost = game_cost
        game.number_of_players = players_count
        game.save()

        pictures_list = []
        for pic in pictures:
            pictures_list.append(pic)

        # Randomize the board
        shuffle_board = shuffle_pictures(pictures_list, board_size)
        # print('SUFFLE', shuffle_board)

        player_board = Board.objects.create(
            player=instance,
            game_id=player_game_id,
            board_number=game.number_of_players,
            size=board_size
        )
        
        try:
            board_array = create_2d_array(shuffle_board, board_size, player_game_id, player_board)
            print(f'>>> SIGNALS @ new_player_signal: PLAYER BOARD: {board_array}')
        except Exception as e:
            print(
                f'>>> SIGNALS @ new_player_signal: failed creating a board for a player. ERROR: {e}')
            logger.error(
                f'>>> SIGNALS @ new_player_signal: failed creating a board for a player. ERROR: {e}')
            board_array = []

        player_board.pictures = board_array
        player_board.pictures_draw = board_array
        player_board.save()

        # Updating WS
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(instance.player_game_id), {
                'type': 'game.message',
                'data': {
                        'players_count': players_count,
                        'price': game_cost
                }
            }
        )

        logger.info(
            f'>>>SIGNALS@new_player: PLAYER BOARD CREATED ID: {player_board}')
        print(
            f'>>>SIGNALS@new_player: PLAYER BOARD CREATED ID: {player_board}')

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
            # shuffled_board.append(pictures[i]['remote_id']) # Cloudinary
            # print(f'PIC: {pictures[i]}')
            shuffled_board.append(pictures[i])
    else:
        print('ERROR: Not enough images in the album')
        return None

    return shuffled_board


def cost_calculation(players_count):
    try:
        base_price = Control.objects.get(name='base_price').value_float
    except Exception as e:
        print(
            f">>> SIGNALS: Missing Control for base_price. ERROR: {e}")
        logger.error(
            f">>> SIGNALS: Missing Control for base_price. ERROR: {e}")
        base_price = 0.1

    if players_count > 0:
        try:
            game_cost = round(players_count * base_price, 2)
            # if players_count <= Control.objects.get(name="free_players").value_integer:
            #     game_cost = 0.0
            # if players_count < 21:
            #     game_cost = round(players_count * base_price, 2)
            # elif players_count < 41:
            #     game_cost = round(players_count * base_price*0.80, 2)
            # else:
            #     game_cost = round(players_count * base_price*0.66, 2)
        except Exception as e:
            print(
                f">>> SIGNALS: Missing Control for free_players. ERROR: {e}")
            logger.error(
                f">>> SIGNALS: Missing Control for free_players. ERROR: {e}")
            game_cost = 0.1
    else:
        game_cost = 0

    return game_cost
