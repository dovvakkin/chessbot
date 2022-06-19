"""Module with pieces movement logic."""
from copy import deepcopy

def check_knight(color, board, pos):
    """Check if there is a knight of the opposite `color` at position `pos` on board `board`."""
    piece = board.board[pos[0]][pos[1]]
    if piece is not None and piece.color != color and piece.name == 'N':
        return False
    return True


def check_diag_castle(color, board, start, to):
    """
    Check the diagonal path from `start` (non-inclusive) to `to` (inclusive) on board `board`.

    For any threats from the opposite `color`.
    """
    if abs(start[0] - to[0]) != abs(start[1] - to[1]):
        return False

    x_pos = 1 if to[0] - start[0] > 0 else -1
    y_pos = 1 if to[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos

    exists_piece = board.board[i][j] is not None
    if exists_piece and (board.board[i][j].name in ('P', 'K')) and \
            board.board[i][j].color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):

        if exists_piece and board.board[i][j].color != color:
            if board.board[i][j].name in ['B', 'Q']:
                return False
            return True

        if exists_piece and board.board[i][j].color == color:
            return True

        i += x_pos
        j += y_pos

        if min(i, j) < 0 or max(i, j) > 7:
            continue

        exists_piece = board.board[i][j] is not None

    return True


def check_diag(board, start, to):
    """
    Check if there are no pieces along the diagonal.

    Path from `start` (non-inclusive) to `to` (non-inclusive).
    """
    if abs(start[0] - to[0]) != abs(start[1] - to[1]):
        return False

    x_pos = 1 if to[0] - start[0] > 0 else -1
    y_pos = 1 if to[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos
    while (i < to[0] if x_pos == 1 else i > to[0]):
        if board.board[i][j] is not None:
            return False
        i += x_pos
        j += y_pos
    return True


def check_check(color, board, position):
    """
    Calculate check position.

    color: Boolean
    True if White, False if Black

    board: List
    list of Pieces / None

    position: tuple(2)
    King's position
    """
    directions = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
    knight_directions = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]

    for direction in knight_directions:
        # checking for Horse

        x_coord, y_coord = direction[0] + position[0], direction[1] + position[1]

        if min(x_coord, y_coord) < 0 or max(x_coord, y_coord) > 7:
            continue

        if ~check_knight(color, board, (x_coord, y_coord)):
            return True

    for direction in directions:

        i, j = deepcopy(position)
        x_dir, y_dir = direction
        first_step = True

        while min(i, j) >= 0 and max(i, j) <= 7:

            i += x_dir
            j += y_dir

            if min(i, j) < 0 or max(i, j) > 7:
                break

            if board.board[i][j] is None:
                continue
            # при проверке соседних клеток хотим игнорировать самого короля
            if board.board[i][j].name == 'K' and board.board[i][j].color == color:
                continue

            if board.board[i][j].color == color:
                break

            if abs(direction[0]) + abs(direction[1]) == 2: #diag

                if first_step:
                    first_step = False

                    if board.board[i][j] == 'P':

                        if color: # white king
                            if i < position[0]:
                                return True
                        else:
                            if i > position[0]:
                                return False

                if board.board[i][j].name in ['B', 'Q']:
                    return True

            else: #line

                if board.board[i][j].name in ['R', 'Q']:
                    return True

    return False

def check_updown_castle(color, board, start, to):
    """
    Check if there are any threats from the opposite.

    `color` from `start` (non-inclusive) to `to` (inclusive) on board `board`.
    """
    x_pos = 1 if to[0] - start[0] > 0 else -1
    i = start[0] + x_pos

    front_piece = board.board[i][start[1]]
    if front_piece is not None and front_piece.name == 'K' and front_piece.color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):
        if board.board[i][start[1]] is not None and board.board[i][start[1]].color != color:
            if board.board[i][start[1]].name in ['R', 'Q']:
                return False
            return True

        if board.board[i][start[1]] is not None and board.board[i][start[1]].color == color:
            return True

        i += x_pos

    return True

def check_updown(board, start, to):
    """
    Check if there are no pieces along the vertical or horizontal path.

    From `start` (non-inclusive) to `to` (non-inclusive).
    """
    if start[0] == to[0]:
        smaller_y = start[1] if start[1] < to[1] else to[1]
        bigger_y = start[1] if start[1] > to[1] else to[1]

        for i in range(smaller_y + 1, bigger_y):
            if board.board[start[0]][i] is not None:
                return False
        return True

    smaller_x = start[0] if start[0] < to[0] else to[0]
    bigger_x = start[0] if start[0] > to[0] else to[0]

    for i in range(smaller_x + 1, bigger_x):
        if board.board[i][start[1]] is not None:
            return False
    return True


