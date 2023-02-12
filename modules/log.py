from datetime import datetime
from blessed import Terminal
import os

if not os.path.isdir('log'):
    os.mkdir('log')

term = Terminal()

class Logger:
    def __init__(self, name):
        self.name = name
        self.session_file_path = f'log/{name}.txt'
        if os.path.exists(self.session_file_path):
            session_file = open(self.session_file_path, 'a+', encoding='utf-8')
        else:
            session_file = open(self.session_file_path, 'w+', encoding='utf-8')
        session_file.write('--- ' + datetime.now().strftime('%D/%m/%Y %H:%M:%S') + '\n')
        session_file.close()

    def create_log_entry(self, type, message):
        emojis = {
            'log': '📄',
            'warn': '⚠',
            'info': 'ℹ',
            'error': '❌'
        }

        if not type in emojis:
            raise Exception(f'logging type {type} doesn\'t exist (expected one of {", ".join(list(emojis.keys()))})')
        
        if os.path.exists(self.session_file_path):
            session_file = open(self.session_file_path, 'a+', encoding='utf-8')
        else:
            session_file = open(self.session_file_path, 'w+', encoding='utf-8')

        session_file.write(datetime.now().strftime('%D/%m/%Y %H:%M:%S') + f' [{emojis[type]}] {message}\n')
        session_file.close()
    
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
        session_file = open(self.session_file_path, 'r', encoding='utf-8')
        lines = session_file.readlines()
        regular_log_counts = 0
        titles = 0
        other_logs = ''
        for line in lines:
            if line.startswith('--- '):
                titles += 1
                continue
            if line.split(' ')[2] == '[📄]':
                regular_log_counts += 1
            else:
                other_logs += line

        session_file.close()
        
        return term.bold(str(len(lines) - titles)) + ' entries, of which ' + term.bold(str(regular_log_counts)) + ' regular entries.' + (f' found important entries:\n{other_logs}' if len(other_logs) > 0 else '')