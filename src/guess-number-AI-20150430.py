try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except:
    import simplegui
    
import math
    
TITLE = 'AI guess number'
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 150
CONTROL_WIDTH =  300
AI_hint0 = 'If you choose a number in your mind, I can guess it;-)'
AI_hint1 = 'Input y to play with me~'

in_play = False
guess_limit = 0
guess_prac = 0

limit_lower = '#'
limit_upper = '#'
answer_num = 0
temp0 = '#'

def new_game():

    global AI_hint0, AI_hint1, limit_lower, limit_upper, answer_num, temp0, in_play, guess_limit, guess_prac
    
    in_play = True
    AI_hint0 = 'Now input 2 numbers to tell me the range, format:[lower limit, upper limit]'
    AI_hint1 = 'First the lower limit then the upper one or type in reverse order will both be OK'
    limit_lower = '#'
    limit_upper = '#'
    answer_num = 0
    temp0 = '#'
    guess_limit = 0
    guess_prac = 0

def guess_num(lim_l, lim_u):

    global answer_num, limit_lower, limit_upper

    total = lim_u + 1 - lim_l
    
    if (total % 2 == 0):
        answer_num = lim_l + (total / 2) - 1
    else:
        answer_num = lim_l + ((total - 1) / 2) 
        
    limit_lower = lim_l
    limit_upper = lim_u
    
    return answer_num

def UI_with_AI(inp):

    global in_play, AI_hint0, AI_hint1, guess_limit, guess_prac, limit_lower, limit_upper, temp0
    
    if (not 'Q' == inp[0].upper()):
        if (not in_play):
            if ('Y' != inp[0].upper()):
                AI_hint0 = 'If you want to play with me, input y anytime:-)'
                AI_hint1 = ''
            else:
                new_game()
        else:
            alpha_inp = inp[0].upper()
            if ((0 != guess_prac) and (not (alpha_inp in ['R', 'H', 'L']))):
                AI_hint0 = 'Input: ' + inp + ' You must input R/H/L/Q, or I can\'t understand you:-)'
                AI_hint1 = 'Right? Higher than ' + str(answer_num) + '? Lower than ' + str(answer_num) + '? Quit?'
            elif (0 == guess_prac):
                try:# first to determine the range of this game
                    temp0 = int(inp)
                    AI_hint0 = 'Input: ' + inp
                    if((limit_lower != '#') and (limit_upper != '#')):
                        AI_hint0 =  AI_hint0 + 'Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                        AI_hint1 = 'Input BU to substitute the upper bound, BL to substitue the lower bound.'
                    elif (limit_lower != '#'):
                        minn = min(limit_lower, temp0)
                        maxn = max(limit_lower, temp0)
                        limit_lower = minn
                        limit_upper = maxn
                        AI_hint0 = 'Input C to confirm the range [' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                        AI_hint1 = 'Input a new integer to modify one of the bounds'
                    else:
                        limit_lower = temp0
                        AI_hint0 = 'Input: ' + str(temp0) + ' Next integer input will compare with the lower bound'
                        AI_hint1 = 'The bigger one will be the upper bound, the lower one will be the lower bound'
                except:
                    if ((temp0 != '#') and (inp.upper() in ['BU', 'BL', 'C'])):
                        if (inp.upper() == 'C'):
                            if ((limit_lower != '#') and (limit_upper != '#')):
                                if (limit_upper > limit_lower):
                                    in_play = True
                                    guess_limit = int(math.log(limit_upper - limit_lower, 2)) + 1
                                    guess_prac = 1
                                    AI_hint0 = 'Try 1: ' + str(guess_num(limit_lower, limit_upper))#first guess
                                    AI_hint1 = 'Right? Higher than ' + str(answer_num) + '? Lower than ' + str(answer_num) + '? Quit?'
                                else:
                                    AI_hint0 = 'Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                                    AI_hint1 = 'The upper bound must be bigger than the lower one. Input a new integer please'
                            else:
                                AI_hint0 = 'Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                                AI_hint1 = 'You must input integer(s) to substitue the #(s)'
                        elif (inp.upper() == 'BU'):
                            limit_upper = temp0
                            AI_hint0 = 'Input C to ensure the range, input new value to modify the range'
                            AI_hint1 = 'Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                        else:
                            limit_lower = temp0
                            AI_hint0 = 'Input C to ensure the range, input new value to modify the range'
                            AI_hint1 = 'Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                    elif (temp0 != '#'):
                        AI_hint0 = 'Input BU/BL/C to modify the upper bound/modify the lower bound/confirm the range'
                        AI_hint1 = 'Wait: ' + str(temp0) + ' Range:[' + str(limit_lower) + ', ' + str(limit_upper) + ']'
                    else:
                        AI_hint0 = 'Bounds are not defined. Input INTEGERs to define the range'
                        AI_hint1 = ''
            elif (alpha_inp == 'R'):
                AI_hint0 = 'Aha! I know what you think is ' + str(answer_num) + ':-)'
                AI_hint1 = 'Another game? Input y to play a new game, q to quit'
                in_play = False
            elif (guess_prac >= guess_limit):
                AI_hint0 = 'AI failed...I can\'t figure out the answer'
                AI_hint1 = 'Another game? Input y to play a new game, q to quit'
                in_play = False
            elif (alpha_inp == 'H'):
                guess_prac += 1
                AI_hint0 = 'Well...Try ' + str(guess_prac) + ': ' + str(guess_num(answer_num + 1, limit_upper))
                AI_hint1 = 'Right? Higher than ' + str(answer_num) + '? Lower than ' + str(answer_num) + '? Quit?'
            else:
                guess_prac += 1
                AI_hint0 = 'Well...Try ' + str(guess_prac) + ': ' + str(guess_num(limit_lower, answer_num - 1))
                AI_hint1 = 'Right? Higher than ' + str(answer_num) + '? Lower than ' + str(answer_num) + '? Quit?'
    else:
        AI_hint0 = 'Hope to see you next time:-)'
        AI_hint1 = 'Have a nice day~Input y to play a new game with AI.'
        in_play = False
            
def draw(canvas):

    global AI_hint0, AI_hint1
    
    canvas.draw_text(AI_hint0,  (CANVAS_WIDTH / 8, CANVAS_HEIGHT / 2), 15, 'Red')
    canvas.draw_text(AI_hint1,  (CANVAS_WIDTH / 8, CANVAS_HEIGHT / 2 + 15), 15, 'Red')
    
frame = simplegui.create_frame(TITLE, CANVAS_WIDTH, CANVAS_HEIGHT, CONTROL_WIDTH)
frame.add_input('Input below to talk with AI:', UI_with_AI, 100)
frame.set_draw_handler(draw)
frame.start()
