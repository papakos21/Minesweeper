class Tile:
    def __init__(self):
        self.is_revealed = False
        self.number_of_neighbour_bombs = 0
        self.bomb = False
        self.flag = False
        self.question_mark = False

    # tiles(bombs or number(0,1,2,3,4,5,6,7,8))
    # tile hidden or revealed
    def board_value(self) -> str:
        if self.is_revealed:
            if self.bomb:
                return "*"
            else:
                if self.number_of_neighbour_bombs > 0:
                    return str(self.number_of_neighbour_bombs)
                else:
                    return "  "
        else:
            return "  "
