import PySimpleGUI as sg
from MinesweeperBoard import MinesweeperBoard

game = MinesweeperBoard()


layout =  [[sg.Button('?', size=(4, 2), key=(i,j), pad=(0,0)) for j in range(game.column_size)] for i in range(game.row_size)]

window = sg.Window('Minesweeper', layout)
show_everything = False
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    # window[(row, col)].update('New text')   # To change a button's text, use this pattern
    game.players_choice_of_tile_and_action(event, "reveal")
    if game.game_over():
        show_everything = True
        if game.human_wins:
            sg.popup_ok('WINNER!!')
        else:
            sg.popup_ok('LOSER!!!')
    for r in range (game.row_size):
        for c in range (game.column_size):
            if show_everything or game.board[r][c].is_revealed:
                window[(r,c)].update(game.board[r][c].board_value(), button_color=('white','black'))




window.close()