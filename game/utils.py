import random
from .models import Board, Game, Picture, DisplayPicture
from users.models import User

def create_2d_array(pictures, board_size, game_id, board):
    """This routin will run for every new player, and will generate
    the 2D array of the board

    Args:
        pictures (list): list of pictures in the board
        board_size (int): 
    
    Return: 
        extracted_array (list of list)
    """
    extracted_array = []
    for i in range(board_size):
        row = []
        for j in range(board_size):

            poped_pic_id = pictures.pop() 
            poped_pic = Picture.objects.get(pk=poped_pic_id)
            disp_pic = DisplayPicture.objects.create(
                image=poped_pic,
                board=board,
                game_id=game_id
            )

            row.append(disp_pic.pk)

            # row.append(pictures.pop())
        extracted_array.append(row)
    return extracted_array

def check_players(picture_id,game_id):
    """Checks the players that have the drawn picture on their board

    Args:
        picture_id (str): 
        game_id (str): 
    
    Return:
        boards (list): list of boards that have the picture
    """
    print(f"PIC ID: {picture_id}")
    boards = Board.objects.filter(game_id=game_id, pictures__contains=[picture_id])
    return boards

  
def random_game_id(user):
    for i in range(5):
        code = str(random.randint(1001, 9999))
        if not Game.objects.filter(game_id=code, user=user).exists():
            return code
    raise ValueError('Too many attempts to generate the code')
