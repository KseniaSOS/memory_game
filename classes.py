from random import randint
from typing import List
from helper_functions import create_card_frame, create_empty_frame, \
    merge_str_line_by_line, create_nested_list


class BoardElement:
    """
    Creates the BoardElement class where all board objects will be added.
    Indicates its state whether it is visible or not.
    """

    def __init__(self, element_name: str,
                 element_content: str, frame_elements: dict, frame_size: dict):
        self._frame_elements = frame_elements
        self._frame_size = frame_size
        self._element_content = element_content
        self._element_name = element_name
        self._card_front = create_card_frame(
            element_content, frame_elements, frame_size)
        self._card_back = create_card_frame(
            create_empty_frame(frame_size), frame_elements, frame_size)
        self.is_visible = False

    @property
    def card_front(self):
        return self._card_front

    @property
    def card_back(self):
        return self._card_back

    @card_back.setter
    def card_back(self, element_idx: List[int]):
        """
        This method sets the value of the private attribute _card_back
        and expects a list of two integers.
        Example usage: 'element.card_back = [1, 2]'
        """
        self._card_back = create_card_frame(
            f"{element_idx[0]}{element_idx[1]}", self._frame_elements,
            self._frame_size)

    @property
    def element_name(self):
        return self._element_name

    def __str__(self):
        """
        Custom functionality for the default __str__ method for
        printing content.
        """
        if self.is_visible:
            return self.card_front
        else:
            return self.card_back

    def __copy__(self):
        return BoardElement(self._element_name, self._element_content,
                            self._frame_elements, self._frame_size)


class Board:
    """
    Class of board elements: frame and images.
    """

    def __init__(self, board_size: List[int], start_element: BoardElement):
        # initialize attributes
        self._board_size = board_size
        # create a list of start elements then repeat that a number of
        # times equal to the number of rows in the board
        self._board_content = [(board_size[1] * [
            start_element]).copy() for _ in range(board_size[0])]
        self._nb_used_board_cells = 0

    @property
    def board_size(self):
        return self._board_size

    @property
    def board_content(self):
        return self._board_content

    @property
    def nb_used_board_cells(self):
        return self._nb_used_board_cells

    def __str__(self):
        """
        Custom functionality for the string method of this class.
        It merges all the elements of the board into a single string.
        """

        board_str = ""
        # for each row add subsequent rows of default elements
        for row in range(0, self._board_size[0]):
            row_string = self._board_content[row][0].__str__()
            # for each column add subsequent default element
            for column in range(1, self._board_size[1]):
                row_string = merge_str_line_by_line(
                    row_string, self._board_content[row][column].__str__())
            board_str += row_string
        return board_str

    def insert_board_element(
            self, element: BoardElement, board_index: List[int]):
        self._board_content[board_index[0]][board_index[1]] = element
        self._board_content[board_index[0]][board_index[1]].card_back = \
            board_index

    def flip_board_element(self, board_index: List[int]):
        """
        The function flips a card.
        """
        self._board_content[board_index[0]][board_index[1]].is_visible = \
            not self._board_content[board_index[0]][board_index[1]].is_visible

    def populate_board(self, element_list: List[BoardElement]):
        """
        This function randomly populates the board with pairs of elements
        from a card element list.
        """

        # create list of possible indexes
        row_indexes = list(range(self._board_size[0]))
        column_indexes = list(range(self._board_size[1]))
        index_list = create_nested_list(row_indexes, column_indexes)

        # create copy of element list for the pairs
        for element in element_list:
            # draw a random index
            idx = randint(0, len(index_list) - 1)
            self.insert_board_element(element, index_list[idx])
            index_list.pop(idx)
            # draw again for the pair
            idx = randint(0, len(index_list) - 1)
            self.insert_board_element(element.__copy__(), index_list[idx])
            index_list.pop(idx)
            # update the number of cards on the board
            # with +2 since we have a pair.
            self._nb_used_board_cells += 2
            if self._nb_used_board_cells == self.board_size[0] * \
                    self.board_size[1]:
                break


def flip_all_elements(self):
    """
    This function flips all cards at the same time.
    """
    for row in range(0, self._board_size[0]):
        for column in range(0, self._board_size[1]):
            self._board_content[row][column].is_visible = \
                not self._board_content[row][column].is_visible


def count_flipped_cards(self):
    """
    This function counts the number of flipped cards.
    """
    number_flipped_cards = 0
    for row in range(0, self._board_size[0]):
        for column in range(0, self._board_size[1]):
            number_flipped_cards += int(
                self._board_content[row][column].is_visible)

    return number_flipped_cards


def check_board_element_match(self, idx1, idx2):
    """
    Check by card element name whether two elements selected by
    respective indexes are a match.
    """

    return self._board_content[idx1[0]][idx1[1]].element_name == \
        self._board_content[idx2[0]][idx2[1]].element_name
