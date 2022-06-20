"""Module with board representing class and FEN notation handling."""

from copy import deepcopy
from glob import glob
from random import choice, randint

from PIL import Image

import numpy as np

from . import piece

INITIAL_NOTATION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
STORAGE = {}
DEBUG_MODE = False

for k in glob("chessbot/Board_images/*.png"):
    name = k.split(".png")[0]
    name = name.replace("\\", "/").split("/")[-1]
    STORAGE[name] = Image.open(k)


def convert_fen_to_array(notation):
    """Convert positional part of FEN notation to 8x8 array (or list of lists)."""
    arr = np.empty((8, 8)).astype("str")
    arr[:, :] = ""

    board_pt = notation.split(" ")[0]
    board = board_pt.replace("\\", "/").split("/")

    for j, line in enumerate(board):

        pos = 0
        for character in line:

            if character.isdigit():
                pos += int(character)

            else:
                fig = ""

                if character.lower() == character:
                    fig = "b" + character.upper()
                else:
                    fig = "w" + character

                arr[j, pos] = fig
                pos += 1

    return arr


def convert_array_to_image(arr, previous_move=None):
    """Convert numpy array board representation to png image."""
    board = deepcopy(STORAGE['board'])

    if not previous_move is None:
        for pos in previous_move:

            if np.sum(pos) % 2:
                board.paste(STORAGE['square_dark'], (28 + pos[1]
                            * 90, 28 + pos[0] * 90), STORAGE['square_dark'])
            else:
                board.paste(STORAGE['square_light'], (28 + pos[1]
                            * 90, 28 + pos[0] * 90), STORAGE['square_light'])

    for i, line in enumerate(arr):
        for j, character in enumerate(line):
            if character != '':
                board.paste(STORAGE[character], (33 + j * 90,
                            33 + i * 90), STORAGE[character])

    return board


def convert_fen_to_image(fen, previous_move=None):
    """
    Transform FEN notation to board image.

    params:
    fen : string
    Chess notation

    previous_move : None or array (list) of size 2, 2 - coordinates of
    previous and new position of last move
    """
    arr = convert_fen_to_array(fen)
    return convert_array_to_image(arr, previous_move)


def generate_new_board(notation, random_mode = False):
    """
    Generate chess board. Can either generate from FEN notation or random_state.

    Returns board image and string matrix of inner board representation.
    """
    if random_mode:

        first_row = ['R', 'N', 'B', 'Q']
        second_row = first_row + ['P']

        arr = np.empty((8, 8)).astype(str)
        arr[:, :] = ""

        w_x, b_x = randint(0, 7), randint(0, 7)
        arr[0, b_x] = 'bK'
        arr[7, w_x] = 'wK'

        b_first_layer = [x for x in range(8) if x != b_x]
        for pos in b_first_layer:
            arr[0, pos] = 'b' + choice(first_row)

        w_first_layer = [x for x in range(8) if x != w_x]
        for pos in w_first_layer:
            arr[7, pos] = 'w' + choice(first_row)

        for i in range(8):
            arr[1, i] = 'b' + choice(second_row)
            arr[6, i] = 'w' + choice(second_row)

        return convert_array_to_image(arr), arr

    img = convert_fen_to_image(notation)
    arr = convert_fen_to_array(notation)
    return img, arr

class Board():
    """
    Class to represent a chess board.

    ...
    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board

    turn : bool
        True if white's turn
    board_image : Image
        PIL Image of the board
    board_array : list[list[Piece]]
        chess board in specific array for image and FEN
    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant
    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant
    """

    def __init__(self, random_mode = False, notation = INITIAL_NOTATION):
        """Game board initialization."""
        self.board_image, self.board_array = generate_new_board(notation = notation,
                                                                random_mode = random_mode
                                                                )

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
                        elif j == 7:
                            self.board[i][j] = piece.Rook(flag, king_side=True)
                        else:
                            self.board[i][j] = piece.Rook(flag, first_move=False, king_side=False)
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
        """Convert 8x8 array (or list of lists) to positional part of FEN notation."""
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
        """Update board's array and image from self.board object."""
        arr = np.empty((8, 8)).astype("str")
        arr[:, :] = ""

        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):

                if elem is None:
                    continue

                if DEBUG_MODE:
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
