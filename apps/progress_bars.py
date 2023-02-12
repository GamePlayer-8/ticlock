from blessed import Terminal
from math import floor
from time import time
import modules.progress_bar as progress
term = Terminal()

def update(dt, frame, keys):
    render_str = ''

    render_str += term.move_xy(5, 4) + term.bold('Definite progress bars')
    render_str += term.move_xy(0, 5) + term.red(progress.definite(20, time()%1))
    render_str += term.move_xy(0, 6) + term.orange(progress.definite(term.width, time()%1))

    render_str += term.move_xy(5, 8) + term.bold('Loaders')
    render_str += term.move_xy(0, 9) + term.blue(progress.loader(20))
    render_str += term.move_xy(21, 9) + term.cyan(progress.loader(50))

    return render_str