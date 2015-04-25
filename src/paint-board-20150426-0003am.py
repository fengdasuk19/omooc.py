# coding: utf-8

try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except:
    import simplegui

TITLE = 'Paint board v0.4.25.1'
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 800
CONTROL_WIDTH = 300
COUNT_LIMIT = 1024

shape_msg = ''
size_msg = ''
brush_shape = ''
brush_size = 0

history_draw = []
save_draw = [] # wait to write into a file

color_R = 255 
color_G = 255
color_B = 255
color_mix = 'rgb(' + str(color_R) + ', ' + str(color_G) + ', ' + str(color_B) + ')' 
color_msg = ''

playback_rate = 1000
ct_history = -1
max_len = 0
in_play = False
timer_created = False


class Traces:

    def __init__(self,  trace_pos, trace_shape, trace_size, trace_color):
    
        self.pos = trace_pos
        self.shape = trace_shape
        self.size = trace_size
        self.color = trace_color

class Brushes:
    
    def __init__(self, what_pos, which_shape, what_size, what_color):
        
        self.pos = what_pos
        self.shape = which_shape
        self.size = what_size
        self.color = what_color
        
    def draw(self, canvas):
        
        if ("t" == self.shape):
            canvas.draw_polygon(((self.pos[0] - self.size * (3 ** (1.0 / 2)) / 2, self.pos[1] + self.size / 2.0),
                               (self.pos[0] + self.size * (3 ** (1.0 / 2)) / 2, self.pos[1] + self.size / 2.0),
                               (self.pos[0], self.pos[1] - self.size)), 10, self.color, self.color)
        elif ("r" == self.shape):
            canvas.draw_polygon(((self.pos[0] - self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] - self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] - self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] + self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] + self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] + self.size * (2 ** (1.0 / 2)) / 2),
                               (self.pos[0] + self.size * (2 ** (1.0 / 2)) / 2, self.pos[1] - self.size * (2 ** (1.0 / 2)) / 2)), 10, self.color, self.color)
        elif ("c" == self.shape):
            try:
                canvas.draw_circle(self.pos, self.size, 10, self.color, self.color)
            except:
                global size_msg
                size_msg = 'Radius must be no less than 0'

def draw(canvas):
    
    global shape_msg, size_msg, shape_label, size_label, brush_shape, brush_size, color_msg, ct_history, max_len, timer, in_play, timer_created
    
    say_shape = 'Shape: ' + shape_msg
    shape_label.set_text(say_shape)
    say_size = 'Size: ' + size_msg
    size_label.set_text(say_size)
    
    for i in history_draw:
        painter_brush = Brushes(i.pos, i.shape, i.size, i.color)
        painter_brush.draw(canvas)
    
    if ((not in_play) and (True == timer_created)):
        timer.stop()
        timer_created = False
        

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
        shape_msg = 'Error: not alphabetic'

def size_choice(inp):
    
    global size_msg, brush_size
    
    try:
        brush_size = float(inp)
        if (brush_size <= 0):
            raise ValueError
        size_msg = str(brush_size)
    except:
        size_msg = 'Pleas input a positive number.'
    
    
def set_R(inp):

    global color_R, color_msg, color_mix
    
    try:
        color_R = int(inp)
        if (not color_R in range(0, 256)):
            raise ValueError
        color_msg = 'Color: ' + color_mix
        color_label.set_text(color_msg)
    except:
        color_msg = 'Color: Input an integer for R, range:[0, 255]'
        color_label.set_text(color_msg)
    
def set_G(inp):

    global color_G, color_msg, color_mix
    
    try:
        color_G = int(inp)
        if (not color_G in range(0, 256)):
            raise ValueError
        color_msg = 'Color: ' + color_mix
        color_label.set_text(color_msg)
    except:
        color_msg = 'Color: Input an integer for G, range:[0, 255]'
        color_label.set_text(color_msg)
    
def set_B(inp):

    global color_B, color_msg, color_mix
    
    try:
        color_B = int(inp)
        if (not color_B in range(0, 256)):
            raise ValueError
        color_msg = 'Color: ' + color_mix
        color_label.set_text(color_msg)
    except:
        color_msg = 'Color: Input an integer for B, range:[0, 255]'
        color_label.set_text(color_msg)
    
def set_color():    # mix R&G&B to attain a new color

    global color_R, color_G, color_B, color_mix

    color_mix = 'rgb(' + str(color_R) + ', ' + str(color_G) + ', ' + str(color_B) + ')' 
    color_label.set_text('Color: ' + color_mix)
    

def brush_of_painter(pos):  # when click on the canvas...
    
    global brush_shape, brush_size, ct_history
    
    if ((ct_history <= COUNT_LIMIT) and (brush_shape in ['t', 'r', 'c']) and (brush_size > 0)):
        t = Traces(tuple(pos), brush_shape, brush_size, color_mix)
        history_draw.append(t)
        ct_history += 1

