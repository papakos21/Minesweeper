"""module containing Minesweeper model"""
import requests
import time
import random
import json
import os.path
import uuid
import pickle
import sqlite3
from random import Random
from Tile import Tile
from DifficultyEnum import Difficulty
from typing import List, Tuple

#SERVER_URL = 'http://localhost:8000'
SERVER_URL = 'http://ec2-3-15-190-19.us-east-2.compute.amazonaws.com:8000'

class MinesweeperInterface:
    """"""

    def build_board(self, row_index: int, column_index: int) -> List[List[Tile]]:
        """build board"""
        board = []
        for _ in range(row_index):
            row = []
            for _ in range(column_index):
                row.append(Tile())
            board.append(row)
        return board

    def get_column_size(self):
        raise NotImplementedError('Not Implemented')

    def human_won(self):
        raise NotImplementedError('Not Implemented')

    def get_tile(self, row_index, column_index):
        raise NotImplementedError('Not Implemented')

    def get_row_size(self):
        raise NotImplementedError('Not Implemented')

    def game_over(self) -> bool:
        raise NotImplementedError('Not Implemented')

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str) -> None:
        raise NotImplementedError('Not Implemented')


class CrazyMinesweeperBoard(MinesweeperInterface):
    """MinesweeperBoard contacts the server."""

    def get_column_size(self):
        return 10

    def human_won(self):
        return False

    def get_tile(self, row_index, column_index):
        t = Tile()
        r = Random()
        t.number_of_neighbour_bombs = r.randint(0, 8)
        t.bomb = r.randint(0, 10) > 5
        t.is_revealed = r.randint(0, 10) > 5
        t.flag = r.randint(0, 10) > 5
        return t

    def get_row_size(self):
        return 10

    def game_over(self) -> bool:
        return False

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str) -> None:
        pass


class RemoteMinesweeperBoard(MinesweeperInterface):
    """MinesweeperBoard contacts the server."""

    def __init__(self, difficulty: Difficulty = Difficulty.EASY, user_id = 'unknown'):
        self.cache = {}
        self.column_size, self.row_size, self.game_id = self.start_new_game(difficulty)
        self.board = self.build_board(self.row_size, self.column_size)
        self._game_over = False
        self.user_id = user_id

    def start_new_game(self, difficulty: Difficulty):
        headers= {"User_Id": self.user_id}
        response = requests.request("GET",SERVER_URL + '/new_game/' + str(difficulty), headers=headers)
        new_game_info = json.loads(response.text)
        return new_game_info['column_size'], new_game_info['row_size'], new_game_info['game_id']

    def get_column_size(self):

        return self.column_size

    def human_won(self):
        if 'human_won' in self.cache:
            return self.cache['human_won']
        response = requests.get(SERVER_URL + '/human_won/' + self.game_id)
        self.cache['human_won'] = (response.text == 'True')
        return self.cache["human_won"]

    def get_tile(self, row_index, column_index):
        # key = (row_index, column_index)
        # if key in self.cache:
        #     return self.cache[key]
        # response = requests.get(SERVER_URL + '/get_tile/' + str(row_index) + '/' + str(column_index))
        # tile_data = json.loads(response.text)
        # tile = Tile()
        # tile.flag = tile_data['flag']
        # tile.bomb = tile_data['bomb']
        # tile.is_revealed = tile_data['is_revealed']
        # tile.number_of_neighbour_bombs = tile_data['number_of_neighbour_bombs']
        # tile.question_mark = tile_data['question_mark']
        # self.cache[key] = tile
        # return tile
        return self.board[row_index][column_index]

    def get_row_size(self):

        return self.row_size

    def game_over(self) -> bool:

        return self._game_over

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str) -> None:
        data = json.dumps(
            {'row_index': choice[0], 'column_index': choice[1], 'action': action, 'game_id': self.game_id})
        response = requests.post(SERVER_URL + '/play', data)
        foo = 0
        game_over_and_changed_tiles = json.loads(response.text)
        self._game_over = game_over_and_changed_tiles['game_over']
        for changed_tile in game_over_and_changed_tiles['changed_tiles']:
            current_tile = self.board[changed_tile['row_index']][changed_tile['column_index']]
            remote_tile = changed_tile['tile']
            current_tile.flag = remote_tile['flag']
            current_tile.bomb = remote_tile['bomb']
            current_tile.is_revealed = remote_tile['is_revealed']
            current_tile.number_of_neighbour_bombs = remote_tile['number_of_neighbour_bombs']


