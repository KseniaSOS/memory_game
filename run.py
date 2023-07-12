# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from helper_functions import parse_layout, create_card_frame, create_empty_frame
from classes import BoardElement, Board
from game import run_game

LAYOUT_JSON = "layout.json"

if __name__ == '__main__':
    # parse the layout
    layout = parse_layout(LAYOUT_JSON)

    # create a list of available card elements
    card_elements = []
    card_names = layout['card_elements'].keys()
    for card_name in card_names:
        element = BoardElement(card_name, layout['card_elements'][card_name], layout['frame_elements'],
                               layout['frame_size'])
        card_elements.append(element)

    # create empty board element
    empty_frame = create_empty_frame(layout['frame_size'])
    empty_frame_element = BoardElement(" ",empty_frame, layout['frame_elements'], layout['frame_size'])

    # initialize the game board
    my_board = Board(layout['board_size'], empty_frame_element)
    my_board.populate_board(card_elements)
    my_board.flip_all_elements()
    print(my_board)
    exit(0)

    # run the game
    run_game(my_board, layout['messages'])