import sqlite3
conn = sqlite3.connect("usctt.sqlite")
c = conn.cursor()
c.execute('''CREATE TABLE usctt
                    (discordid text, username text, password text)''')