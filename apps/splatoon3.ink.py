from blessed import Terminal
from math import floor
import requests, time, datetime
import modules.progress_bar as progress
term = Terminal()

def reload_maps():
    headers = {
        'User-Agent': 'splatoon3.ink for ticlock',
        'From': 'github.com/rexxt/ticlock'
    }
    req = requests.get('https://splatoon3.ink/data/schedules.json', headers=headers)
    return req.json()['data']

last_update = 0
maps = {}
def update(dt, keys):
    global maps, last_update

    render_str = ''

    panel_number = 4
    panel_x = [floor(i/panel_number*term.width) for i in range(panel_number)]

    if time.time() - last_update >= 3600:
        maps = reload_maps()
    last_update = time.time()

    string = 'Splatoon 3 rotations - provided by splatoon3.ink'
    render_str += term.move_xy(floor(term.width/2-len(string)/2), 1) + string

    if 'currentFest' in maps:
        # we're in a splatfest
        render_str += term.move_xy(panel_x[0], 3) + term.on_purple('Current splatfest')
        render_str += term.move_xy(panel_x[0], 4) + term.bold(maps['currentFest']['title'])

        start_time = datetime.datetime.strptime(maps['currentFest']['startTime'], '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.datetime.strptime(maps['currentFest']['endTime'], '%Y-%m-%dT%H:%M:%SZ')
        midterm_time = datetime.datetime.strptime(maps['currentFest']['midtermTime'], '%Y-%m-%dT%H:%M:%SZ')

        render_str += term.move_xy(panel_x[0], 5) + start_time.strftime('%d/%m/%Y %H:%M') + ' UTC - ' + end_time.strftime('%d/%m/%Y %H:%M') + ' UTC'

        render_str += term.move_xy(panel_x[1], 3) + term.on_green('Turf War')
        for i in range(len(maps['festSchedules']['nodes'])):
            fest_map = maps['festSchedules']['nodes'][i]
            render_str += term.move_xy(panel_x[1], 4 + i) + term.bold(term.green('Now') if i == 0 else term.orange('Next') if i <= 1 else f'+{i}') + f' {fest_map["festMatchSetting"]["vsStages"][0]["name"]}/{fest_map["festMatchSetting"]["vsStages"][1]["name"]}'
        
        render_str += term.move_xy(panel_x[2], 3) + term.on_blue('Tri') + term.on_yellow('col') + term.on_gray('our') + term.on_purple(' Turf War')
        if time.time() <= midterm_time.timestamp():
            render_str += term.move_xy(panel_x[2], 4) + term.red('Starts on ' + midterm_time.strftime('%d/%m/%Y %H:%M') + ' UTC.')
        else:
            render_str += term.move_xy(panel_x[2], 4) + term.green('Live now!')
        render_str += term.move_xy(panel_x[2], 5) + maps['currentFest']['tricolorStage']['name']

        render_str += term.move_xy(panel_x[3], 3) + term.on_orange('Salmon Run')
        for i in range(len(maps['coopGroupingSchedule']['regularSchedules']['nodes'])):
            salmon_run = maps['coopGroupingSchedule']['regularSchedules']['nodes'][i]
            render_str += term.move_xy(panel_x[3], 4 + i*2) + term.bold(term.green('Now') if i == 0 else term.orange('Next') if i <= 1 else f'+{i}') + f' {salmon_run["setting"]["coopStage"]["name"]}'
            render_str += term.move_xy(panel_x[3], 5 + i*2) + '/'.join([weapon['name'] for weapon in salmon_run['setting']['weapons']])[:term.width-panel_x[3]]

    return render_str