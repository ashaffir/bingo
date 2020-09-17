from .models import Board

def create_2d_array(pictures, board_size):
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
            row.append(pictures.pop())
        extracted_array.append(row)
    return extracted_array

def check_players(picture_id,game_id):
    """Checks the players that have the picture in their board

    Args:
        picture_id (str): 
        game_id (str): 
    
    Return:
        boards (list): list of boards that have the picture
    """
    boards = Board.objects.filter(game_id=game_id, pictures__contains=[picture_id])
    return boards
