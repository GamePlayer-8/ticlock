"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

import time
import datetime
from math import floor
import requests
from blessed import Terminal
from modules.log import Logger

LOG = Logger('splatoon3.ink')
TERM = Terminal()

def reload_maps():
    """
        AI:define_function # Needs work
    """
    headers = {
        'User-Agent': 'splatoon3.ink for ticlock',
        'From': 'github.com/rexxt/ticlock'
    }
    req = requests.get('get',
        'https://splatoon3.ink/data/schedules.json',
        headers=headers,
        timeout=20
    )
    return req.json()['data']

def update(_dt, _frame, _keys): # Please Make use of those variables or I'll delete them
    """
        AI:define_function # Needs work
    """
    maps = {}
    last_update = 0

    render_str = ''

    panel_number = 4
    panel_x = [floor(i/panel_number*TERM.width) for i in range(panel_number)]
    last_update_hour = datetime.datetime.now().hour

    if time.time() - last_update >= 3600 or datetime.datetime.now().hour != last_update_hour:
        maps = reload_maps()
        last_update = time.time()
        last_update_hour = datetime.datetime.now().hour

    string = 'Splatoon 3 rotations - provided by splatoon3.ink'
    render_str += TERM.move_xy(floor(TERM.width/2-len(string)/2), 1) + string

    if 'currentFest' in maps:
        # we're in a splatfest
        render_str += \
            TERM.move_xy(panel_x[0], 3) + \
            TERM.on_purple('Current splatfest')
        render_str += \
            TERM.move_xy(panel_x[0], 4) + \
            TERM.bold(maps['currentFest']['title'])

        start_time = \
            datetime.datetime.strptime(
                maps['currentFest']['startTime'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
        end_time = \
            datetime.datetime.strptime(
                maps['currentFest']['endTime'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
        midterm_time = \
            datetime.datetime.strptime(
                maps['currentFest']['midtermTime'],
                '%Y-%m-%dT%H:%M:%SZ'
            )

        render_str += \
            TERM.move_xy(panel_x[0], 5) + \
            start_time.strftime('%d/%m/%Y %H:%M') + \
            ' UTC - ' + \
            end_time.strftime('%d/%m/%Y %H:%M') + ' UTC'

        render_str += \
            TERM.move_xy(panel_x[1], 3) + \
            TERM.on_green('Turf War')
        for i in range(len(maps['festSchedules']['nodes'])):
            fest_map = maps['festSchedules']['nodes'][i]
            if i == 1:
                next_rotation_time = \
                    datetime.datetime.strptime(
                        fest_map['startTime'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).timestamp()
                delta_time = datetime.timedelta(
                    seconds=next_rotation_time - time.time()
                )
            if fest_map['festMatchSetting']:
                render_str += \
                    TERM.move_xy(panel_x[1], 4 + i) + \
                    TERM.bold(TERM.green('Now') if i == 0 else TERM.orange(
                        'Next') if i <= 1 else f'+{i}') + \
                        f' {fest_map["festMatchSetting"]["vsStages"][0]["name"]}/\
                        {fest_map["festMatchSetting"]["vsStages"][1]["name"]}'
        render_str += \
            TERM.move_xy(
                panel_x[1], 3 + len(maps['festSchedules']['nodes'])) + \
            'Next rotation in ' + TERM.bold(str(delta_time)
                                            )

        render_str += TERM.move_xy(panel_x[2], 3) + TERM.on_blue('Tri') + TERM.on_yellow(
            'col') + TERM.on_gray('our') + TERM.on_purple(' Turf War')
        if time.time() <= midterm_time.timestamp():
            render_str += TERM.move_xy(panel_x[2], 4) + TERM.red(
                'Starts on ' + midterm_time.strftime('%d/%m/%Y %H:%M') + ' UTC.')
        else:
            render_str += TERM.move_xy(panel_x[2], 4) + TERM.green('Live now!')
        render_str += TERM.move_xy(panel_x[2], 5) + \
            maps['currentFest']['tricolorStage']['name']

        render_str += TERM.move_xy(panel_x[3], 3) + \
            TERM.on_orange('Salmon Run')
        for i in range(len(maps['coopGroupingSchedule']['regularSchedules']['nodes'])):
            salmon_run = maps['coopGroupingSchedule']['regularSchedules']['nodes'][i]
            if i == 1:
                next_rotation_time = datetime.datetime.strptime(
                    salmon_run['startTime'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
                delta_time = datetime.timedelta(
                    seconds=next_rotation_time - time.time())
            if salmon_run['setting']:
                render_str += TERM.move_xy(
                    panel_x[3],
                    4 + i*2
                ) + TERM.bold(TERM.green('Now') if i == 0 else TERM.orange(
                    'Next') if i <= 1 else f'+{i}') + f' \
                    {salmon_run["setting"]["coopStage"]["name"]}'
                render_str += TERM.move_xy(panel_x[3], 5 + i*2) + '/'.join(
                    [weapon['name'] \
                    for weapon in salmon_run['setting']['weapons']])[:TERM.width-panel_x[3]]
        render_str += TERM.move_xy(panel_x[3], 3 + len(maps['coopGroupingSchedule']
                                   ['regularSchedules']['nodes'])*2) + \
                                   'Next rotation in ' + TERM.bold(str(delta_time)
                                )

    return render_str
