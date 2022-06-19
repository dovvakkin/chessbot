"""Test for board generation and FEN -> array conversion."""
import numpy as np
from .board import Board, convert_fen_to_array


def test_fen_to_array():
    """Test if FEN -> array is valid."""
    fen = 'r1b1k3/ppppp3/8/2b5/8/4N3/PQPPPPPP/4K2R w KQkq - 0 1'
    arr = np.array([
       ['bR', '', 'bB', '', 'bK', '', '', ''],
       ['bP', 'bP', 'bP', 'bP', 'bP', '', '', ''],
       ['', '', '', '', '', '', '', ''],
       ['', '', 'bB', '', '', '', '', ''],
       ['', '', '', '', '', '', '', ''],
       ['', '', '', '', 'wN', '', '', ''],
       ['wP', 'wQ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
       ['', '', '', '', 'wK', '', '', 'wR']
    ])
    conversion = convert_fen_to_array(fen)
    assert np.all(arr == conversion)


def test_board_generation():
    """Test if array -> FEN (partial) is valid."""
    fen = 'r1b1k3/ppppp3/8/2b3q1/R6r/4N3/PQPPPPPP/4K2R w KQkq - 0 1'
    arr = np.array([
       ['bR', '', 'bB', '', 'bK', '', '', ''],
       ['bP', 'bP', 'bP', 'bP', 'bP', '', '', ''],
       ['', '', '', '', '', '', '', ''],
       ['', '', 'bB', '', '', '', 'bQ', ''],
       ['wR', '', '', '', '', '', '', 'bR'],
       ['', '', '', '', 'wN', '', '', ''],
       ['wP', 'wQ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
       ['', '', '', '', 'wK', '', '', 'wR']
    ])
    brd = Board(random_mode = False, notation = fen)
    assert np.all(arr == brd.board_array)
    