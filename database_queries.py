import sqlite3
conn = sqlite3.connect('minesweeper.db')
c = conn.cursor()

c.execute('''SELECT * from games''')
for row in c.fetchall():
    print(row)

conn.commit()

conn.close()