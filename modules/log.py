"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

import os
from datetime import datetime
from blessed import Terminal

if not os.path.isdir('log'):
    os.mkdir('log')

term = Terminal()


class Logger:
    """
        AI:define_function # Needs work
    """

    def __init__(self, name):
        """
            AI:define_function # Needs work
        """
        self.name = name
        self.session_file_path = f'log/{name}.txt'
        with open(self.session_file_path, 'a', encoding='utf-8') as session_file:
            self.current_session_time = datetime.now().strftime('%D/%m/%Y %H:%M:%S')
            session_file.write('--- ' + self.current_session_time + '\n')

    def create_log_entry(self, self_type, message):
        """
            AI:define_function # Needs work
        """
        emojis = {
            'log': '📄',
            'warn': '⚠',
            'info': 'ℹ',
            'error': '❌'
        }

        if not self_type in emojis:
            raise Exception(
                f'''logging type {type} doesn\'t exist 
                (expected one of {", ".join(list(emojis.keys()))})'''
            )

        with open(self.session_file_path, 'a', encoding='utf-8') as session_file:
            session_file.write(
                datetime.now().strftime('%D/%m/%Y %H:%M:%S') + \
                f' [{emojis[self_type]}] {message}\n'
            )

    def log(self, message):
        """Alias to self.create_log_entry('log', message)."""
        self.create_log_entry('log', message)

    def warn(self, message):
        """Alias to self.create_log_entry('warn', message)."""
        self.create_log_entry('warn', message)

    def info(self, message):
        """Alias to self.create_log_entry('info', message)."""
        self.create_log_entry('info', message)

    def error(self, message):
        """Alias to self.create_log_entry('error', message)."""
        self.create_log_entry('error', message)

    def brief(self):
        """
            AI:define_function # Needs work
        """
        with open(self.session_file_path, 'r', encoding='utf-8') as session_file:
            lines = session_file.readlines()
            regular_log_counts = 0
            titles = 0
            entries = 0
            other_logs = ''
            reading = False
            for line in lines:
                if line.startswith('--- '):
                    if reading:
                        titles += 1
                    if line == f'--- {self.current_session_time}':
                        reading = True
                    continue
                if reading:
                    entries += 1
                    if line.split(' ')[2] == '[📄]':
                        regular_log_counts += 1
                    else:
                        other_logs += line

        return term.bold(
            str(entries - titles)) + \
            ' entries, of which ' + \
            term.bold(str(regular_log_counts)) + \
            ' regular entries.' + \
            (f' found important entries:\n{other_logs}' if len(other_logs) > 0 else ''
             )
