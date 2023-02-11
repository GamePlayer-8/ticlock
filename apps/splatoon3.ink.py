from blessed import Terminal
from math import floor
import requests, time
import apps._progress_bar as progress
term = Terminal()

def reload_maps():
    headers = {
        'User-Agent': 'splatoon3.ink for ticlock',
        'From': 'github.com/rexxt'
    }
    req = requests.get('https://splatoon3.ink/data/schedules.json', headers=headers)
    return req.json()

last_update = 0
maps = {}
def update(dt, keys):
    global maps, last_update

    render_str = ''

    if time.time() - last_update >= 3600:
        maps = reload_maps()
    last_update = time.time()

    string = 'Splatoon 3 rotations - provided by splatoon3.ink'
    render_str += term.move_xy(floor(term.width/2-len(string)/2), 1) + string

    return render_str