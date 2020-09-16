def extract_winning_conditions(pictures, board_size,winning_conditions):
    """This routin will run for every new player, and will generate
    a list of all possible winning patters for the player's board

    Args:
        pictures (list): list of pictures in the board
        board_size (int): 
        winning_conditions (list): which conditions need to be extracted
    
    Return: 
        extracted_winnings (list of list)
    """
    extracted_winnings = []
    
    for cond in winning_conditions:
        if cond == 'rows':
            for pic in pictures:
                row = []
                for i in range(board_size-1):
                    row.append(pic)


