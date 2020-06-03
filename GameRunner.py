from MinesweeperModel import MinesweeperModel

difficulty = input("Choose: easy, medium, hard : ")

game = MinesweeperModel(difficulty)
game.get_board_size(difficulty)
game.get_number_of_bombs(difficulty)

