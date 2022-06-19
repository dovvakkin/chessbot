from lib2to3.pytree import convert

from torch import nonzero
from . import piece
import numpy as np
from PIL import Image
from glob import glob
from copy import deepcopy
from random import randint, choice

initial_notation = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
storage = {}
debug_mode = False

for i in glob("chessbot/Board_images/*.png"):
    name = i.split(".png")[0]
    name = name.replace("\\", "/").split("/")[-1]
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


def convert_array_to_image(arr, previous_move=None):

    board = deepcopy(storage['board'])

    if not previous_move is None:
        for pos in previous_move:

            if np.sum(pos) % 2:
                board.paste(storage['square_dark'], (28 + pos[1]
                            * 90, 28 + pos[0] * 90), storage['square_dark'])
            else:
                board.paste(storage['square_light'], (28 + pos[1]
                            * 90, 28 + pos[0] * 90), storage['square_light'])

    for i, line in enumerate(arr):
        for j, ch in enumerate(line):
            if ch != '':
                board.paste(storage[ch], (33 + j * 90,
                            33 + i * 90), storage[ch])

    return board


def convert_fen_to_image(fen, previous_move=None):
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


class Board():

    def __init__(self, random_mode=False):

        if random_mode:
            self.board_image, self.board_array = generate_random_board()
        else:
            self.board_image, self.board_array = generate_new_board()

        self.board_image.save("chessbot/Current_game/initial_board.png")

        self.black_ghost_piece = None
        self.white_ghost_piece = None

        self.board = []

        for i in range(8):
            self.board.append([None] * 8)

        for i, line in enumerate(self.board_array):
            for j, cell in enumerate(line):

                if cell.__len__():
                    if cell[0] == 'b':
                        flag = False
                    else:
                        flag = True

                    if cell[1] == 'P':
                        self.board[i][j] = piece.Pawn(flag)
                    elif cell[1] == 'R':
                        if j == 0:
                            self.board[i][j] = piece.Rook(
                                flag, king_side=False)
                        else:
                            self.board[i][j] = piece.Rook(flag, king_side=True)
                    elif cell[1] == 'N':
                        self.board[i][j] = piece.Knight(flag)
                    elif cell[1] == 'B':
                        self.board[i][j] = piece.Bishop(flag)
                    elif cell[1] == 'K':
                        self.board[i][j] = piece.King(flag)
                    elif cell[1] == 'Q':
                        self.board[i][j] = piece.Queen(flag)

                    else:
                        raise ImportWarning(
                            "Incorrect symbol enccountered in Board Array")

    def _convert_array_to_fen(self):
        """
        converts 8x8 array (or list of lists) to positional part of FEN notation
        """

        blueprint = []  # using list because joining them such way is less memory-intensive

        for line in self.board_array:

            sub = []

            counter = 0
            for i in range(8):

                if line[i] == '':
                    counter += 1
                else:
                    if counter > 0:
                        sub.append(str(counter))
                    counter = 0

                    if line[i][0] == 'b':
                        sub.append(line[i][1].lower())
                    else:
                        sub.append(line[i][1])

            if counter > 0:
                sub.append(str(counter))

            blueprint.append("".join(sub))

        return "/".join(blueprint)

    def _update_board(self):
        """
        Updates board's array and image from self.board object
        """

        arr = np.empty((8, 8)).astype("str")
        arr[:, :] = ""

        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):

                if elem is None:
                    continue

                if debug_mode:
                    print(elem)
                    print(type(elem))

                if elem.color:
                    prefix = 'w'
                else:
                    prefix = 'b'

                if elem.name == 'GP':
                    continue

                arr[i, j] = prefix + elem.name

        self.board_array = arr
        self.board_image = convert_array_to_image(arr)
        self.board_image.save("chessbot/Current_game/board.png")

    def _print_board(self):
        buffer = ""
        for i in range(33):
            buffer += "*"
        print(buffer)
        for i in range(len(self.board)):
            tmp_str = "|"
            for j in self.board[i]:
                if j == None or j.name == 'GP':
                    tmp_str += "   |"
                elif len(j.name) == 2:
                    tmp_str += (" " + str(j) + "|")
                else:
                    tmp_str += (" " + str(j) + " |")
            print(tmp_str)
        buffer = ""
        for i in range(33):
            buffer += "*"
        print(buffer)
