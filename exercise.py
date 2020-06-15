import random
from Tile import Tile
def get_position_of_bombs(number_of_bombs: int, row_index, column_index):
        number_of_tiles = row_index*column_index
        #position_of_bombs = (random.sample(range(0, number_of_tiles), number_of_bombs))
        position_of_bombs = []
        while len(position_of_bombs) != number_of_bombs:
            current_random_number = random.randint(0,number_of_tiles-1)
            if current_random_number not in position_of_bombs:
                position_of_bombs.append(current_random_number)
        return (position_of_bombs)

    # def build_board(self, row_index: int, column_index: int):
    #     board=[]
    #     for i in range(row_index):
    #         row = []
    #         for j in range(column_index):
    #             row.append(Tile())
    #         board.append(row)
    #     return board

def build_board(row_index, column_index):
    #row = [Tile() for _ in range(column_index)]
    return [[Tile() for _ in range(column_index)] for _ in range(row_index)]
   

print(build_board(5,5))


# [[<Tile.Tile object at 0x7f4507600b70>, <Tile.Tile object at 0x7f4507600c18>, <Tile.Tile object at 0x7f450761b908>, <Tile.Tile object at 0x7f45076169b0>,
# <Tile.Tile object at 0x7f4507609fd0>], [<Tile.Tile object at 0x7f4507600b70>, <Tile.Tile object at 0x7f4507600c18>, <Tile.Tile object at 0x7f450761b908>,
# <Tile.Tile object at 0x7f45076169b0>, <Tile.Tile object at 0x7f4507609fd0>], [<Tile.Tile object at 0x7f4507600b70>, <Tile.Tile object at 0x7f4507600c18>,
# <Tile.Tile object at 0x7f450761b908>, <Tile.Tile object at 0x7f45076169b0>, <Tile.Tile object at 0x7f4507609fd0>], [<Tile.Tile object at 0x7f4507600b70>,
# <Tile.Tile object at 0x7f4507600c18>, <Tile.Tile object at 0x7f450761b908>, <Tile.Tile object at 0x7f45076169b0>, <Tile.Tile object at 0x7f4507609fd0>],
# [<Tile.Tile object at 0x7f4507600b70>, <Tile.Tile object at 0x7f4507600c18>, <Tile.Tile object at 0x7f450761b908>, <Tile.Tile object at 0x7f45076169b0>,
# <Tile.Tile object at 0x7f4507609fd0>]]
