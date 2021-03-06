"""module containing Minesweeper model"""
import random
import os.path
import pickle
from Tile import Tile
from DifficultyEnum import Difficulty
from typing import List, Tuple


class MinesweeperBoard:
    """the MinesweeperBoard"""

    def __init__(self, difficulty: Difficulty = Difficulty.EASY,
                 test_bombs_coordinates: List[Tuple[int, int]] = None,
                 test_board: List[List[Tile]] = None,
                 load_from_file: bool = False,
                 filename: str = './game.txt'):
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

    def build_board(self, row_index: int, column_index: int) -> List[List[Tile]]:
        """build board"""
        board = []
        for _ in range(row_index):
            row = []
            for _ in range(column_index):
                row.append(Tile())
            board.append(row)
        return board

    def get_position_of_bombs(self, number_of_bombs: int,
                              row_index: int,
                              column_index: int) -> List[int]:
        """get position of bombs"""
        number_of_tiles = row_index * column_index
        position_of_bombs = (random.sample(range(0, number_of_tiles), number_of_bombs))
        return position_of_bombs

    def get_coordinate_position_of_bombs_2(self,position_of_bombs: List[int],
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
        if action == 'flag':
            current_board_tile.flag = not current_board_tile.flag
        if action == 'question':
            current_board_tile.question_mark = True
        self.save_game()
        # player chooses a tile and then chooses if wants to reveal it, flag it, or question mark it

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