class Piece():
    """
    A class to represent a piece in chess.

    ...
    Attributes:
    -----------
    name : str
        Represents the name of a piece as following -
        Pawn -> P
        Rook -> R
        Knight -> N
        Bishop -> B
        Queen -> Q
        King -> K
    color : bool
        True if piece is white
    """

    def __init__(self, color):
        """Init piece name and color."""
        self.name = ""
        self.color = color

    def is_valid_move(self, board, start, to): # pylint: disable=unused-argument
        """Check if proposed move is valid."""
        return False

    def is_white(self):
        """Return color of piece."""
        return self.color

class Rook(Piece):
    """Rook piece."""

    def __init__(self, color, first_move=True, king_side=True):
        """Init piece name, color and first move."""
        super().__init__(color)
        self.name = "R"
        self.first_move = first_move
        self.king_side = king_side

    def is_valid_move(self, board, start, to):
        """Check if proposed move is valid."""
        if start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        return False


class Knight(Piece):
    """Knight piece."""

    def __init__(self, color):
        """Init piece name and color."""
        super().__init__(color)
        self.name = "N"

    def is_valid_move(self, board, start, to): # pylint: disable=unused-argument
        """Check if proposed move is valid."""
        if abs(start[0] - to[0]) == 2 and abs(start[1] - to[1]) == 1:
            return True
        if abs(start[0] - to[0]) == 1 and abs(start[1] - to[1]) == 2:
            return True
        return False


class Bishop(Piece):
    """Bishop piece."""

    def __init__(self, color):
        """Init piece name and color."""
        super().__init__(color)
        self.name = "B"

    def is_valid_move(self, board, start, to):
        """Check if proposed move is valid."""
        return check_diag(board, start, to)


class Queen(Piece):
    """Queen piece."""

    def __init__(self, color):
        """Init piece name and color."""
        super().__init__(color)
        self.name = "Q"

    def is_valid_move(self, board, start, to):
        """Check if proposed move is valid."""
        if abs(start[0] - to[0]) == abs(start[1] - to[1]):
            return check_diag(board, start, to)

        if start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)

        return False


class King(Piece):
    """King piece."""

    def __init__(self, color, first_move=True):
        """Init piece name and color."""
        super().__init__(color)
        self.name = "K"
        self.first_move = first_move

    def can_castle(self, board, start, to, right): # pylint: disable=too-many-return-statements, inconsistent-return-statements
        """Return True if king at `start` can move to `to` on `board` for castling."""
        if self.color and right:
            knight_attack = check_knight(self.color, board, (6, 3)) and \
                check_knight(self.color, board, (6, 4)) and \
                check_knight(self.color, board, (5, 4)) and \
                check_knight(self.color, board, (5, 5)) and \
                check_knight(self.color, board, (5, 6)) and \
                check_knight(self.color, board, (5, 7)) and \
                check_knight(self.color, board, (6, 7))
            if not knight_attack:
                return False

            diags = check_diag_castle(self.color, board, (7, 5), (2, 0)) and \
                check_diag_castle(self.color, board, (7, 6), (1, 0)) and \
                check_diag_castle(self.color, board, (7, 5), (5, 7)) and \
                check_diag_castle(self.color, board, (7, 6), (6, 7))
            if not diags:
                return False

            updowns = check_updown_castle(self.color, board, (7, 5), (0, 5)) and \
                check_updown_castle(self.color, board, (7, 6), (0, 6))
            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(True, False)
            board.board[to[0]][to[1]-1] = Rook(True, False)
            board.board[start[0]][start[1]] = None
            board.board[7][7] = None
            return True

        if self.color and not right:
            knight_attack = check_knight(self.color, board, (6, 0)) and \
                check_knight(self.color, board, (6, 1)) and \
                check_knight(self.color, board, (5, 1)) and \
                check_knight(self.color, board, (5, 2)) and \
                check_knight(self.color, board, (5, 3)) and \
                check_knight(self.color, board, (5, 4)) and \
                check_knight(self.color, board, (6, 4)) and \
                check_knight(self.color, board, (6, 5))
            if not knight_attack:
                return False

            diags = check_diag_castle(self.color, board, (7, 2), (5, 0)) and \
                check_diag_castle(self.color, board, (7, 3), (4, 0)) and \
                check_diag_castle(self.color, board, (7, 2), (2, 7)) and \
                check_diag_castle(self.color, board, (7, 3), (3, 7))
            if not diags:
                return False

            updowns = check_updown_castle(self.color, board, (7, 2), (0, 2)) and \
                check_updown_castle(self.color, board, (7, 3), (0, 3))
            if not updowns:
                return False
            board.board[to[0]][to[1]] = King(True, False)
            board.board[to[0]][to[1]+1] = Rook(True, False)
            board.board[start[0]][start[1]] = None
            board.board[7][0] = None

            return True

        if not self.color and right:
            knight_attack = check_knight(self.color, board, (1, 3)) and \
                check_knight(self.color, board, (1, 4)) and \
                check_knight(self.color, board, (1, 7)) and \
                check_knight(self.color, board, (2, 4)) and \
                check_knight(self.color, board, (2, 5)) and \
                check_knight(self.color, board, (2, 6)) and \
                check_knight(self.color, board, (2, 7))
            if not knight_attack:
                return False

            diags = check_diag_castle(self.color, board, (0, 5), (5, 0)) and \
                check_diag_castle(self.color, board, (0, 6), (6, 0)) and \
                check_diag_castle(self.color, board, (0, 5), (2, 7)) and \
                check_diag_castle(self.color, board, (0, 6), (1, 7))
            if not diags:
                return False

            updowns = check_updown_castle(self.color, board, (0, 2), (7, 2)) and \
                check_updown_castle(self.color, board, (0, 3), (7, 3))
            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(False, False)
            board.board[to[0]][to[1]-1] = Rook(False, False)
            board.board[start[0]][start[1]] = None
            board.board[0][7] = None

            return True

        if not self.color and not right:
            knight_attack = check_knight(self.color, board, (1, 0)) and \
                check_knight(self.color, board, (1, 1)) and \
                check_knight(self.color, board, (1, 4)) and \
                check_knight(self.color, board, (1, 5)) and \
                check_knight(self.color, board, (2, 1)) and \
                check_knight(self.color, board, (2, 2)) and \
                check_knight(self.color, board, (2, 3)) and \
                check_knight(self.color, board, (2, 4))
            if not knight_attack:
                return False

            diags = check_diag_castle(self.color, board, (0, 2), (5, 7)) and \
                check_diag_castle(self.color, board, (0, 3), (4, 7)) and \
                check_diag_castle(self.color, board, (0, 2), (2, 0)) and \
                check_diag_castle(self.color, board, (0, 3), (3, 0))
            if not diags:
                return False

            updowns = check_updown_castle(self.color, board, (0, 2), (7, 2)) and \
                check_updown_castle(self.color, board, (0, 3), (7, 3))

            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(False, False)
            board.board[to[0]][to[1]+1] = Rook(False, False)
            board.board[start[0]][start[1]] = None
            board.board[0][0] = None

            return True

    def is_valid_move(self, board, start, to):
        """Check if proposed move is valid."""
        if self.first_move and abs(start[1] - to[1]) == 2 and start[0] - to[0] == 0:
            return self.can_castle(board, start, to, to[1] - start[1] > 0)

        if abs(start[0] - to[0]) == 1 or start[0] - to[0] == 0:
            if start[1] - to[1] == 0 or abs(start[1] - to[1]) == 1:
                self.first_move = False
                return True

        return False


