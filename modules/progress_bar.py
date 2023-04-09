"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

from math import floor
from time import time

def definite(length, fill):
    """
        AI:define_function # Needs work
    """

    shadow = '░'
    full = '█'

    fill_len = floor(length * fill)
    shadow_len = length - fill_len

    return full * fill_len + shadow * shadow_len

def loader(length):
    """
        AI:define_function # Needs work
    """
    shadow = '░'
    degrees = '▒▓█'

    interval = 2

    string = [shadow for i in range(length)]

    point = (time()%interval)/interval*length
    for i, rate in enumerate(degrees):
        displacement = floor(point - len(degrees) + 1 + i)
        string[displacement] = rate

    return ''.join(string)
