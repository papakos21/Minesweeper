import pytest
from MinesweeperModel import MinesweeperModel


def test_get_board_size_default():
    game = MinesweeperModel()
    assert game.row_index == 8 and game.column_index == 10


def test_get_board_size_medium():
    game = MinesweeperModel('medium')
    assert game.row_index == 14 and game.column_index == 20


def test_get_number_of_bombs_easy():
    game = MinesweeperModel('easy')
    assert game.number_of_bombs == 10


def test_build_board():
    game = MinesweeperModel('easy')
    assert len(game.board) == game.row_index
    assert len(game.board[0]) == game.column_index
