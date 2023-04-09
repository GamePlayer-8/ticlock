"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

import time
import datetime
from blessed import Terminal
from modules import _7sd
from modules import progress_bar as progress

term = Terminal()

display = _7sd.SevenSegmentDisplay()

def convert_state(string):
    """
        AI:define_function # Needs work
    """
    line = []
    for char in string:
        if char in (' ', '\t', '\r', '\n'):
            continue
        line.append(char == '#')
    return line

states = [
    convert_state("""
 #
# #
 .
# #
 #
"""),
convert_state("""
 .
. #
 .
. #
 .
"""),
convert_state("""
 #
. #
 #
# .
 #
"""),
convert_state("""
 #
. #
 #
. #
 #
"""),
convert_state("""
 .
# #
 #
. #
 .
"""),
convert_state("""
 #
# .
 #
. #
 #
"""),
convert_state("""
 #
# .
 #
# #
 #
"""),
convert_state("""
 #
. #
 .
. #
 .
"""),
convert_state("""
 #
# #
 #
# #
 #
"""),
convert_state("""
 #
# #
 #
. #
 #
"""),
]

def calc_time(now):
    """
        AI:define_function # Needs work
    """
    hour = '0' + str(now.hour) if now.hour < 10 else str(now.hour)
    minute = '0' + str(now.minute) if now.minute < 10 else str(now.minute)
    second = '0' + str(now.second) if now.second < 10 else str(now.second)
    return [hour, minute, second]

def update(_dt, _frame, _keys): # PLEASE SPECIFY THE USAGE OF IT
    """
        AI:define_function # Needs work
    """
    displays_x = []
    render_str = ''

    now = datetime.datetime.now()
    sec_time = time.time()

    digits = calc_time(now)
    digits = digits[0] + digits[1] + digits[2]
    size = 3
    x_position = int((term.width-78)//2)
    y_position = 5

    off_x = 0
    for i, digit in enumerate(digits):
        num_digit = int(digit)

        display.state = states[num_digit]
        render_str += display.render(x_position + i * size *
                                     4 + off_x * 4, y_position, size=size)
        if i % 2 == 1:
            off_x += 1
        else:
            displays_x.append(x_position + i * size * 4 + off_x * 4)

    blink_interval = 1
    blink_length = 0.5

    if sec_time % blink_interval < blink_length:
        for i in range(2):
            render_str += term.move_xy(
                x_position + ((size + 2)*4 + 4)*(i+1) + (4 if i == 1 else 0),
                y_position + 2
            ) + term.on_white('  ')
            render_str += term.move_xy(
                x_position + ((size + 2)*4 + 4)*(i+1) + (4 if i == 1 else 0),
                y_position + 6
            ) + term.on_white('  ')

    render_str += term.move_xy(
        displays_x[0],
        y_position - 2
    ) + term.red(
        progress.definite(
            2*(4 + size * 2) + 2,
            now.hour/24
        )
    )
    render_str += term.move_xy(
        displays_x[1],
        y_position - 2
    ) + term.orange(
        progress.definite(
            2*(4 + size * 2) + 2,
            now.minute/60
        )
    )
    render_str += term.move_xy(
        displays_x[2],
        y_position - 2
    ) + term.cyan(
        progress.definite(
            2*(4 + size * 2) + 2,
            now.second/60
        )
    )
    render_str += term.move_xy(
        displays_x[2],
        y_position - 3
    ) + term.blue(
        progress.definite(
            2*(4 + size * 2) + 2,
            sec_time % 1
        )
    )

    render_str += term.move_xy(
        x_position,
        y_position + 10
    ) + f'{now.day}/{now.month}/{now.year}'

    return render_str
