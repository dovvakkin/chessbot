from PIL import Image
import numpy as np
from glob import glob
from copy import deepcopy
from random import randint, choice

initial_notation = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
storage = {}

for i in glob("Board_images/*.png"):
    name = i.split(".png")[0]
    name = name.replace("\\", "/").split("/")[1]
    storage[name] = Image.open(i)

def _convert_fen_to_array(notation):
    
    arr = np.empty((8, 8)).astype("str")
    arr[:, :] = ""
    
    board_pt = notation.split(" ")[0]
    board = board_pt.replace("\\", "/").split("/")
    
    for i, line in enumerate(board):

        pos = 0
        for ch in line:
            
            if ch.isdigit():
                pos += int(ch)
            
            else:
                fig = ""
                
                if ch.lower() == ch:
                    fig = "b" + ch.upper()
                else:
                    fig = "w" + ch
                    
                arr[i, pos] = fig
                pos += 1
                
    return arr

def convert_array_to_image(arr, previous_move = None):
    
    board = deepcopy(storage['board'])
    
    if not previous_move is None:
        for pos in previous_move:
            
            if np.sum(pos) % 2:
                board.paste(storage['square_dark'], (28 + pos[1] * 90, 28 + pos[0] * 90), storage['square_dark'])
            else:
                board.paste(storage['square_light'], (28 + pos[1] * 90, 28 + pos[0] * 90), storage['square_light'])

    for i, line in enumerate(arr):
        for j, ch in enumerate(line):
            if ch != '':
                board.paste(storage[ch], (33 + j * 90, 33 + i * 90), storage[ch])
            
    return board

def convert_fen_to_image(fen, previous_move = None):
    
    """
    Transforms FEN notation to board image
    
    params:
    fen : string
    Chess notation
    
    previous_move : None or array (list) of size 2, 2 - coordinates of previous and new position of last move
    """
    arr = _convert_fen_to_array(fen)
    return convert_array_to_image(arr, previous_move)

def generate_new_board():

    """
    Generates board from default fen notation
    Returns PIL.Image board object + array of figures
    """

    img = convert_fen_to_image(initial_notation)
    arr = _convert_fen_to_array(initial_notation)

    return img, arr

def generate_random_board():

    """
    Generates board with random initial setup 
    """

    first_row = ['R', 'N', 'B', 'Q']
    second_row = first_row + ['P']

    arr = np.empty((8, 8)).astype(str)
    arr[:, :] = ""

    wx, bx = randint(0, 7), randint(0, 7)
    arr[0, bx] = 'bK'
    arr[7, wx] = 'wK'

    b_first_layer = [x for x in range(8) if x != bx]
    for pos in b_first_layer:
        arr[0, pos] = 'b' + choice(first_row)

    w_first_layer = [x for x in range(8) if x != wx]
    for pos in w_first_layer:
        arr[7, pos] = 'w' + choice(first_row)

    for i in range(8):
        arr[1, i] = 'b' + choice(second_row)
        arr[6, i] = 'w' + choice(second_row)

    return convert_array_to_image(arr), arr

