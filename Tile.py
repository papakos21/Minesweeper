class Tile:
    def __init__(self):
        self.is_revealed = False
        self.number_of_neighbour_bombs = 0
        self.bomb = False
    # tiles(bombs or number(0,1,2,3,4,5,6,7,8))
    # tile hidden or revealed
