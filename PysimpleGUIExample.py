import PySimpleGUI as sg
from MinesweeperBoard import MinesweeperBoard

game = MinesweeperBoard()

sg.theme('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
layout = []
for r in range(game.row_size):
    row = []
    for c in range(game.column_size):
            row.append(sg.Button(' '))
    layout.append(row)

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()