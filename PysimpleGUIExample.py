import PySimpleGUI as sg

from DifficultyEnum import Difficulty
from MinesweeperBoard import MinesweeperBoard
menu_def = [['Difficulty', ['Easy', 'Medium', 'Hard']]]
menu_ui = [sg.Menu(menu_def, )]
game = MinesweeperBoard(load_from_file= True, filename= 'gui3.txt')
layout = []
layout.append(menu_ui)
for i in range(game.row_size):
    layout.append([sg.Button('?', size=(4, 2), key=(i, j), pad=(0, 0)) for j in range(game.column_size)])

window = sg.Window('Minesweeper', layout, finalize=True)

# this is to capture right clicks ( crazy ... )
for r in range(game.row_size):
    for c in range(game.column_size):
        window[(r, c)].bind("<Button-2>", "Right")  # <----- this for windows might be Button-3
        window[(r, c)].bind("<Button-3>", "Right")  # <----- this for windows might be Button-3
show_everything = False
for r in range(game.row_size):
    for c in range(game.column_size):
        if show_everything or game.board[r][c].is_revealed:
           window[(r, c)].update(game.board[r][c].board_value(), button_color=('white', 'black'))

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event in ['Easy', 'Medium', 'Hard']:
        if game.has_not_started:
            game = MinesweeperBoard(difficulty=Difficulty[event.upper()])
        continue
    is_right_click = event[1] == "Right"
    coordinates = event if not is_right_click else event[0]
    if is_right_click:
        # right click logic
        window[coordinates].update('M')

        continue  # <--- this is needed for now otherwise left click logic will also happen

    # a change since right click even is ((r,c),"Right") left is just (r,c)

    game.players_choice_of_tile_and_action(coordinates, "reveal")
    if game.game_over():
        show_everything = True

    for r in range(game.row_size):
        for c in range(game.column_size):
            if show_everything or game.board[r][c].is_revealed:
                window[(r, c)].update(game.board[r][c].board_value(), button_color=('white', 'black'))

    if game.game_over():
        if game.human_wins:
            sg.popup_ok('WINNER!!')
        else:
            sg.popup_ok('LOSER!!!')

window.close()
