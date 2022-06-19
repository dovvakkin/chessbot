import piece
from generating_board import generate_new_board, generate_random_board

def convert_array_to_fen(arr):
    
    """
    converts 8x8 array (or list of lists) to positional part of FEN notation
    """
    
    blueprint = [] # using list because joining them such way is less memory-intensive
    
    for line in arr:
        
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
    
class Board():

    def __init__(self, random_mode = False):

        if random_mode:
            self.board_image, self.board_array = generate_random_board()
        else:
            self.board_image, self.board_array = generate_new_board()

        self.board_fen = convert_array_to_fen(self.board_array)
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
                            self.board[i][j] = piece.Rook(flag, king_side = True)
                        else:
                            self.board[i][j] = piece.Rook(flag, king_side = False)
                    elif cell[1] == 'N':
                        self.board[i][j] = piece.Knight(flag)
                    elif cell[1] == 'B':
                        self.board[i][j] = piece.Bishop(flag)
                    elif cell[1] == 'K':
                        self.board[i][j] = piece.King(flag)
                    elif cell[1] == 'Q':
                        self.board[i][j] = piece.Queen(flag)

                    else:
                        raise ImportWarning("Incorrect symbol enccountered in Board Array")
    
    def print_board(self):
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