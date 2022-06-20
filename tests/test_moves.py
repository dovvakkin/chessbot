"""Tests for pieces' moves correctness."""
from chessbot import chess
from chessbot.chess import translate


def test_rook_move():
    """Test rook's movements."""
    chess_game = chess.Chess(notation='rr4k1/8/8/8/8/8/8/R5K1 w KQkq - 0 1')

    # correct vertical move
    move_start = translate("a1")
    move_to = translate("a8")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1

    # incorrect (diagonal) move
    move_start = translate("b8")
    move_to = translate("c1")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct horisontal move
    move_start = translate("b8")
    move_to = translate("d8")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_knight_move():
    """Test knight's movements."""
    chess_game = chess.Chess(notation='6k1/8/8/8/8/8/8/N5K1 w KQkq - 0 1')

    # incorrect move
    move_start = translate("a1")
    move_to = translate("c3")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct move
    move_start = translate("a1")
    move_to = translate("c2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_bishop_move():
    """Test bishop's movements."""
    chess_game = chess.Chess(notation='6k1/8/8/8/8/8/8/B5K1 w KQkq - 0 1')

    # incorrect move
    move_start = translate("a1")
    move_to = translate("c4")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct move
    move_start = translate("a1")
    move_to = translate("c3")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_queen_move():
    """Test queen's movements."""
    chess_game = chess.Chess(notation='q5k1/8/8/8/8/8/8/Q5K1 w KQkq - 0 1')

    # incorrect move
    move_start = translate("a1")
    move_to = translate("c2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct diagonal move
    move_start = translate("a1")
    move_to = translate("c3")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1

    # correct linear move
    move_start = translate("a8")
    move_to = translate("a1")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_king_move():
    """Test king's movements."""
    chess_game = chess.Chess(notation='6k1/8/8/8/8/8/8/6K1 w KQkq - 0 1')

    # incorrect move
    move_start = translate("g1")
    move_to = translate("c3")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct move
    move_start = translate("g1")
    move_to = translate("g2")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1


def test_pawn_move():
    """Test pawn's movements."""
    chess_game = chess.Chess(notation='6k1/1p6/2P5/1p6/8/8/8/6K1 w KQkq - 0 1')

    # correct takeover
    move_start = translate("c6")
    move_to = translate("b7")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1

    # incorrect move
    move_start = translate("b5")
    move_to = translate("b6")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 0

    # correct move
    move_start = translate("b5")
    move_to = translate("b4")
    check_move = chess_game.move(move_start, move_to)
    assert check_move == 1
