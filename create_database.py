import sqlite3
conn = sqlite3.connect('minesweeper.db')
c = conn.cursor()

c.execute('''CREATE TABLE games
             (game_id text,
             user_id text,
             game_difficulty text,
             human_won text,
             number_of_completed_player_moves real,
             duration_in_seconds real,
             date text,
             initial_game_state text)''')

c.execute('''CREATE TABLE player_moves
             (game_id text,
             user_id text,
             type_of_move text,
             time_of_move real,
             column_played real,
             row_played real,
             move_index real)''')



conn.commit()

conn.close()