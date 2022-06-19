"""A module to launch Stockfish engine wrapper."""

from stockfish import Stockfish

DEFAULT_PATH = 'chessbot\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe'
DEFAULT_PARAMS = {
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
    """
    A class to represent a wrapper of a stockfish solver.

    ...
    Attributes:
    -----------
    path : str
        path to stokfish execution
    solver : bool
        True if piece is white
    """

    def __init__(self, path=None, depth=15, params=None):
        """Initialise Stockfish wrapper."""
        if path is None:
            path = DEFAULT_PATH
        if params is None:
            params = DEFAULT_PARAMS

        self.solver = Stockfish(path=path, depth=depth, parameters=params)

    def make_step(self, fen):
        """Predict best possible move for black team."""
        if not self.solver.is_fen_valid(fen):
            return None

        self.solver.set_fen_position(fen)
        return self.solver.get_best_move()

    def check_fen(self, fen):
        """Check if there is a possible move from current state."""
        return self.solver.is_fen_valid(fen)
