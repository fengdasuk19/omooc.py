# coding: utf-8

try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except:
    import simplegui
    
import math

title = 'Paint board v0.4.25.1'
canvas_width = 500
canvas_height = 500
control_width = 250

shape_msg = ''
size_msg = ''
brush_shape = ''
brush_size = 0

history_draw = []

class Traces:

    def __init__(self,  trace_pos, trace_shape, trace_size):
    
        self.pos_xy = trace_pos
        self.shape = trace_shape
        self.size = trace_size

class Brushes:
    
    def __init__(self, what_pos, which_shape, what_size):
        
        self.pos = what_pos
        self.shape = which_shape
        self.size = what_size
        
    def draw(self, canvas):
        
        if ("t" == self.shape):
            canvas.draw_polygon(((self.pos[0] - self.size * (3 ** (1.0 / 2)) / 2, self.pos[1] + self.size / 2.0),
                               (self.pos[0] + self.size * (3 ** (1.0 / 2)) / 2, self.pos[1] + self.size / 2.0),
                               (self.pos[0], self.pos[1] - self.size)), 10, 'Red', 'Red')
        elif ("r" == self.shape):
            canvas.draw_polygon(((self.pos[0] - self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] - self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] - self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] + self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] + self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] + self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] + self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] - self.size * (2 ** (1.0 / 2)) / 2)), 10, 'Red', 'Red')
        elif ("c" == self.shape):
            try:
                canvas.draw_circle(self.pos, self.size, 10, 'Red', 'Red')
            except:
                global size_msg
                size_msg = 'Radius must be no less than 0'

def draw(canvas):
    
    global shape_msg, size_msg, shape_label, size_label, brush_shape, brush_size
    
    say_shape = 'Shape: ' + shape_msg
    shape_label.set_text(say_shape)
    say_size = 'Size: ' + size_msg
    size_label.set_text(say_size)
    
    for i in history_draw:
        painter_brush = Brushes(i.pos_xy, i.shape, i.size)
        painter_brush.draw(canvas)
        

def shape_choice(inp):
    
    global shape_msg, brush_shape
       
    if (ord(inp[0]) in range(ord('a'), ord('z'))) or (ord(inp[0]) in range(ord('A'), ord('Z'))):
        inp = inp[0].lower()
        if ('t' == inp):
            shape_msg = 'triangle'
            brush_shape = 't'
        elif ('r' == inp):
            shape_msg = 'rectangle'
            brush_shape = 'r'
        elif ('c' == inp):
            shape_msg = 'circle'
            brush_shape = 'c'
        else:
            shape_msg = 'Input t/r/c'
    else:
        outcome0 = 'Error: not alphabetic'

def size_choice(inp):
    
    global size_msg, brush_size
    
    try:
        brush_size = float(inp)
        size_abs = math.fabs(brush_size)
        test_positive = 1 / (1 + brush_size / size_abs)
        size_msg = str(brush_size)
    except (ValueError, ZeroDivisionError):
        size_msg = 'Pleas input a positive number.'
    
    
def brush_of_painter(pos):
    
    global brush_shape, brush_size
    
    if ((brush_shape in ['t', 'r', 'c']) and (brush_size > 0)):
        t = Traces(pos, brush_shape, brush_size)
        history_draw.append(t)
    
        
frame = simplegui.create_frame(title, canvas_width,
                               canvas_height, control_width)
frame.set_draw_handler(draw)
shape_label = frame.add_label(shape_msg)
size_label = frame.add_label(size_msg)
frame.add_label('Input t to select brush with TRIANGLE')
frame.add_label('Input r to select brush with RECTANGLE')
frame.add_input('Input c to select brush with CIRCLE', shape_choice, 110)
frame.add_input('Size:(input a number here) ', size_choice, 110)
#frame.add_input('Color_1:(input an integer here) ', size_choice, 110)
frame.set_mouseclick_handler(brush_of_painter)
frame.start()
