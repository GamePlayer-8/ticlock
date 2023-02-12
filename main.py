from blessed import Terminal
from sys import exit
from math import floor
import modules.progress_bar as progress
import os, importlib, time, pynput.keyboard as kb
from modules.log import Logger

term = Terminal()
main_log_stream = Logger('ticlock-main')

apps = {}
current_app = 'clock'
app_frame_number = 0

menu_keypresses = 0
last_menu_keypress = time.time()

key_inputs = {}
def key_press(key):
    try:
        key_inputs[key.char] = 0
    except AttributeError:
        key_inputs[key] = 0

def key_release(key):
    try:
        del key_inputs[key.char]
    except AttributeError:
        del key_inputs[key]

if not os.path.exists('apps/clock.py'):
    print(term.bold_red('! Well that\'s awkward...'))
    print('We couldn\'t find the clock app. Try making a file called "clock.py" in the apps folder.')

def find_app_number():
    num = 0
    for file in os.listdir('apps'):
        if file.startswith('_') or not file.endswith('.py'):
            continue
        num += 1
    return num

def reload_apps():
    global apps_list, current_app_id
    apps_num = find_app_number()
    for file in os.listdir('apps'):
        if file.startswith('_') or not file.endswith('.py'):
            continue

        mod_name = file.rstrip('.py')
        spec = importlib.util.spec_from_file_location(mod_name, 'apps/' + file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        apps[mod_name] = module

        main_log_stream.log(f'Loaded application {mod_name}.')

        with term.location(floor(term.width/2 - 10), 1):
            print(term.green(progress.definite(20, len(apps.keys())/apps_num)), end='')

    apps_list = list(apps.keys())
    current_app_id = apps_list.index(current_app)

reload_apps()

def construct_applications_list(apps_list, id):
    app_str = ''
    for i in range(id, len(apps_list)):
        app = apps_list[i]
        if term.length(app_str + app) > term.width:
            break
        ending_character = ' ' if i <= len(apps_list) - 1 else ''
        if id == i:
            app_str += term.on_orange(app) + ending_character
        else:
            app_str += app + ending_character
    return app_str

listener = kb.Listener(
    on_press=key_press,
    on_release=key_release)
listener.start()

try:
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        last_op = time.time()
        while True:
            delta = time.time() - last_op
            last_op = time.time()

            for key in key_inputs:
                key_inputs[key] += 1

            if '*' in key_inputs:
                if key_inputs['*'] == 1:
                    if time.time() - last_menu_keypress < 0.5:
                        menu_keypresses += 1
                    else:
                        menu_keypresses = 1
                    last_menu_keypress = time.time()
                    if menu_keypresses > 2:
                        menu_keypresses = 0

            render_str = ''

            if hasattr(apps[current_app], 'update'):
                if menu_keypresses < 2:
                    render_str += apps[current_app].update(delta, app_frame_number, key_inputs)
                else:
                    render_str += apps[current_app].update(delta, app_frame_number, {})
            else:
                string = term.bold_red(f'This application ({current_app}) has no update sequence.')
                string2 = f'If you\'re the developper of this app, open its Python file (apps/{current_app}.py) and add an update function.'
                render_str += term.move_xy(floor(term.width/2 - term.length(string)/2), floor(term.height/2)) + string
                render_str += term.move_xy(floor(term.width/2 - term.length(string2)/2), floor(term.height/2) + 1) + string2

                render_str += term.move_xy(floor(term.width/2 - 0.125*term.width), floor(term.height/2) + 3) + term.blue(progress.loader(floor(0.25*term.width)))
            
            menu_y = term.height - 4

            if menu_keypresses == 2:
                render_str += term.move_xy(0, menu_y) + term.on_blue(term.clear_eol + term.on_cyan('ticlock') + f' menu ・ (←/→) change application - (Enter) open application - (r) reload all applications ・ {(1/max(delta, 1e-10)):.2f}FPS')
                render_str += term.move_xy(0, menu_y + 1) + term.on_gray(term.clear_eol + construct_applications_list(apps_list, current_app_id))

                if kb.Key.left in key_inputs:
                    if (key_inputs[kb.Key.left]-1) % 30 == 0:
                        current_app_id = max(current_app_id - 1, 0)
                
                if kb.Key.right in key_inputs:
                    if (key_inputs[kb.Key.right]-1) % 30 == 0:
                        current_app_id = min(current_app_id + 1, len(apps_list) - 1)
                
                if kb.Key.enter in key_inputs:
                    if key_inputs[kb.Key.enter] == 1:
                        current_app = apps_list[current_app_id]
                        app_frame_number = -1
                        menu_keypresses = 0
                
                if 'r' in key_inputs:
                    if key_inputs['r'] == 1:
                        reload_apps()

            app_frame_number += 1

            print(term.home+term.clear+render_str, end='')
except KeyboardInterrupt:
    print(term.green('ticlock closed.'))
    print('here\'s what went on in the main log stream:')
    print(main_log_stream.brief())
    exit()
except Exception as e:
    main_log_stream.error(f'Error in application {current_app}: {e}')
    current_app = 'readlogs'
    print(main_log_stream.brief())
    current_app_id = apps_list.index(current_app)