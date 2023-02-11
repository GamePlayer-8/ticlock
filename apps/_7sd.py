# 7-segment display
from blessed import Terminal
term = Terminal()

class SevenSegmentDisplay:
    def __init__(self, state=[True for i in range(7)]):
        self.state = state

    def render_hori_line(self, x, y, length):
        string = ''
        string += term.move_xy(x + 2, y)
        string += ' ' * (length * 2)
        return string

    def render_vert_line(self, x, y, length):
        string = ''
        for i in range(length):
            string += term.move_xy(x, y + i) + '  '
        return string

    def render(self, x, y, colour = term.on_white, size = 3):
        string = ''
        if self.state[0]:
            string += colour + self.render_hori_line(x, y, size) + term.normal
        if self.state[1]:
            string += colour + self.render_vert_line(x, y + 1, size) + term.normal
        if self.state[2]:
            string += colour + self.render_vert_line(x + 2 + size*2, y + 1, size) + term.normal
        if self.state[3]:
            string += colour + self.render_hori_line(x, y + 1 + size, size) + term.normal
        if self.state[4]:
            string += colour + self.render_vert_line(x, y + 2 + size, size) + term.normal
        if self.state[5]:
            string += colour + self.render_vert_line(x + 2 + size*2, y + 2 + size, size) + term.normal
        if self.state[6]:
            string += colour + self.render_hori_line(x, y + 2 + size*2, size) + term.normal
        return string