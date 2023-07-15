import os
import platform
import json
from typing import List


def parse_layout(layout_json):
    """
    Reads json file and converts to dictionary.
    """

    # read json file
    with open(layout_json) as user_file:
        file_contents = user_file.read()
    # convert to dictionary
    parsed_json = json.loads(file_contents)

    return parsed_json


def create_vertical_padding(corner_element: str, padding_element: str,
                            frame_width: int):
    """
    Creates a vertical line with padding of cards frame.
    """

    # create the padding line
    padding_line = "".join((frame_width - 2) * [padding_element])
    # create full vertical padding
    vertical_padding = f"{corner_element}{padding_line}{corner_element}\n"

    return vertical_padding


def create_blank_line(side_element: str, frame_width: int):
    """
    Creates a blank line with side elements of cards frame.
    """

    # create blank line
    blank_line_no_padding = "".join((frame_width - 2) * [' '])
    # pad it with side elements
    blank_line = f"{side_element}{blank_line_no_padding}{side_element}\n"

    return blank_line


def create_empty_frame(frame_size: dict):
    """
    Create the bulk of the empty frame without any padding with adding
    a blank line to create an empty frame for the cards.
    """

    blank_line = "".join((frame_size['frame_width'] - 2) * [" "])
    empty_frame = "\n".join((frame_size['frame_height'] - 2) * [blank_line])

    return empty_frame


def create_card_frame(card_element: str, frame_elements: dict,
                      frame_size: dict):
    """
    This function creates a frame around a given card element
    """

    # create top and bottom card element frame elements
    top_cover = create_vertical_padding(frame_elements['corner_element'],
                                        frame_elements['top_element'],
                                        frame_size['frame_width'])
    bottom_cover = create_vertical_padding(frame_elements['corner_element'],
                                           frame_elements['bottom_element'],
                                           frame_size['frame_width'])

    # create blank line
    blank_line = create_blank_line(frame_elements['side_element'],
                                   frame_size['frame_width'])

    # separate the card element string into individual lines
    card_element_lines = card_element.split('\n')

    # get element dimensions
    height = len(card_element_lines)
    width = 0
    for element_line in card_element_lines:
        element_line_len = len(element_line)
        if element_line_len > width:
            width = element_line_len

    # for each line add wall elements corresponding to the frame width
    card_element_lines_framed = []
    for element_line in card_element_lines:
        element_line_len = len(element_line)
        frame_start_offset = int(
            (frame_size['frame_width'] - 2 - element_line_len) / 2)
        frame_end_offset = \
            frame_size['frame_width'] - 2 - element_line_len - \
            frame_start_offset
        card_element_line_framed = frame_elements['side_element'] + "".join(
            frame_start_offset * [' ']) + element_line + "".join(
            frame_end_offset * [' ']) + frame_elements['side_element'] + "\n"
        card_element_lines_framed.append(card_element_line_framed)

    # calculate top and bottom frame cover offsets
    frame_start_offset = int((frame_size['frame_height'] - 2 - height) / 2)
    frame_end_offset = frame_size['frame_height'] - 2 - height - \
        frame_start_offset

    # assemble the framed card element
    framed_card_element = top_cover + "".join(
        frame_start_offset * [blank_line]) + "".join(
            card_element_lines_framed) + "".join(frame_end_offset * [
                blank_line]) + bottom_cover

    return framed_card_element


def merge_str_line_by_line(string1: str, string2: str):
    # split each string into lines using the newline character as separator
    string1_lines = string1.split('\n')
    string2_lines = string2.split('\n')

    # merge the two strings line by line (https://shorturl.at/kwIJ4)
    merged_lines = []
    for x, y in zip(string1_lines, string2_lines):
        merged_lines.append(f"{x}{y}")
    final_string = "\n".join(merged_lines)

    return final_string


def create_nested_list(list1: List[int], list2: List[int]):
    """
    The Function allocate nested list and go through list elements
    in a nested loop to create the nested list.
    """
    nested_list = []
    for idx1 in range(len(list1)):
        for idx2 in range(len(list2)):
            # append the list elements as a joint list
            nested_list.append([list1[idx1], list2[idx2]])

    return nested_list


def check_value(val: str, prev_val: str, supp_vals: List[str],
                error_messages: dict):
    """
    Check whether the card ('val') is within a list of supported
    values ('supp_vals'), checks if card is the same as the first one or has
    an empty value.
    The function will either return 'True' or,
    in case of an incorrect value, raise a ValueError with the error
    message specified by err_msg.
    """

    if not val:
        raise ValueError(error_messages['empty_string'])

    # check whether same index, provided previous value has been given
    if val == prev_val:
        raise ValueError(error_messages['duplicate_index'])

    if val not in supp_vals:
        raise ValueError(error_messages['wrong_index'])

    return True


def check_input(supported_vals: List[str], prev_val: str, card_nr: int,
                messages: dict):
    """
    Checks card, what a player has been selected.
    Displays an error message.
    """

    while True:
        try:
            input_value = input(messages['input_message'][card_nr])
            # strip trailing spaces from the user input
            input_value = input_value.strip(' ')

            check_value(input_value, prev_val, supported_vals,
                        messages['error_messages'])
            return input_value
        except ValueError as e:
            print(e)


def check_is_int(user_name: str, error_messages: dict):
    """
    The function checks if the user did not enter a name or
    if the user only input numbers for their username.
    """

    if not user_name:
        raise ValueError(error_messages['no_name'])

    user_name_int = 0
    try:
        int(user_name)
        user_name_int = int(user_name)
    except ValueError:
        pass
    if user_name_int:
        raise ValueError(error_messages['wrong_name'])

    return True


def check_user_name(error_messages: dict):
    """
    The function check if the user did not enter a name then
    runs check_is_int function.
    """

    while True:
        try:
            user_name = input("Please enter your name:\n")
            check_is_int(user_name, error_messages)
            break
        except ValueError as e:
            print(e)

    return user_name


def check_end_game_choice(choice: str, error_messages: dict):
    """
    Checks whether empty string or list is in the supported values, then
    displays an error message.
    """

    if not choice:
        raise ValueError(error_messages['empty_string'])

    choice = choice.capitalize()
    if choice not in ['Y', 'N']:
        raise ValueError(error_messages['wrong_choice'])

    return True


def clear_terminal():
    """
    Function for platform dependent clearing of terminal.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')