def clear_canvas():

    global history_draw, save_draw, ct_history
    
    history_draw = []
    ct_history = -1
    
def save_pic():

    global history_draw, save_draw, max_len
    save_draw = list(history_draw)
    max_len = len(save_draw)
    
def reapr_pic_whole():

    global history_draw, save_draw, ct_history
    history_draw = list(save_draw)
    max_len = len(history_draw)
    ct_history = max_len - 1
    
def playback_sbs():

    global in_play, timer, ct_history, history_draw, save_draw, timer_created, playback_rate
    
    ct_history = -1
    history_draw = []
    if ((not in_play) and (0 != len(save_draw))):
        in_play = True
        timer = simplegui.create_timer(playback_rate, timer_handler)
        timer_created = True
        timer.start()
    
def change_playback_rate(inp):

    global playback_rate
    
    try:
        playback_rate = float(inp)
        if (playback_rate <= 0):
            raise ValueError
        playback_rate_label.set_text('Playback rate of drawing procedure: ' + str(playback_rate) + ' msec / trace')
    except:
        playback_rate_label.set_text('Input a positive number please')
    
    
def timer_handler():

    global ct_history, timer, in_play, max_len
    
    ct_history += 1
    history_draw.append(save_draw[ct_history])
    if (ct_history == max_len - 1):
        in_play = False
    
    
def read_file(inp):

    global readf, history_draw, save_draw, max_len
    
    try:
        readf = open(inp, 'r+')
        history_draw = []
        save_draw = []
        max_len = int(readf.readline())
        readf.readline()
        i = 1
        while (i <= max_len):
            pos_x = float(readf.readline())
            pos_y = float(readf.readline())
            shapes = readf.readline()[0]
            sizes = float(readf.readline())
            t = readf.readline()
            j = 0
            colors = ''
            while (t[j] != ')'):
                colors += t[j]
                j += 1
            colors += ')'
            readf.readline()
            save_draw.append(Traces((pos_x, pos_y), shapes, sizes, colors)) 
            i += 1
        readf.close()
        readf_label.set_text('Read ' + inp + ' successfully!')
    except:
        readf_label.set_text('No such a file. Input correct file name please.')
    
def write_file(inp):

    global writef, max_len
    
    try:
        writef = open(inp, 'w')
        writef.write(str(max_len))  #float -> string, only string can be write into file
        writef.write('\n') 
        writef.write('\n') 
        for i in save_draw:
            writef.write(str(i.pos[0]))  #float
            writef.write('\n')
            writef.write(str(i.pos[1]))  #float
            writef.write('\n')
            writef.write(i.shape)   #string
            writef.write('\n')
            writef.write(str(i.size))    #float
            writef.write('\n')
            writef.write(i.color)   #string
            writef.write('\n')
            writef.write('\n')
        writef.close()
        writef_label.set_text('Save as ' + inp + ' successfully!')
    except:
        writef_label.set_text('Input correct file name please.')
    
    
frame = simplegui.create_frame(TITLE, CANVAS_WIDTH,
                               CANVAS_HEIGHT, CONTROL_WIDTH)
frame.set_draw_handler(draw)

frame.add_label('Click the button below to CLEAR the canvas')
frame.add_button('Clear', clear_canvas)

readf_label = frame.add_label('Want to read your picture?')
frame.add_input(' Input its name below, and it\'ll be read from outside:', read_file, 110)

shape_label = frame.add_label(shape_msg)
size_label = frame.add_label(size_msg)
color_label = frame.add_label('Color: ' + color_msg)
frame.add_input('Shape:(input t/r/c)', shape_choice, 110)
frame.add_input('Size:(input a number here) ', size_choice, 110)

frame.add_label('Input colr below')
text4color_R = frame.add_input('R:(input an integer here) ', set_R, 110)
text4color_G = frame.add_input('G:(input an integer here) ', set_G, 110)
text4color_B = frame.add_input('B:(input an integer here) ', set_B, 110)
frame.add_label('Press Enter to update R/G/B after each input, then click the button below to get a new brush with a new color')
frame.add_button('Mix them!', set_color)

frame.add_label('Click the button below to SAVE the picture')
frame.add_button('Save', save_pic)
writef_label = frame.add_label('Want to transform **what you\'ve saved** into a portable file?')
frame.add_input('Name your works below, then press Enter:', write_file, 110)

frame.add_label('Click the button below to REAPPEAR the WHOLLE picture')
frame.add_button('Reappear WHOLE', reapr_pic_whole)

frame.add_label('Input new playback rate of the drawing procedure in the box below, press Enter to confirm your update')
frame.add_input('(Default: 1000 msec / trace): ', change_playback_rate, 110)
frame.add_label('Click the button below to REAPPEAR the picture STEP BY STEP')
playback_rate_label = frame.add_label('Playback rate of drawing procedure: ' + str(playback_rate) + ' msec / trace')
frame.add_button('Playback STEP BY STEP', playback_sbs)

frame.set_mouseclick_handler(brush_of_painter)

frame.start()
