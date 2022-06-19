import board
import piece

class Chess():

    def __init__(self, random_mode = False):
        self.board = board.Board()

        self.turn = True
        self.turn_number = 1
        self.halfstep_number = 0

        self.white_ghost_piece = None
        self.black_ghost_piece = None

        self.random_mode = random_mode
        if random_mode:
            self.castling = '-'
        
        else:
            self.castling = "KQkq"

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

    def has_piece_under(self, start):
        print(self.board)
        print(self.board.board)
        print(start)
        if self.board.board[start[0]][start[1]] == None:
            return False
        if self.board.board[start[0]][start[1]].name == "GP":
            return False
        return True

    def move(self, start, to):
        if self.board.board[start[0]][start[1]] == None:
            return False

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            return False

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            return False

        if target_piece.is_valid_move(self.board, start, to):

            # for FEN calculation
            if not self.turn:
                self.turn_number += 1
            if self.castling != "-":
                if target_piece.name == 'R':
                    if target_piece.king_side:
                        if self.turn:
                            self.castling.replace("K", "")
                        else:
                            self.castling.replace("k", "")
                    else:
                        if self.turn:
                            self.castling.replace("Q", "")
                        else:
                            self.castling.replace("q", "")
                if target_piece.name == 'K':
                    if self.turn:
                        self.castling.replace("K", "")
                        self.castling.replace("Q", "")
                    else:
                        self.castling.replace("k", "")
                        self.castling.replace("q", "")
                if self.castling == "":
                    self.castling == "-"

            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                
                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return True
                
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

            return True
        else:
            return False

    def _reverse_translate(pos):

        dictionary = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e', 5 : 'f', 6 : 'g', 7 : 'h'}
        
        return str(8 - pos[0]) + dictionary[pos[1]]

    def get_fen(self):

        """
        Generates full FEN notation. Positions obtained from inner representation.
        
        side: Boolean
        True = White, False = Black

        castling: String
        Current castling possibilities

        ghost: String
        Location of ghost pawn if one exists

        halfmove: Int
        Tie Counter (number of half-moves passed from last figure taken or pawn moved)

        move: Int
        Move counter
        """

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
        if not self.white_ghost_piece is None:
            fen_container.append(self._reverse_translate(self.white_ghost_piece))
        elif not self.black_ghost_piece is None:
            fen_container.append(self._reverse_translate(self.black_ghost_piece))
        else:
            fen_container.append('-')

        # 5 - halfturns
        fen_container.append(self.halfstep_number)

        # 6 - turns 
        fen_container.append(self.turn_number)

        return " ".join(fen_container)
        
def translate(s):
    try:
        row = int(s[1])
        col = s[0]
        if row < 1 or row > 8:
            return None
        if col < 'a' or col > 'h':
            return None
        dictionary = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dictionary[col])
    except:
        return None
