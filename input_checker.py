from typing import List


def check_value(val: str, supp_vals: List[str], err_msg: str):
    """
    Check whether the value ('val') is within a list of supported values ('supp_vals').
    The function will either return 'True' or, in case of an incorrect value, raise a ValueError with the error
    message specified by err_msg.

    :param val:
    :param supp_vals:
    :param err_msg:
    :return:
    """

    if val in supp_vals:
        return True
    else:
        raise ValueError(err_msg)


def check_input(supported_vals: List[str], inp_msg, err_msg):
    """

    :param supported_vals:
    :param inp_msg:
    :param err_msg:
    :return:
    """
    while True:
        try:
            input_value = input(inp_msg)
            check_value(input_value, supported_vals, err_msg)
            return input_value
        except ValueError as e:
            print(e)
