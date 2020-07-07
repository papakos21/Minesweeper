import pytest
from MinesweeperBoard import MinesweeperBoard
from Tile import Tile


def test_get_board_size_default():
    game = MinesweeperBoard()
    assert game.row_size == 8 and game.column_size == 10


def test_get_board_size_medium():
    game = MinesweeperBoard('medium')
    assert game.row_size == 14 and game.column_size == 20


def test_get_number_of_bombs_easy():
    game = MinesweeperBoard('easy')
    assert game.number_of_bombs == 10


def test_build_board():
    game = MinesweeperBoard('easy')
    assert len(game.board) == game.row_size
    assert len(game.board[0]) == game.column_size

def test_get_position_of_bombs_hard():
    game = MinesweeperBoard('hard')
    assert len(game.position_of_bombs) == 99

def test_assign_bombs_to_tiles():
    game = MinesweeperBoard('easy')
    counter = 0
    for row in game.board:
        for column in row:
            if column.bomb:
                counter += 1
    assert counter == 10

# def test_numbers_to_tiles():
#     game = MinesweeperModel('easy')
#     t = Tile()
#     if game.board[0][0].bomb is True and game.board.board[0][1].bomb is True:
#         assert t[5][5].number_of_neighbour_bombs == 2
def test_numbers_to_tiles():
    game = MinesweeperBoard()
    game.board[0][0].bomb is True
    game.board[0][1].bomb is True
    assert game.board[1][0].number_of_neighbour_bombs == 2