class MinesweeperBoard(MinesweeperInterface):
    """the MinesweeperBoard"""

    def __init__(self, difficulty: Difficulty = Difficulty.EASY,
                 test_bombs_coordinates: List[Tuple[int, int]] = None,
                 test_board: List[List[Tile]] = None,
                 load_from_file: bool = False,
                 filename: str = './game.txt'):
        self.difficulty = difficulty
        self.filename = filename
        if os.path.isfile(filename) and load_from_file:
            self.load_game()
            self.has_not_started = False
        else:
            self.has_not_started = True
            self.difficulty = difficulty
            coordinates = self.get_board_size(difficulty) if test_board is None else \
                (len(test_board), len(test_board[0]))
            self.row_size = coordinates[0]
            self.column_size = coordinates[1]
            self.number_of_bombs = self.get_number_of_bombs(difficulty) \
                if test_bombs_coordinates is None else len(test_bombs_coordinates)
            # self.x,self.y=self.get_board_size(difficulty)
            self.board = self.build_board(self.row_size,
                                          self.column_size) if test_board is None else test_board
            self.position_of_bombs = self.get_position_of_bombs(self.number_of_bombs, self.row_size,
                                                                self.column_size) if test_board is \
                                                                                     None else None
            self.coordinates_of_bombs = self.get_coordinate_position_of_bombs_2(
                self.position_of_bombs, self.row_size,
                self.column_size) if not test_bombs_coordinates else test_bombs_coordinates
            self.assign_bombs_to_tiles()
            self.assign_numbers_to_tiles()
        self.choice = None
        self.human_wins = False
        self.changed_tiles_accumulator = []

    def get_board_size(self, difficulty: Difficulty) -> Tuple[int, int]:
        """determine the board size"""
        if difficulty not in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
            raise ValueError("easy or medium or hard ")
        if difficulty == Difficulty.EASY:
            row_index = 8
            column_index = 10
        elif difficulty == Difficulty.MEDIUM:
            row_index = 14
            column_index = 20
        elif difficulty == Difficulty.HARD:
            row_index = 20
            column_index = 24
        coordinates = (row_index, column_index)
        return coordinates

    def get_number_of_bombs(self, difficulty: Difficulty) -> int:
        """determine the number of bombs"""
        if difficulty == Difficulty.EASY:
            number_of_bombs = 10
        elif difficulty == Difficulty.MEDIUM:
            number_of_bombs = 40
        elif difficulty == Difficulty.HARD:
            number_of_bombs = 99
        return number_of_bombs

    def get_position_of_bombs(self, number_of_bombs: int,
                              row_index: int,
                              column_index: int) -> List[int]:
        """get position of bombs"""
        number_of_tiles = row_index * column_index
        position_of_bombs = (random.sample(range(0, number_of_tiles), number_of_bombs))
        return position_of_bombs

    def get_coordinate_position_of_bombs_2(self, position_of_bombs: List[int],
                                           row_size: int,
                                           column_size: int) -> List[Tuple[int, int]]:
        """get the coordinates of the position of bombs"""
        count = 0
        coordinates_to_return = []
        for row in range(row_size):
            for column in range(column_size):
                if count in position_of_bombs:
                    coordinates_to_return.append((row, column))
                count += 1
        return coordinates_to_return

    def assign_bombs_to_tiles(self) -> None:
        """assign bombs to tiles"""
        for (row, column) in self.coordinates_of_bombs:
            self.board[row][column].bomb = True

    def assign_numbers_to_tiles(self) -> None:
        """assign numbers to tiles"""
        for (row, column) in self.coordinates_of_bombs:
            neighbours = self.find_neighbours(row, column)
            for neigbour_row, neighbour_column in neighbours:

                if self.board[neigbour_row][neighbour_column].bomb is False:
                    self.board[neigbour_row][neighbour_column].number_of_neighbour_bombs += 1

    def find_neighbours(self, row: int, column: int) -> List[Tuple[int, int]]:
        """find neigbours"""
        neighbours_to_return = []
        for delta_row in [-1, 0, 1]:
            for delta_column in [-1, 0, 1]:
                if not (delta_row == 0 and delta_column == 0):
                    neigbour_row = delta_row + row
                    neighbour_column = delta_column + column
                    if 0 <= neigbour_row < self.row_size and \
                            0 <= neighbour_column < self.column_size:
                        neighbours_to_return.append((neigbour_row, neighbour_column))
        return neighbours_to_return

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str) -> None:
        """players choice of tile and action """

        self.has_not_started = False
        current_board_tile = self.board[choice[0]][choice[1]]
        self.choice = choice
        if action == 'reveal':
            current_board_tile.is_revealed = True
            if not current_board_tile.bomb:
                self.reveal_neighbours_if_not_bomb_or_number()
            else:
                self.reveal_all_and_add_to_changed_tiles()

        if action == 'flag':
            current_board_tile.flag = not current_board_tile.flag
        if action == 'question':
            current_board_tile.question_mark = True
        self.changed_tiles_accumulator.append(
            {'row_index': choice[0], 'column_index': choice[1], 'tile': current_board_tile.__dict__})
        self.save_game()
        # player chooses a tile and then chooses if wants to reveal it, flag it, or question mark it

    def reveal_all_and_add_to_changed_tiles(self):
        for row_index in range(self.row_size):
            for column_index in range(self.column_size):
                current_board_tile = self.board[row_index][column_index]
                if not current_board_tile.is_revealed:
                    current_board_tile.is_revealed= True
                    self.changed_tiles_accumulator.append(
                        {'row_index': row_index, 'column_index': column_index, 'tile': current_board_tile.__dict__})

    def reveal_neighbours_if_not_bomb_or_number(self) -> None:
        """reveal neighbours if not bombs or numbers"""
        if self.board[self.choice[0]][self.choice[1]].number_of_neighbour_bombs == 0:
            for coordinate in self.find_neighbours(self.choice[0], self.choice[1]):
                if self.board[coordinate[0]][coordinate[1]].is_revealed == False:
                    self.players_choice_of_tile_and_action(coordinate, 'reveal')

    def game_over(self) -> bool:
        """game over"""
        if self.choice in self.coordinates_of_bombs:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
            self.reveal_all()
            return True
        number_of_tiles_without_bomb = self.row_size * self.column_size - self.number_of_bombs
        number_of_revealed_tiles = self.count_of_revealed_tiles()
        if number_of_revealed_tiles == number_of_tiles_without_bomb:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
            self.reveal_all()
            self.human_wins = True

            return True

        return False

    def count_of_revealed_tiles(self) -> int:
        """count of revealed tiles"""
        count = 0
        for row in range(self.row_size):
            for column in range(self.column_size):
                if self.board[row][column].is_revealed:
                    count += 1
        return count

    def save_game(self):
        """save game"""
        file_handler = open(self.filename, "wb")
        pickle.dump(self, file_handler)
        file_handler.close()

    def load_game(self):
        """load game"""
        file_handler = open(self.filename, "rb")
        loaded_game = pickle.load(file_handler)
        self.board = loaded_game.board
        self.human_wins = loaded_game.human_wins
        self.filename = loaded_game.filename
        self.choice = loaded_game.choice
        self.row_size = loaded_game.row_size
        self.difficulty = loaded_game.difficulty
        self.has_not_started = loaded_game.has_not_started
        self.column_size = loaded_game.column_size
        self.number_of_bombs = loaded_game.number_of_bombs
        self.coordinates_of_bombs = loaded_game.coordinates_of_bombs
        self.position_of_bombs = loaded_game.position_of_bombs

    def reveal_all(self):
        """reveal all"""
        for row in range(self.row_size):
            for column in range(self.column_size):
                self.board[row][column].is_revealed = True

    def human_won(self):
        return self.human_wins

    def get_tile(self, row_index, column_index):
        return self.board[row_index][column_index]

    def get_row_size(self):
        return self.row_size

    def get_column_size(self):
        return self.column_size

    def get_changed_tiles(self):
        return self.changed_tiles_accumulator

    def reset_changed_tiles(self):
        self.changed_tiles_accumulator = []


