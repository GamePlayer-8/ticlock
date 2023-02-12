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

    effect_sz = 50
    render_str += term.move_xy(5, 11) + term.bold('Trippy effect')
    render_str += term.move_xy(0, 12) + term.red(progress.loader(effect_sz))
    render_str += term.move_xy(effect_sz, 12) + term.purple(progress.loader(effect_sz))
    render_str += term.move_xy(effect_sz*2, 12) + term.blue(progress.loader(effect_sz))
    render_str += term.move_xy(effect_sz*3, 12) + term.cyan(progress.loader(effect_sz))
    render_str += term.move_xy(effect_sz*4, 12) + term.green(progress.loader(effect_sz))

    return render_str