from Tile import Tile
import random


class MinesweeperModel:

    def __init__(self, difficulty='easy'):

        coordinates = self.get_board_size(difficulty)
        self.row_size=coordinates[0]
        self.column_size=coordinates[1]
        self.number_of_bombs = self.get_number_of_bombs(difficulty)
        #self.x,self.y=self.get_board_size(difficulty)
        self.board = self.build_board(self.row_size, self.column_size)
        self.position_of_bombs = self.get_position_of_bombs(self.number_of_bombs, self.row_size, self.column_size)
        self.coordinates_of_bombs = self.get_coordinate_position_of_bombs(self.position_of_bombs, self.row_size, self.column_size)
        #self.coordinates_of_bombs = self.get_position_of_bombs_2(self.number_of_bombs, self.row_size, self.column_size)

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
        board=[]
        for i in range(row_index):
            row = []
            for j in range(column_index):
                row.append(Tile())
            board.append(row)
        return board

    def get_position_of_bombs(self, number_of_bombs: int, row_index, column_index):
        number_of_tiles = row_index*column_index
        position_of_bombs = (random.sample(range(0, number_of_tiles), number_of_bombs))
        return (position_of_bombs)
        # returns N random *distinct* numbers between 1 and X * Y *exclusive*(meaning -1) [1, X*Y)

    def get_position_of_bombs_2(self, number_of_bombs, row_size, column_size):
        all_coordinates = []
        for r in range (row_size):
            for c in range (column_size):
                all_coordinates.append((r,c))
        return random.sample(all_coordinates, number_of_bombs)



    def get_coordinate_position_of_bombs(self, position_of_bombs, column_size):
        coordinates_to_return = []
        for p in position_of_bombs:
            coordinates_to_return.append((p//column_size, p%column_size))
        return coordinates_to_return
        # Returns list of bomb coordinates [(b1_Y,b1_X),...,(bN_Y,bN_X]
        # Hint: use for(iterate) division (//) for Y ,  and % (module) for X to calculate b<i>_Y and b<i>_X

    def get_coordinate_position_of_bombs_2(self, position_of_bombs, row_size, column_size):
        count = 0
        coordinates_to_return = []
        for r in range (row_size):
            for c in range (column_size):
                if count in position_of_bombs:
                    coordinates_to_return.append((r,c))
                    count+= 1
        return coordinates_to_return



        # Function6 Assign_bombs_to_tiles: input board and bomb indexes from Function4
        # returns board with bomb tiles assigned.

        # Function7
        # Assign_numbers_to_tiles: input board from Function5
        # returns board with tile numbers assigned.

    # board (size(x,y choice by the user)) (3 choices : easy,medium,hard)

    # number of bombs,numbers,flags(graphic),question marks(graphic)
    #
    # _ _ _
    # _ _ _
    # _ _ _
    #

    # game over : 1)all revealed except for the bombs(win) 2)when user clicks a bomb tile(lose)
    # bombs placed randomly
    # the numbers are calculated AFTER bomb assignment
