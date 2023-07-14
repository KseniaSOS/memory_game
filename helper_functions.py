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


def create_vertical_padding(corner_element: str, padding_element: str, frame_width: int):
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


def create_card_frame(card_element: str, frame_elements: dict, frame_size: dict):
    """
    This function creates a frame around a given card element
    """

    # create top and bottom card element frame elements
    top_cover = create_vertical_padding(frame_elements['corner_element'], frame_elements['top_element'],
                                        frame_size['frame_width'])
    bottom_cover = create_vertical_padding(frame_elements['corner_element'], frame_elements['bottom_element'],
                                           frame_size['frame_width'])

    # create blank line
    blank_line = create_blank_line(frame_elements['side_element'], frame_size['frame_width'])

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
        frame_start_offset = int((frame_size['frame_width'] - 2 - element_line_len) / 2)
        frame_end_offset = frame_size['frame_width'] - 2 - element_line_len - frame_start_offset
        card_element_line_framed = frame_elements['side_element'] + "".join(frame_start_offset * [' ']) + \
            element_line + "".join(frame_end_offset * [' ']) + frame_elements['side_element'] + "\n"
        card_element_lines_framed.append(card_element_line_framed)

    # calculate top and bottom frame cover offsets
    frame_start_offset = int((frame_size['frame_height'] - 2 - height) / 2)
    frame_end_offset = frame_size['frame_height'] - 2 - height - frame_start_offset

    # assemble the framed card element
    framed_card_element = top_cover + "".join(frame_start_offset * [blank_line]) + \
        "".join(card_element_lines_framed) + "".join(frame_end_offset * [blank_line]) + bottom_cover

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


def check_value(val: str, supp_vals: List[str], err_msg: str):
    """
    Check whether the value ('val') is within a list of supported
    values ('supp_vals'). The function will either return 'True' or,
    in case of an incorrect value, raise a ValueError with the error
    message specified by err_msg.
    """

    if val in supp_vals:
        return True
    else:
        raise ValueError(err_msg)


def check_input(supported_vals: List[str], inp_msg, err_msg):
    """
    Check input, what a player has been selected.
    Displays an error massage.
    """
    while True:
        try:
            input_value = input(inp_msg)
            check_value(input_value, supported_vals, err_msg)
            return input_value
        except ValueError as e:
            print(e)
