"""
GNU GPL 3.0
Mizu /edits by Chimmie
"""

# 7-segment display
from blessed import Terminal
TERM = Terminal()

class SevenSegmentDisplay:
    """
        AI:define_function # Needs work
    """
    def __init__(self, state=[True for i in range(7)]):
        """
            AI:define_function # Needs work
        """
        self.state = state

    def render_hori_line(self, x_position, y_position, length):
        """
            AI:define_function # Needs work
        """
        string = ''
        string += TERM.move_xy(x_position + 2, y_position)
        string += ' ' * (length * 2)
        return string

    def render_vert_line(self, x_position, y_position, length):
        """
            AI:define_function # Needs work
        """
        string = ''
        for i in range(length):
            string += TERM.move_xy(x_position, y_position + i) + '  '
        return string

    def render(self, x_position, y_position, colour = TERM.on_white, size = 3):
        """
            AI:define_function # Needs work
        """
        string = ''
        if self.state[0]:
            string += colour + \
                self.render_hori_line(x_position, y_position, size) + \
                TERM.normal
        if self.state[1]:
            string += colour + \
                self.render_vert_line(x_position, y_position + 1, size) + \
                TERM.normal
        if self.state[2]:
            string += colour + \
                self.render_vert_line(x_position + 2 + size*2, y_position + 1, size) + \
                TERM.normal
        if self.state[3]:
            string += colour + \
                self.render_hori_line(x_position, y_position + 1 + size, size) + \
                TERM.normal
        if self.state[4]:
            string += colour + \
                self.render_vert_line(x_position, y_position + 2 + size, size) + \
                TERM.normal
        if self.state[5]:
            string += colour + \
                self.render_vert_line(x_position + 2 + size*2, y_position + 2 + size, size) + \
                TERM.normal
        if self.state[6]:
            string += colour + \
                self.render_hori_line(x_position, y_position + 2 + size*2, size) + \
                TERM.normal
        return string
