def check_knight(color, board, pos):
    piece = board.board[pos[0]][pos[1]]
    if piece != None and piece.color != color and piece.name == 'N':
        return False
    return True


def check_diag_castle(color, board, start, to):
    if abs(start[0] - to[0]) != abs(start[1] - to[1]): 
        return False

    x_pos = 1 if to[0] - start[0] > 0 else -1
    y_pos = 1 if to[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos

    exists_piece = board.board[i][j] != None
    if exists_piece and (board.board[i][j].name == 'P' or board.board[i][j].name == 'K') and \
            board.board[i][j].color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):

        if exists_piece and board.board[i][j].color != color:
            if board.board[i][j].name in ['B', 'Q']:
                return False
            else:
                return True
        if exists_piece and board.board[i][j].color == color:
            return True
        i += x_pos
        j += y_pos

        if min(i, j) < 0 or max(i, j) > 7:
            continue

        exists_piece = board.board[i][j] != None

    return True


def check_diag(board, start, to):
    if abs(start[0] - to[0]) != abs(start[1] - to[1]):
        return False

    x_pos = 1 if to[0] - start[0] > 0 else -1
    y_pos = 1 if to[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos
    while (i < to[0] if x_pos == 1 else i > to[0]):
        if board.board[i][j] != None:
            return False
        i += x_pos
        j += y_pos
    return True


def check_updown_castle(color, board, start, to):

    x_pos = 1 if to[0] - start[0] > 0 else -1
    i = start[0] + x_pos

    front_piece = board.board[i][start[1]]
    if front_piece != None and front_piece.name == 'K' and front_piece.color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):
        if board.board[i][start[1]] != None and board.board[i][start[1]].color != color:
            if board.board[i][start[1]].name in ['R', 'Q']:
                return False
            else:
                return True
        if board.board[i][start[1]] != None and board.board[i][start[1]].color == color:
            return True

        i += x_pos

    return True


def check_updown(board, start, to):
    if start[0] == to[0]:
        smaller_y = start[1] if start[1] < to[1] else to[1]
        bigger_y = start[1] if start[1] > to[1] else to[1]

        for i in range(smaller_y + 1, bigger_y):
            if board.board[start[0]][i] != None:
                return False
        return True
    else:
        smaller_x = start[0] if start[0] < to[0] else to[0]
        bigger_x = start[0] if start[0] > to[0] else to[0]

        for i in range(smaller_x + 1, bigger_x):
            if board.board[i][start[1]] != None:
                return False
        return True


class Piece():
    def __init__(self, color):
        self.name = ""
        self.color = color

    def is_valid_move(self, board, start, to):
        return False

    def is_white(self):
        return self.color


class Rook(Piece):
    def __init__(self, color, first_move=True, king_side=True):
        super().__init__(color)
        self.name = "R"
        self.first_move = first_move
        self.king_side = king_side

    def is_valid_move(self, board, start, to):
        if start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        return False


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "N"

    def is_valid_move(self, board, start, to):
        if abs(start[0] - to[0]) == 2 and abs(start[1] - to[1]) == 1:
            return True
        if abs(start[0] - to[0]) == 1 and abs(start[1] - to[1]) == 2:
            return True
        return False


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "B"

    def is_valid_move(self, board, start, to):
        return check_diag(board, start, to)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "Q"

    def is_valid_move(self, board, start, to):
        if abs(start[0] - to[0]) == abs(start[1] - to[1]):
            return check_diag(board, start, to)

        elif start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        return False


class King(Piece):
    def __init__(self, color, first_move=True):
        super().__init__(color)
        self.name = "K"
        self.first_move = first_move

    def can_castle(self, board, start, to, right):
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
        if self.first_move and abs(start[1] - to[1]) == 2 and start[0] - to[0] == 0:
            return self.can_castle(board, start, to, to[1] - start[1] > 0)

        if abs(start[0] - to[0]) == 1 or start[0] - to[0] == 0:
            if start[1] - to[1] == 0 or abs(start[1] - to[1]) == 1:
                self.first_move = False
                return True

        return False


class GhostPawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "GP"

    def is_valid_move(self, board, start, to):
        return False


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "P"
        self.first_move = True

    def is_valid_move(self, board, start, to):
        if self.color:
            if start[0] == to[0] + 1 and (start[1] == to[1] + 1 or start[1] == to[1] - 1):
                if board.board[to[0]][to[1]] != None:
                    self.first_move = False
                    return True
                return False

            if start[1] == to[1]:
                if (start[0] - to[0] == 2 and self.first_move) or (start[0] - to[0] == 1):
                    for i in range(start[0] - 1, to[0] - 1, -1):
                        if board.board[i][start[1]] != None:
                            return False
                    if start[0] - to[0] == 2:
                        board.board[start[0] - 1][start[1]
                                                  ] = GhostPawn(self.color)
                        board.white_ghost_piece = (start[0] - 1, start[1])
                    self.first_move = False
                    return True
                return False
            return False

        else:
            if start[0] == to[0] - 1 and (start[1] == to[1] - 1 or start[1] == to[1] + 1):
                if board.board[to[0]][to[1]] != None:
                    self.first_move = False
                    return True
                return False
            if start[1] == to[1]:
                if (to[0] - start[0] == 2 and self.first_move) or (to[0] - start[0] == 1):
                    for i in range(start[0] + 1, to[0] + 1):
                        if board.board[i][start[1]] != None:
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
