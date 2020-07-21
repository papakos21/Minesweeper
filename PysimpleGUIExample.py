import PySimpleGUI as sg
from DifficultyEnum import Difficulty
from MinesweeperBoard import MinesweeperBoard
import time
from playsound import playsound

def load_minesweeper_window(difficulty: Difficulty = Difficulty.EASY, load_from_file: bool = False):
    menu_def = [['New Game', ['Easy', 'Medium', 'Hard']]]
    menu_ui = [sg.Menu(menu_def, )]
    game = MinesweeperBoard(load_from_file=load_from_file, filename='gui3.txt', difficulty=difficulty)
    layout = []
    layout.append(menu_ui)
    for i in range(game.row_size):
        layout.append([sg.Button('?', size=(2, 1), key=(i, j), pad=(0, 0)) for j in range(game.column_size)])
    layout.append([sg.Text(' ' , key="timer", size=(4, 1))])
    window = sg.Window('Minesweeper', layout, finalize=True)
    for r in range(game.row_size):
        for c in range(game.column_size):
            window[(r, c)].bind("<Button-2>", "Right")  # <----- this for windows might be Button-3
            window[(r, c)].bind("<Button-3>", "Right")  # <----- this for windows might be Button-3
    for r in range(game.row_size):
        for c in range(game.column_size):
            if game.board[r][c].is_revealed:
                window[(r, c)].update(game.board[r][c].board_value(), button_color=('white', 'black'))
    return (game, window)


game, window = load_minesweeper_window(load_from_file=True)

# this is to capture right clicks

startime = int(round(time.time()))


while True:
    event, values = window.read(timeout = 100)
    if event == '__TIMEOUT__':
        current_time = int(round(time.time()))
        time_value = str(current_time-startime)

        window[ "timer"].update(time_value)
        continue
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event in ['Easy', 'Medium', 'Hard']:
        # if game.has_not_started:
        pop_up_layout = [[sg.Text('Are you sure?')], [sg.Button('Yes'), sg.Button('No')]]
        pop_up_window = sg.Window('Decision', pop_up_layout, finalize=True)
        pop_up_event, pop_up_values = pop_up_window.read()
        if pop_up_event == 'Yes':

            window.close()
            game, window = load_minesweeper_window(difficulty=Difficulty[event.upper()])
            startime = int(round(time.time()))
        pop_up_window.close()

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
        if game.human_wins:
            sg.popup_ok('WINNER!!')
            playsound("eks.mp3")
        else:
            sg.popup_ok('LOSER!!!')

            playsound("mal.mp3")
    else:
        playsound("bravo.mp3")
    for r in range(game.row_size):
        for c in range(game.column_size):
            if  game.board[r][c].is_revealed:
                window[(r, c)].update(game.board[r][c].board_value(), button_color=('white', 'black'))



window.close()
