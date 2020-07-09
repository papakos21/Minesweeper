from Tile import Tile
import random
from typing import List, Tuple


class MinesweeperBoard:

    def __init__(self, difficulty='easy', test_bombs_coordinates: List[Tuple[int, int]] = None,
                 test_board: List[List[Tile]] = None):

        coordinates = self.get_board_size(difficulty) if test_board is None else (len(test_board), len(test_board[0]))
        self.row_size = coordinates[0]
        self.column_size = coordinates[1]
        self.number_of_bombs = self.get_number_of_bombs(difficulty) if test_bombs_coordinates is None else len(
            test_bombs_coordinates)
        # self.x,self.y=self.get_board_size(difficulty)
        self.board: List[List[Tile]] = self.build_board(self.row_size,
                                                        self.column_size) if test_board is None else test_board
        self.position_of_bombs = self.get_position_of_bombs(self.number_of_bombs, self.row_size,
                                                            self.column_size) if test_board is None else None
        self.coordinates_of_bombs: List[Tuple[int, int]] = self.get_coordinate_position_of_bombs_2(
            self.position_of_bombs, self.row_size,
            self.column_size) if not test_bombs_coordinates else test_bombs_coordinates
        self.assign_bombs_to_tiles()
        self.assign_numbers_to_tiles()
        self.choice = None
        self.human_wins = False

        # self.coordinates_of_bombs = self.get_position_of_bombs_2(self.number_of_bombs, self.row_size, self.column_size)

        # self.board_size

    # Example of how to modify the fields of an object
    # tile = Tile()
    # tile.bomb = True
    # tile.number_of_neighbour_bombs += 1

    def get_board_size(self, difficulty: str):

        if difficulty not in ['easy', 'medium', 'hard']:
            raise ValueError("easy or medium or hard ")
        if difficulty == 'easy':
            row_index = 8
            column_index = 10
        elif difficulty == 'medium':
            row_index = 14
            column_index = 20
        elif difficulty == 'hard':
            row_index = 20
            column_index = 24
        coordinates = (row_index, column_index)
        return coordinates

    def get_number_of_bombs(self, difficulty: str):
        if difficulty == 'easy':
            number_of_bombs = 10
        elif difficulty == 'medium':
            number_of_bombs = 40
        elif difficulty == 'hard':
            number_of_bombs = 99
        return number_of_bombs

    def build_board(self, row_index: int, column_index: int):
        board = []
        for i in range(row_index):
            row = []
            for j in range(column_index):
                row.append(Tile())
            board.append(row)
        return board

    def get_position_of_bombs(self, number_of_bombs: int, row_index, column_index):
        number_of_tiles = row_index * column_index
        position_of_bombs = (random.sample(range(0, number_of_tiles), number_of_bombs))
        return (position_of_bombs)
        # returns N random *distinct* numbers between 1 and X * Y *exclusive*(meaning -1) [1, X*Y)

    # def get_position_of_bombs_2(self, number_of_bombs, row_size, column_size):
    #     all_coordinates = []
    #     for r in range(row_size):
    #         for c in range(column_size):
    #             all_coordinates.append((r, c))
    #     return random.sample(all_coordinates, number_of_bombs)
    #
    # def get_coordinate_position_of_bombs(self, position_of_bombs, column_size):
    #
    #     coordinates_to_return = []
    #     for p in position_of_bombs:
    #         coordinates_to_return.append((p // column_size, p % column_size))
    #     return coordinates_to_return
    # Returns list of bomb coordinates [(b1_Y,b1_X),...,(bN_Y,bN_X]
    # Hint: use for(iterate) division (//) for Y ,  and % (module) for X to calculate b<i>_Y and b<i>_X

    def get_coordinate_position_of_bombs_2(self, position_of_bombs, row_size, column_size):

        count = 0
        coordinates_to_return = []
        for r in range(row_size):
            for c in range(column_size):
                if count in position_of_bombs:
                    coordinates_to_return.append((r, c))
                count += 1
        return coordinates_to_return

    def assign_bombs_to_tiles(self):
        # for r in range(self.row_size):
        #     for c in range(self.column_size):
        for (r, c) in self.coordinates_of_bombs:
            self.board[r][c].bomb = True

    def assign_numbers_to_tiles(self):
        for (r, c) in self.coordinates_of_bombs:
            neighbours: List[Tuple[int, int]] = self.find_neighbours(r, c)
            for rn, cn in neighbours:

                    if self.board[rn][cn].bomb is False:
                        self.board[rn][cn].number_of_neighbour_bombs += 1

    def find_neighbours(self, r, c):
        neighbours_to_return = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if not(dr == 0 and dc == 0):
                    rn = dr + r
                    cn = dc + c
                    if 0 <= rn < self.row_size and 0 <= cn < self.column_size:
                            neighbours_to_return.append((rn, cn))
        # neighbours_to_return.append((r, c + 1))
        # neighbours_to_return.append((r - 1, c - 1))
        # neighbours_to_return.append((r - 1, c))
        # neighbours_to_return.append((r - 1, c + 1))
        # neighbours_to_return.append((r + 1, c - 1))
        # neighbours_to_return.append((r + 1, c))
        # neighbours_to_return.append((r + 1, c + 1))
        return neighbours_to_return

    def players_choice_of_tile_and_action(self, choice: Tuple[int, int], action: str):
        current_board_tile = self.board[choice[0]][choice[1]]
        self.choice = choice
        if action == 'reveal':
            current_board_tile.is_revealed = True
            if not current_board_tile.bomb:
                self.reveal_neighbours_if_not_bomb_or_number()
        if action == 'flag':
            current_board_tile.flag = True
        if action == 'question':
            current_board_tile.question_mark = True

        # player chooses a tile and then chooses if wants to reveal it, flag it, or question mark it

    def reveal_neighbours_if_not_bomb_or_number(self):
        # logic : ensure that current tile is 0(by using self.choice to access current tile
        if self.board[self.choice[0]][self.choice[1]].number_of_neighbour_bombs == 0:
            for coordinate in self.find_neighbours(self.choice[0], self.choice[1]):
                if self.board[coordinate[0]][coordinate[1]].is_revealed == False:
                    self.players_choice_of_tile_and_action(coordinate, 'reveal')


    def game_over(self) -> bool:
        if self.choice in self.coordinates_of_bombs:
            return True
        number_of_revealed_tiles_needed_for_winning = self.row_size * self.column_size - self.number_of_bombs
        number_of_revealed_tiles = self.count_of_revealed_tiles()
        if number_of_revealed_tiles == number_of_revealed_tiles_needed_for_winning:
            self.human_wins = True
            return True

        return False

    def count_of_revealed_tiles(self):
        count = 0
        for r in range(self.row_size):
            for c in range(self.column_size):
                if self.board[r][c].is_revealed:
                    count += 1
        return count

    """
    1.Will there be an input for coordinates by the user?
    2.Will there be a new attribute to Tile like self.flag or self.question_mark = False?
    3.We have to reprint the board every time?
    """
# board (size(x,y choice by the user)) (3 choices : easy,medium,hard)

# number of bombs,numbers,flags(graphic),question marks(graphic)
#
# _ _ _
# _ _ _
# _ _ _
#
