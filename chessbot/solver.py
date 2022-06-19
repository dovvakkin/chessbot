from stockfish import Stockfish

default_path = 'chessbot\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe'
default_parameters = {
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 4,
    "Ponder": "false",
    "Hash": 64,
    "MultiPV": 1,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "true",
    "UCI_Elo": 1350
}


class Solver():

    def __init__(self, path=None, depth=15, params=None):

        if path is None:
            path = default_path
        if params is None:
            params = default_parameters

        self.solver = Stockfish(path=path, depth=depth, parameters=params)

    def make_step(self, fen):
        """
        Predicts best possible move for opposing team (PvE)
        """

        if not self.solver.is_fen_valid(fen):
            raise ValueError("Incorrect FEN notation")

        self.solver.set_fen_position(fen)
        return self.solver.get_best_move()
