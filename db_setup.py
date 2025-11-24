import sqlite3
import requests


def create_player_stats_table():
    """Create database table which will contain player statistics"""
    conn = sqlite3.connect('fantasy_football_data.db')
    c = conn.cursor()

    base_url = 'https://fantasy.premierleague.com/api/'
    r = requests.get(base_url + 'bootstrap-static/').json()

    c.execute("DROP TABLE IF EXISTS player_stats")

    c.execute("""CREATE TABLE player_stats (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 position INTEGER,
                 xG1 INTEGER,
                 xG2 INTEGER,
                 xG3 INTEGER,
                 xG4 INTEGER,
                 xG5 INTEGER,
                 xA1 INTEGER,
                 xA2 INTEGER,
                 xA3 INTEGER,
                 xA4 INTEGER,
                 xA5 INTEGER)
                 """)

    elements = r['elements']
    for i in range(len(elements)):
        id_ = elements[i]['id']
        name = elements[i]['second_name'] + ', ' + elements[i]['first_name']
        pos = elements[i]['element_type']  # position of each player in FPL
        r2 = requests.get(base_url + 'element-summary/' + str(id_)).json()

        try:
            g1, g2, g3, g4, g5 = (r2['history'][-1]['expected_goals'], r2['history'][-2]['expected_goals'],
                                  r2['history'][-3]['expected_goals'], r2['history'][-4]['expected_goals'],
                                  r2['history'][-5]['expected_goals'])

            a1, a2, a3, a4, a5 = (r2['history'][-1]['expected_assists'], r2['history'][-2]['expected_assists'],
                                  r2['history'][-3]['expected_assists'], r2['history'][-4]['expected_assists'],
                                  r2['history'][-5]['expected_assists'])

            c.execute("INSERT INTO player_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (id_, name, pos, g5, g4, g3, g2, g1, a5, a4, a3, a2, a1))
        except:
            ()

    c.execute("ALTER TABLE player_stats ADD COLUMN xGxA1 INTEGER")
    c.execute("ALTER TABLE player_stats ADD COLUMN xGxA2 INTEGER")
    c.execute("ALTER TABLE player_stats ADD COLUMN xGxA3 INTEGER")
    c.execute("ALTER TABLE player_stats ADD COLUMN xGxA4 INTEGER")
    c.execute("ALTER TABLE player_stats ADD COLUMN xGxA5 INTEGER")

    c.execute("""UPDATE player_stats
                 SET xGxA1 = ROUND(xG1+xA1, 2),
                 xGxA2 = ROUND(xG2+xA2, 2),
                 xGxA3 = ROUND(xG3+xA3, 2),
                 xGxA4 = ROUND(xG4+xA4, 2),
                 xGxA5 = ROUND(xG5+xA5, 2)
                 """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Database setup started")
    create_player_stats_table()
    print("Database setup completed successfully")
