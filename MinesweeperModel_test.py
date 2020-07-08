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


def test_numbers_to_tiles():
    test_board = [[Tile(), Tile()], [Tile(), Tile()]]
    test_bomb_coordinates = [(0, 0), (0, 1)]
    test_board[0][0].bomb = True
    test_board[0][1].bomb = True
    game = MinesweeperBoard(test_board=test_board, test_bombs_coordinates=test_bomb_coordinates)

    assert game.board[1][0].number_of_neighbour_bombs == 2
    assert game.board[1][1].number_of_neighbour_bombs == 2


def test_game_over_is_True_and_human_wins():
    # to do
    test_board = [[Tile(), Tile()], [Tile(), Tile()]]
    test_bomb_coordinates = [(0, 0)]
    test_board[0][0].bomb = True
    test_board[0][1].is_revealed = True
    test_board[1][1].is_revealed = True
    test_board[1][0].is_revealed = True
    game = MinesweeperBoard(test_board=test_board, test_bombs_coordinates=test_bomb_coordinates)

    assert game.game_over() is True
    assert game.human_wins is True


def test_game_over_is_True_and_human_loses():
    # to do
    test_board = [[Tile(), Tile()], [Tile(), Tile()]]
    test_bomb_coordinates = [(0, 0)]
    test_board[0][0].bomb = True
    test_board[0][0].is_revealed = False
    test_board[1][1].is_revealed = True
    test_board[1][0].is_revealed = True
    test_board[0][1].is_revealed = False
    game = MinesweeperBoard(test_board=test_board, test_bombs_coordinates=test_bomb_coordinates)

    assert game.game_over() is False
    game.players_choice_of_tile_and_action((0, 0), 'reveal')
    assert game.game_over() is True
    assert game.human_wins is False


def test_reveal_neighbours():
    test_board = [[Tile(), Tile(), Tile()], [Tile(), Tile(), Tile()], [Tile(), Tile(), Tile()]]
    test_bomb_coordinates = [(0, 0)]
    test_board[0][0].bomb = True
    game = MinesweeperBoard(test_board=test_board, test_bombs_coordinates=test_bomb_coordinates)
    game.players_choice_of_tile_and_action((2, 2), 'reveal')
    assert game.board[0][1].is_revealed == True
    assert game.board[0][2].is_revealed == True
    assert game.board[1][0].is_revealed == True
    assert game.board[1][1].is_revealed == True
    assert game.board[1][2].is_revealed == True
    assert game.board[2][0].is_revealed == True
    assert game.board[2][1].is_revealed == True
    assert game.board[2][2].is_revealed == True
    assert game.game_over() is True
