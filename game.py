from random import randint
from time import sleep


from helper_functions import create_nested_list, check_input
from classes import Board


def display_rules():
    """
    This function displays rules in terminal
    """
    rules = """
    The objective of Memory Game is to defeat your computer opponent by
    correctly guessing a pair of cards. At the beggining of the game, all 16 cards 
    with ASCCI images will be randomply placed in the terminal. At first You will 
    need to guess the first card, then the second one. If they match, You will get 
    a point. Iterate untill all pair of cards are found."""

    return rules


def display_score(player_score, computer_score):
    """
    This functions displays players and computer score.
    """
    return print(f"Current score: player - {player_score}, computer - {computer_score}")


def player_turn(index_dict, messages: dict):
    """
    Asks the user for two input indices.
    """
    # pre-allocate some variables
    selected_indexes = []
    selected_indexes_str = []
    _index_dict = index_dict.copy()

    for i in range(2):
        # check user input
        keys = list(_index_dict.keys())
        input_value = check_input(keys, messages['input_message'], messages['error_message'])
        selected_index = _index_dict[input_value]
        selected_indexes.append(selected_index)
        selected_indexes_str.append(input_value)
        _index_dict.pop(input_value)

    return selected_indexes, selected_indexes_str


def computer_turn(index_list):
    """
    The function allows the computer to choose its cards. Draw 2 random indices from input list.
    """

    _index_list = index_list.copy()
    selected_indexes = []
    selected_indexes_str = []
    for i in range(2):
        idx = randint(0, len(_index_list) - 1)
        selected_index = _index_list[idx]
        selected_indexes.append(selected_index)
        selected_indexes_str.append(str(selected_index[0]) + str(selected_index[1]))
        _index_list.pop(idx)

    return selected_indexes, selected_indexes_str


def run_game(board: Board, layout: dict):
    """
    The functions starts a game. Prints logo and welcome messages.
    """
    print(layout["logo"])
    input("\nShall we get started? Hit Enter to continue...\n")
    user_name = input("Please enter your name:\n")
    print(f"Welcome {user_name}! Here are the rules:")
    print(display_rules())
    input("Hit Enter to continue...\n")


    # initialize scores
    player_score = 0
    computer_score = 0

    # get number of flipped cards and used board cells to initialize the game
    nb_flipped_cards = board.count_flipped_cards()
    nb_used_board_cells = board.nb_used_board_cells

    # create nested list of indexes packed in a dictionary for user input checking and element selection
    rows = list(range(board.board_size[0]))
    cols = list(range(board.board_size[1]))
    # list of board indexes
    nested_list = create_nested_list(rows, cols)
    # string versions of the board indexes (easier to use for input checking, as it is string)
    keys = [str(nested_list[x][0]) + str(nested_list[x][1]) for x in range(len(nested_list))]
    index_dict = dict(zip(keys, nested_list))

    # launch the game
    while nb_flipped_cards != nb_used_board_cells:
        # display board
        print(board)

        # player takes a turn
        selected_indexes, selected_indexes_str = player_turn(index_dict, layout['messages'])
        for i in range(2):
            board.flip_board_element(selected_indexes[i])
        print(board)

        # check if successful and update the score. Prints an appropriate message.Creates a delay before executing next code(sleep)
        if board.check_board_element_match(selected_indexes[0], selected_indexes[1]):
            player_score += 1
            print("Player successful!")
            display_score(player_score, computer_score)
            for i in range(2):
                index_dict.pop(selected_indexes_str[i])
                nested_list.remove(selected_indexes[i])
            nb_flipped_cards = board.count_flipped_cards()
        else:
            print("No luck this time!")
            for i in range(2):
                board.flip_board_element(selected_indexes[i])
        sleep(5)

        # check if all cards are already flipped by the player
        if nb_flipped_cards == nb_used_board_cells:
            break

        # computer takes a turn
        print("Computer takes a turn...")
        selected_indexes, selected_indexes_str = computer_turn(nested_list)
        for i in range(2):
            board.flip_board_element(selected_indexes[i])
        print(board)

        # check if successful and update the score
        if board.check_board_element_match(selected_indexes[0], selected_indexes[1]):
            computer_score += 1
            print("Computer successful!")
            display_score(player_score, computer_score)
            for i in range(2):
                index_dict.pop(selected_indexes_str[i])
                nested_list.remove(selected_indexes[i])
            nb_flipped_cards = board.count_flipped_cards()
        else:
            print("Computer missed this time!")
            for i in range(2):
                board.flip_board_element(selected_indexes[i])
        sleep(5)

    # finish the game and print result
    if player_score > computer_score:
        print("Congratulations! You have beat the system!")
    elif player_score == computer_score:
        print("It's a tie!")
    else:
        print("Better luck next time!")
    display_score(player_score, computer_score)