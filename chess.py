import board
import piece

class Chess():

    def __init__(self):
        self.board = board.Board()

        self.turn = True

        self.white_ghost_piece = None
        self.black_ghost_piece = None

    def promotion(self, pos, promote):
        pawn = None
        while pawn == None:
            if promote in ['Q', 'R', 'N', 'B']:
                if promote == 'Q':
                    pawn = piece.Queen(True)
                elif promote == 'R':
                    pawn = piece.Rook(True)
                elif promote == 'N':
                    pawn = piece.Knight(True)
                elif promote == 'B':
                    pawn = piece.Bishop(True)
        self.board.board[pos[0]][pos[1]] = pawn 

    def move(self, start, to):
        if self.board.board[start[0]][start[1]] == None:
            return

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            return

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            return

        if target_piece.is_valid_move(self.board, start, to):
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                
                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return
                
            if self.board.board[to[0]][to[1]]:
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[
                            self.black_ghost_piece[0] + 1
                        ][
                            self.black_ghost_piece[1]
                        ] = None
                        self.black_ghost_piece = None
                    else:
                        self.board.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None

            if self.turn and self.black_ghost_piece:
                self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None

            self.turn = not self.turn


def translate(s):
    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            return None
        if col < 'a' or col > 'h':
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        return None