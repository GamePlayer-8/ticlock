"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

import os
import sys
import time
import importlib
from math import floor
import pynput.keyboard as kb
from blessed import Terminal
import config
import modules.progress_bar as progress
from modules.log import Logger

os.chdir(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
PYBIN = sys.executable

TERM = Terminal()
MAIN_LOG_STREAM = Logger('ticlock-main')

apps = {}
CURRENT_APP = 'clock'
APP_FRAME_NUMBER = 0

MENU_KEYPRESSES = 0
LAST_MENU_KEYPRESS = time.time()

KEY_INPUTS = {}
def key_press(key_pressed):
    """
        AI:define_function # Needs work
    """
    try:
        KEY_INPUTS[key_pressed.char] = 0
    except AttributeError:
        KEY_INPUTS[key_pressed] = 0

def key_release(key_pressed):
    """
        AI:define_function # Needs work
    """
    try:
        del KEY_INPUTS[key_pressed.char]
    except AttributeError:
        del KEY_INPUTS[key_pressed]

if not os.path.exists('apps/clock.py'):
    print(TERM.bold_red('! Well that\'s awkward...'))
    print(
        '''We couldn\'t find the clock app.
        Try making a file called "clock.py" in the apps folder.'''
    )

def find_app_number():
    """
        AI:define_function # Needs work
    """
    num = 0
    for file in os.listdir('apps'):
        if file.startswith('_') or not file.endswith('.py'):
            continue
        num += 1
    return num


def reload_apps():
    """
        AI:define_function # Needs work
    """
    apps_num = find_app_number()
    for file in os.listdir('apps'):
        if file.startswith('_') or not file.endswith('.py'):
            continue

        mod_name = file.rstrip('.py')
        spec = importlib.util.spec_from_file_location(mod_name, 'apps/' + file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        apps[mod_name] = module

        MAIN_LOG_STREAM.log(f'Loaded application {mod_name}.')

        with TERM.location(floor(TERM.width/2 - 10), 1):
            print(TERM.green(progress.definite(20, len(apps.keys())/apps_num)), end='')

    return list(apps.keys())

APPS_LIST = reload_apps()
CURRENT_APP_ID = APPS_LIST.index(CURRENT_APP)

reload_apps()

def construct_applications_list(apps_list_arg, app_id):
    """
        AI:define_function # Needs work
    """
    app_str = ''
    for i in range(app_id, len(apps_list_arg)):
        app = apps_list_arg[i]
        if TERM.length(app_str + app) > TERM.width:
            break
        ending_character = ' ' if i <= len(apps_list_arg) - 1 else ''
        if app_id == i:
            app_str += TERM.on_orange(app) + ending_character
        else:
            app_str += app + ending_character
    return app_str

listener = kb.Listener(
    on_press=key_press,
    on_release=key_release)
listener.start()

try:
    with TERM.fullscreen(), TERM.hidden_cursor(), TERM.cbreak():
        last_op = time.time()
        while True:
            delta = time.time() - last_op
            last_op = time.time()

            for key in KEY_INPUTS:
                KEY_INPUTS[key] += 1

            if '*' in KEY_INPUTS:
                if KEY_INPUTS['*'] == 1:
                    if time.time() - LAST_MENU_KEYPRESS < 0.5:
                        MENU_KEYPRESSES += 1
                    else:
                        MENU_KEYPRESSES = 1
                    LAST_MENU_KEYPRESS = time.time()
                    if MENU_KEYPRESSES > 2:
                        MENU_KEYPRESSES = 0

            RENDER_STRING = ''

            if hasattr(apps[CURRENT_APP], 'update'):
                if MENU_KEYPRESSES < 2:
                    RENDER_STRING += \
                        apps[CURRENT_APP].update(
                            delta,
                            APP_FRAME_NUMBER,
                            KEY_INPUTS
                        )
                else:
                    RENDER_STRING += \
                    apps[CURRENT_APP].update(
                        delta,
                        APP_FRAME_NUMBER,
                        {}
                    )
            else:
                string = TERM.bold_red(
                    f'This application ({CURRENT_APP}) has no update sequence.'
                )
                string2 = \
                    f'''If you\'re the developper of this app,
                    open its Python file (apps/{CURRENT_APP}.py) and
                    add an update function.'''
                RENDER_STRING += TERM.move_xy(
                    floor(
                        TERM.width/2 - TERM.length(string)/2),
                        floor(TERM.height/2)
                ) + string
                RENDER_STRING += TERM.move_xy(
                    floor(TERM.width/2 - TERM.length(string2)/2),
                    floor(TERM.height/2) + 1
                ) + string2

                RENDER_STRING += TERM.move_xy(
                    floor(TERM.width/2 - 0.125*TERM.width),
                    floor(TERM.height/2) + 3) + TERM.blue(
                        progress.loader(floor(0.25*TERM.width)
                    )
                )

            menu_y = TERM.height - 4

            if MENU_KEYPRESSES == 2:
                RENDER_STRING += TERM.move_xy(0, menu_y) + \
                    TERM.on_blue(
                        TERM.clear_eol + TERM.on_cyan('ticlock') + \
                        f''' menu ・ (←/→) change application -
                        (Enter) open application -
                        (r) reload all applications ・ {(1/max(delta, 1e-10)):.2f}FPS'''
                    )
                RENDER_STRING += TERM.move_xy(0, menu_y + 1) + \
                    TERM.on_gray(
                        TERM.clear_eol + \
                        construct_applications_list(
                            APPS_LIST,
                            CURRENT_APP_ID
                        )
                    )

                if kb.Key.left in KEY_INPUTS:
                    if (KEY_INPUTS[kb.Key.left]-1) % 30 == 0:
                        CURRENT_APP_ID = max(CURRENT_APP_ID - 1, 0)

                if kb.Key.right in KEY_INPUTS:
                    if (KEY_INPUTS[kb.Key.right]-1) % 30 == 0:
                        CURRENT_APP_ID = min(
                            CURRENT_APP_ID + 1,
                            len(APPS_LIST) - 1
                        )

                if kb.Key.enter in KEY_INPUTS:
                    if KEY_INPUTS[kb.Key.enter] == 1:
                        CURRENT_APP = APPS_LIST[CURRENT_APP_ID]
                        APP_FRAME_NUMBER = -1
                        MENU_KEYPRESSES = 0

                if 'r' in KEY_INPUTS:
                    if KEY_INPUTS['r'] == 1:
                        reload_apps()

            APP_FRAME_NUMBER += 1
            print(RENDER_STRING)
            
            if config.WAIT_BEFORE_REFRESH:
                time.sleep(delta/config.REFRESH_DELAY) # WAIT BETWEEN SCREEN REFRESHES
            
            print(TERM.home+TERM.clear, end='')
           

except KeyboardInterrupt:
    print(TERM.green('ticlock closed.'))
    print('here\'s what went on in the main log stream:')
    print(MAIN_LOG_STREAM.brief())
    sys.exit()
except Exception as e: # pylint: disable=broad-except
    MAIN_LOG_STREAM.error(f'Error in application {CURRENT_APP}: {e}')
    print(MAIN_LOG_STREAM.brief())
    CURRENT_APP = 'clock'
    CURRENT_APP_ID = APPS_LIST.index(CURRENT_APP)
