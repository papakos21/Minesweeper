import pytest
from MinesweeperModel import MinesweeperModel


def test_get_board_size_default():
    game = MinesweeperModel()
    assert game.row_size == 8 and game.column_size == 10


def test_get_board_size_medium():
    game = MinesweeperModel('medium')
    assert game.row_size == 14 and game.column_size == 20


def test_get_number_of_bombs_easy():
    game = MinesweeperModel('easy')
    assert game.number_of_bombs == 10


def test_build_board():
    game = MinesweeperModel('easy')
    assert len(game.board) == game.row_size
    assert len(game.board[0]) == game.column_size

def test_get_position_of_bombs_hard():
    game = MinesweeperModel('hard')
    assert len(game.position_of_bombs) == 99
