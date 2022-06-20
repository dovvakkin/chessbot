"""Tests for chessbot api."""
from chessbot import chess
from chessbot.chess import translate


def test_valid_move():
    """Test is basic move valid."""
    chess_game = chess.Chess(notation='4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1')
    move_start = translate("e1")
    move_to = translate("e2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_invalid_move():
    """Test invalidity of incorrect move of the pawn to the side."""
    chess_game = chess.Chess(notation='4k3/8/8/8/8/8/4P3/4K3 w KQkq - 0 1')
    move_start = translate("e2")
    move_to = translate("f2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0


def test_first_pawn_move():
    """Test ability of the pawn to move up 2 squares and only once."""
    chess_game = chess.Chess(notation='4k3/8/8/8/8/8/4P3/4K3 w KQkq - 0 1')
    # white
    move_start = translate("e2")
    move_to = translate("e4")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
    # black
    move_start = translate("e8")
    move_to = translate("f8")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
    # white invalid (only at start)
    move_start = translate("e4")
    move_to = translate("e6")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0


def test_capture():
    """Test capture of pawn."""
    chess_game = chess.Chess(notation='4k3/8/8/8/5p2/4P3/8/4K3 w KQkq - 0 1')
    # white capture
    move_start = translate("e3")
    move_to = translate("f4")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_en_passant_capture():
    """Test en passant capture of pawn."""
    chess_game = chess.Chess(notation='4k3/8/8/8/5p2/8/4P3/4K3 w KQkq - 0 1')
    # white
    move_start = translate("e2")
    move_to = translate("e4")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
    print(chess_game.board.board)
    print(chess_game.board.white_ghost_piece)
    # black en passant
    move_start = translate("f4")
    move_to = translate("e3")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_castle_queen_side():
    """Test ability to castle queen side."""
    chess_game = chess.Chess(notation='r3k3/ppppp3/8/8/8/8/8/4K3 w KQkq - 0 1')
    # white
    move_start = translate("e1")
    move_to = translate("e2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
    # black castle
    move_start = translate("e8")
    move_to = translate("c8")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_castle_king_side():
    """Test ability to castle king side."""
    chess_game = chess.Chess(notation='r3k2r/pppppppp/8/8/8/8/8/4K3 w KQkq - 0 1')
    # white
    move_start = translate("e1")
    move_to = translate("e2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
    # black castle
    move_start = translate("e8")
    move_to = translate("g8")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
