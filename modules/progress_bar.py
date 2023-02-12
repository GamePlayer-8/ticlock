from math import floor
from time import time

def definite(len, fill):
    shadow = '░'
    full = '█'

    fill_len = floor(len * fill)
    shadow_len = len - fill_len

    return full * fill_len + shadow * shadow_len

def loader(length):
    shadow = '░'
    degrees = '▒▓█'

    interval = 2

    string = [shadow for i in range(length)]

    point = (time()%interval)/interval*length
    for i in range(len(degrees)):
        displacement = floor(point - len(degrees) + 1 + i)
        string[displacement] = degrees[i]

    return ''.join(string)