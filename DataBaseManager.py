import sqlite3


class DataBaseManager:
    def __init__(self, database_name):
        self.database_name = database_name

    def get_top_times(self, difficulty, limit):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT user_id, duration_in_seconds from games WHERE game_difficulty = '{}' AND human_won = '{}'
         ORDER BY duration_in_seconds ASC LIMIT {}'''.format(difficulty, 'True', limit))
        result_accumulator = []
        for row in cursor.fetchall():
            print(row)
            result_accumulator.append(row)
        conn.close()
        return result_accumulator