class GhostPawn(Piece):
    """Ghost pawn for en passant."""

    def __init__(self, color):
        """Init piece name and color."""
        super().__init__(color)
        self.name = "GP"

    def is_valid_move(self, board, start, to):
        """Check if proposed move is valid."""
        return False


class Pawn(Piece):
    """Pawn piece."""

    def __init__(self, color):
        """Init piece name, color and first move."""
        super().__init__(color)
        self.name = "P"
        self.first_move = True

    def is_valid_move(self, board, start, to): #pylint: disable=too-many-return-statements
        """Check if proposed move is valid."""
        if self.color:
            if start[0] == to[0] + 1 and (start[1] == to[1] + 1 or start[1] == to[1] - 1):
                if board.board[to[0]][to[1]] is not None:
                    self.first_move = False
                    return True
                return False

            if start[1] == to[1]:
                if (start[0] - to[0] == 2 and self.first_move) or (start[0] - to[0] == 1):
                    for i in range(start[0] - 1, to[0] - 1, -1):
                        if board.board[i][start[1]] is not None:
                            return False
                    if start[0] - to[0] == 2:
                        board.board[start[0] - 1][start[1]
                                                  ] = GhostPawn(self.color)
                        board.white_ghost_piece = (start[0] - 1, start[1])
                    self.first_move = False
                    return True
                return False
            return False

        if start[0] == to[0] - 1 and (start[1] == to[1] - 1 or start[1] == to[1] + 1):
            if board.board[to[0]][to[1]] is not None:
                self.first_move = False
                return True
            return False
        if start[1] == to[1]:
            if (to[0] - start[0] == 2 and self.first_move) or (to[0] - start[0] == 1):
                for i in range(start[0] + 1, to[0] + 1):
                    if board.board[i][start[1]] is not None:
                        return False
                # insert a GhostPawn
                if to[0] - start[0] == 2:
                    board.board[start[0] + 1][start[1]
                                              ] = GhostPawn(self.color)
                    board.black_ghost_piece = (start[0] + 1, start[1])
                self.first_move = False
                return True
            return False
        return False