class MinesweeperBoardDatabaseTracker(MinesweeperInterface):
    def __init__(self, actual_minesweeper: MinesweeperBoard, game_id: str= 'unknown', user_id: str = 'unknown'):
        self.actual_minesweeper = actual_minesweeper
        if game_id == "unknown":
            self.game_id = str(uuid.uuid4())
        else:
            self.game_id = game_id
        self.user_id = user_id
        self.number_of_moves = 0
        self.current_time = time.time()

    def build_board(self, row_index: int, column_index: int) -> List[List[Tile]]:
        return self.actual_minesweeper.build_board(row_index, column_index)

    def get_column_size(self):
        return self.actual_minesweeper.get_column_size()

    def human_won(self):
        return self.actual_minesweeper.human_won()

    def get_tile(self, row_index, column_index):
        return self.actual_minesweeper.get_tile(row_index, column_index)

    def get_row_size(self):
        return self.actual_minesweeper.get_row_size()

    def game_over(self) -> bool:
        is_game_over = self.actual_minesweeper.game_over()
        if is_game_over:

            conn = sqlite3.connect('minesweeper.db')
            c = conn.cursor()
            c.execute('''INSERT INTO games VALUES 
            ('{}','{}','{}','{}',{},{},'2020/09/14','{}')'''.format(self.game_id,
                                                                         self.user_id,
                                                                         self.actual_minesweeper.difficulty,
                                                                         self.actual_minesweeper.human_won(),
                                                                         self.number_of_moves,
                                                                         time.time() - self.current_time,
                                                                         " "
                                                                         ))

            conn.commit()
            conn.close()

        return is_game_over

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str) -> None:
        self.number_of_moves += 1
        conn = sqlite3.connect('minesweeper.db')
        c = conn.cursor()
        c.execute('''INSERT INTO
        player_moves
        VALUES('{}', '{}', '{}', {}, {}, {}, {})'''.format(self.game_id,
                                                           self.user_id,
                                                           action,
                                                           time.time(),
                                                           choice[1],
                                                           choice[0],
                                                           self.number_of_moves))

        conn.commit()
        conn.close()
        return self.actual_minesweeper.players_choice_of_tile_and_action(choice, action)
