from Tile import Tile


class MinesweeperModel:

    def __init__(self, difficulty='easy'):

        coordinates = self.get_board_size(difficulty)
        self.row_index=coordinates[0]
        self.column_index=coordinates[1]
        self.number_of_bombs = self.get_number_of_bombs(difficulty)
        #self.x,self.y=self.get_board_size(difficulty)
        self.board = self.build_board(self.row_index, self.column_index)


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
        return (row_index, column_index)

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

        # Function4 Get_position_of_bombs: input number of bombs N and number of tile objects X * Y
        # returns N random distinct numbers between 0 and X * Y exclusive(meaning -1) [0, X*Y)

        # Function5 Assign_bombs_to_tiles: input board and bomb indexes from Function4
        # returns board with bomb tiles assigned.

        # Function6 Assign_numbers_to_tiles: input board from Function5
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
