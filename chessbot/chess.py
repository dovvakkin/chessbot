"""Module for chess logic representation."""
from . import board
from . import piece


class Chess():
    """
    Class to represent the game of chess.

    ...
    Attributes:
    -----------
    board : Board
        represents the chess board of the game
    turn : bool
        True if white's turn
    turn_number : int
        Counter of rthe current move
    halfstep_number : int
        Counter of halfsteps (only pawns)
    random_mode : bool
        Random mode for shess positions
    castling : str
        String describing possibility of castling in FEN
    """

    def __init__(self, random_mode=False, notation = board.INITIAL_NOTATION):
        """Initialize game state."""
        self.board = board.Board(random_mode = random_mode, notation = notation)

        self.turn = True
        self.turn_number = 1
        self.halfstep_number = 0

        self.random_mode = random_mode
        if random_mode:
            self.castling = '-'

        else:
            self.castling = "KQkq"

        self.fen = self._update_fen()

    def has_piece_under(self, start):
        """Return True if there is piece on given coord."""
        if self.board.board[start[0]][start[1]] is None:
            return False
        if self.board.board[start[0]][start[1]].name == "GP":
            return False
        return True

    def move(self, start, to):
        """
        Move a piece at `start` to `to`.

        Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.
        start : tup
            Position of a piece to be moved
        to : tup
            Position of where the piece is to be moved

        precondition: `start` and `to` are valid positions on the board
        """
        # pylint: disable=unsubscriptable-object, too-many-statements, too-many-return-statements
        if self.board.board[start[0]][start[1]] is None:
            return 0

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            return 0

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece is not None

        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            return 0

        if target_piece.is_valid_move(self.board, start, to):

            # for FEN calculation (turn numbers)
            if not self.turn:
                self.turn_number += 1
            # for FEN calculation (castling state)
            if self.castling != "-":
                if target_piece.name == 'R':
                    if target_piece.king_side:
                        if self.turn:
                            self.castling = self.castling.replace("K", "")
                        else:
                            self.castling = self.castling.replace("k", "")
                    else:
                        if self.turn:
                            self.castling = self.castling.replace("Q", "")
                        else:
                            self.castling = self.castling.replace("q", "")
                if target_piece.name == 'K':
                    if self.turn:
                        self.castling = self.castling.replace("K", "")
                        self.castling = self.castling.replace("Q", "")
                    else:
                        self.castling = self.castling.replace("k", "")
                        self.castling = self.castling.replace("q", "")
                if self.castling == "":
                    self.castling = "-"

            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:

                if self.turn and self.board.black_ghost_piece:
                    self.board.board[self.board.black_ghost_piece[0]
                                     ][self.board.black_ghost_piece[1]] = None
                elif not self.turn and self.board.white_ghost_piece:
                    self.board.board[self.board.white_ghost_piece[0]
                                     ][self.board.white_ghost_piece[1]] = None
                self.turn = not self.turn
                self._update_fen()
                return 1

            if target_piece.name == 'P' and (to[0] == 0 or to[0] == 7):
                self.board.board[to[0]][to[1]] = piece.Queen(self.turn)
                self.board.board[start[0]][start[1]] = None

                if self.turn and self.board.black_ghost_piece:
                    self.board.board[self.board.black_ghost_piece[0]
                                    ][self.board.black_ghost_piece[1]] = None
                    self.board.black_ghost_piece = None
                elif not self.turn and self.board.white_ghost_piece:
                    self.board.board[self.board.white_ghost_piece[0]
                                    ][self.board.white_ghost_piece[1]] = None
                    self.board.white_ghost_piece = None

                self.turn = not self.turn
                self._update_fen()
                return 1

            if self.board.board[to[0]][to[1]]:
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[
                            self.board.black_ghost_piece[0] + 1
                        ][
                            self.board.black_ghost_piece[1]
                        ] = None
                        self.board.black_ghost_piece = None
                    else:
                        self.board.board[self.board.white_ghost_piece[0] -
                                         1][self.board.white_ghost_piece[1]] = None
                        self.board.white_ghost_piece = None
                if self.board.board[to[0]][to[1]].name == 'K':
                    return -1


            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None

            if self.turn and self.board.black_ghost_piece:
                self.board.board[self.board.black_ghost_piece[0]
                                 ][self.board.black_ghost_piece[1]] = None
                self.board.black_ghost_piece = None
            elif not self.turn and self.board.white_ghost_piece:
                self.board.board[self.board.white_ghost_piece[0]
                                 ][self.board.white_ghost_piece[1]] = None
                self.board.white_ghost_piece = None

            self.turn = not self.turn
            self._update_fen()
            return 1

        return 0

    def _reverse_translate(self, pos):
        """Translate coordinates to literal positions."""
        dictionary = {0: 'a', 1: 'b', 2: 'c',
                      3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        return dictionary[pos[1]] + str(8 - pos[0])

    def _update_fen(self):
        """Generate full FEN notation from inner representation of game."""
        #pylint: disable=protected-access
        # 0 - update iternal array and image of board:
        self.board._update_board()

        fen_container = []

        # 1 - get positional notation:
        fen_container.append(self.board._convert_array_to_fen())

        # 2 - get side
        if self.turn:
            fen_container.append('w')
        else:
            fen_container.append('b')

        # 3 - get castling
        fen_container.append(self.castling)

        # 4 - get ghost pieces
        if not self.board.white_ghost_piece is None:
            fen_container.append(
                self._reverse_translate(self.board.white_ghost_piece))
        elif not self.board.black_ghost_piece is None:
            fen_container.append(
                self._reverse_translate(self.board.black_ghost_piece))
        else:
            fen_container.append('-')

        # 5 - halfturns
        fen_container.append(str(self.halfstep_number))

        # 6 - turns
        fen_container.append(str(self.turn_number))

        self.fen = " ".join(fen_container)

        return self.fen

def translate(literal_pos):
    """Translate literal positions to coordinates."""
    try:
        row = int(literal_pos[1])
        col = literal_pos[0]
        if row < 1 or row > 8:
            return None
        if col < 'a' or col > 'h':
            return None
        dictionary = {'a': 0, 'b': 1, 'c': 2,
                      'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dictionary[col])
    except KeyError:
        return None
