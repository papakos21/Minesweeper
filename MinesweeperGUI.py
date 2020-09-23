"""This is the GUI"""
from threading import Thread
import sqlite3
import time
import PySimpleGUI as sg
from DataBaseManager import DataBaseManager
from playsound import playsound
from DifficultyEnum import Difficulty
from MinesweeperBoard import MinesweeperBoardDatabaseTracker, RemoteMinesweeperBoard
from MinesweeperBoard import MinesweeperBoard
DATABASEMANAGER = DataBaseManager("minesweeper.db")
REMOTE = False
COLOR_MAP = {0: 'white', 1: 'green', 2: 'purple', 3: 'blue', 4: 'brown', 5: 'orange',
             6: 'grey', 7: 'pink', 8: 'yellow'}
DIFFICULTY = "Difficulty.Easy"

file_handler =  open("user_name", "r")
USER_ID = file_handler.read()

def my_playsound(filename):
    """Playsound"""
    if not MUTED:
        my_thread = Thread(target=playsound, args=(filename,))
        my_thread.start()


def paint_board(game, window):
    """Paint Board"""
    for row in range(game.get_row_size()):
        for column in range(game.get_column_size()):
            if game.get_tile(row, column).is_revealed:
                window[(row, column)].update(game.get_tile(row, column).board_value(), disabled=True,
                                             button_color=('white', 'black'),
                                             disabled_button_color=
                                             (COLOR_MAP[game.get_tile(row, column).number_of_neighbour_bombs], 'black')
                                             )
            if game.get_tile(row, column).flag:
                window[(row, column)].update(u'\u2713', button_color=('red', '#283b5b'))


def load_minesweeper_window(difficulty: Difficulty = Difficulty.EASY, load_from_file: bool = False):
    """Load mineSweeper Window"""
    global REMOTE
    global DIFFICULTY
    menu_def = [['New Game', ['Easy', 'Medium', 'Hard']],
                ['Options', ['Toggle Sound', 'Local', 'Remote','High scores']]]
    menu_ui = [sg.Menu(menu_def, )]
    DIFFICULTY = str(difficulty)
    if REMOTE:
        try:
            game = RemoteMinesweeperBoard(difficulty,user_id=USER_ID)


        except:
            print('it was not possible to connect to server. Changing to local mode.')
            REMOTE = False
            game = MinesweeperBoardDatabaseTracker(MinesweeperBoard(load_from_file=load_from_file,
                                                                    filename='gui3.txt',
                                                                    difficulty=difficulty), user_id = USER_ID)
    else:
        game = MinesweeperBoardDatabaseTracker(MinesweeperBoard(load_from_file=load_from_file,
                                                                filename='gui3.txt',
                                                                difficulty=difficulty), user_id = USER_ID)

    layout = [menu_ui]
    for row_index in range(game.get_row_size()):
        layout.append([sg.Button('?', size=(2, 1),
                                 key=(row_index, column_index),
                                 pad=(0, 0)) for column_index in range(game.get_column_size())])
    layout.append([sg.Text(' ', key="timer", size=(8, 1))])
    window = sg.Window('Minesweeper', layout, finalize=True)
    # Adding support for right click
    for row in range(game.get_row_size()):
        for column in range(game.get_column_size()):
            window[(row, column)].bind("<Button-2>", "Right")
            window[(row, column)].bind("<Button-3>", "Right")
    paint_board(game, window)
    return game, window


game, window = load_minesweeper_window(load_from_file=True)

start_time = int(round(time.time() * 100))
MUTED = True

while True:
    event, values = window.read(timeout=10)
    if event == '__TIMEOUT__':
        current_time = int(round(time.time() * 100)) - start_time

        window["timer"].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                             (current_time // 100) % 60,
                                                             current_time % 100))
        continue
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Toggle Sound':
        MUTED = not MUTED
        continue
    if event == "High scores":
        high_scores = DATABASEMANAGER.get_top_times(DIFFICULTY,3)
        rows = []
        for entry in high_scores:
            rows.append([sg.Text(entry[0]),sg.Text(entry[1])])
        pop_up_layout = [[sg.Text('High Scores')]]
        pop_up_layout.extend(rows)
        pop_up_window = sg.Window('Decision', pop_up_layout, finalize=True)
        pop_up_event, pop_up_values = pop_up_window.read()
        if pop_up_event == 'Yes':
            window.close()
        continue
    if event in ['Local', 'Remote']:
        if event is 'Remote':
            REMOTE = True
        else:
            REMOTE = False
        continue
    if event in ['Easy', 'Medium', 'Hard']:
        # if game.has_not_started:
        pop_up_layout = [[sg.Text('Are you sure?')], [sg.Button('Yes'), sg.Button('No')]]
        pop_up_window = sg.Window('Decision', pop_up_layout, finalize=True)
        pop_up_event, pop_up_values = pop_up_window.read()
        if pop_up_event == 'Yes':
            window.close()
            game, window = load_minesweeper_window(difficulty=Difficulty[event.upper()])
            start_time = int(round(time.time() * 100))
        pop_up_window.close()

        continue
    is_right_click = event[1] == "Right"
    coordinates = event if not is_right_click else event[0]
    if is_right_click:
        # right click logic
        if game.get_tile(coordinates[0], coordinates[1]).is_revealed:
            continue
        game.players_choice_of_tile_and_action(coordinates, "flag")
        if game.get_tile(coordinates[0], coordinates[1]).flag:
            window[coordinates].update(u'\u2713', button_color=('red', '#283b5b'))
        else:
            window[coordinates].update('?', button_color=('white', '#283b5b'))

        continue  # <--- this is needed for now otherwise left click logic will also happen

    # a change since right click even is ((r,c),"Right") left is just (r,c)
    tile_text = window[coordinates].ButtonText
    if tile_text == u'\u2713':
        continue
    game.players_choice_of_tile_and_action(coordinates, "reveal")

    if game.game_over():
        if game.human_won():

            sg.popup_ok('WINNER!!')
            my_playsound("eks.mp3")
        else:

            sg.popup_ok('LOSER!!!')

            my_playsound("mal.mp3")
    else:
        my_playsound("bravo.mp3")
    paint_board(game, window)

window.close()
