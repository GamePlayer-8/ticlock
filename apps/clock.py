import datetime, time
from blessed import Terminal
import apps._7sd as _7sd
import apps._progress_bar as progress

term = Terminal()

display = _7sd.SevenSegmentDisplay()

displays_x = []

def convert_state(string):
    li = []
    for char in string:
        if char in (' ', '\t', '\r', '\n'):
            continue
        li.append(char == '#')
    return li

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

def update(dt, keys):
    global displays_x
    string = ''

    now = datetime.datetime.now()
    sec_time = time.time()
    hr = '0' + str(now.hour) if now.hour < 10 else str(now.hour)
    mn = '0' + str(now.minute) if now.minute < 10 else str(now.minute)
    sec = '0' + str(now.second) if now.second < 10 else str(now.second)

    digits = hr + mn + sec
    size = 3
    x = int((term.width-78)//2)
    y = 5

    off_x = 0
    for i in range(len(digits)):
        digit = digits[i]
        num_digit = int(digit)

        display.state = states[num_digit]
        string += display.render(x + i * size * 4 + off_x * 4, y, size=size)
        if i%2 == 1:
            off_x += 1
        else:
            displays_x.append(x + i * size * 4 + off_x * 4)

    blink_interval = 1
    blink_length = 0.5

    if sec_time % blink_interval < blink_length:
        for i in range(2):
            string += term.move_xy(x + ((size + 2)*4 + 4)*(i+1) + (4 if i == 1 else 0), y + 2) + term.on_white('  ')
            string += term.move_xy(x + ((size + 2)*4 + 4)*(i+1) + (4 if i == 1 else 0), y + 6) + term.on_white('  ')

    string += term.move_xy(displays_x[0], y - 2) + term.red(progress.definite(2*(4 + size * 2) + 2, now.hour/24))
    string += term.move_xy(displays_x[1], y - 2) + term.orange(progress.definite(2*(4 + size * 2) + 2, now.minute/60))
    string += term.move_xy(displays_x[2], y - 2) + term.cyan(progress.definite(2*(4 + size * 2) + 2, now.second/60))
    string += term.move_xy(displays_x[2], y - 3) + term.blue(progress.definite(2*(4 + size * 2) + 2, sec_time%1))
    
    string += term.move_xy(x, y + 10) + f'{now.day}/{now.month}/{now.year}'

    return string