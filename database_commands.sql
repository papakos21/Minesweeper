c.execute('''CREATE TABLE games
             (game_id text,
             user_id text,
             game_difficulty text,
             human_won text,
             number_of_completed_player_moves real,
             duration_in_seconds real,
             date text)''')

c.execute('''CREATE TABLE player_moves
             (game_id text,
             user_id text,
             type_of_move text,
             time_of_move real)''')

c.execute('''CREATE TABLE player_moves
             (game_id text,
             user_id text,
             type_of_move text,
             time_of_move real)''')

INSERT INTO games VALUES ('001','Alex','Hard','True',100,1000,'2020/09/14')

INSERT INTO player_moves VALUES ('001','Alex','reveal',1600087297)