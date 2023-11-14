import sqlite3

def main():
    connection = sqlite3.connect("players.db")
    cur = connection.cursor()
    with open("migration/v1.sql", "r") as script:
        cur.executescript(script.read())
        cur.execute(
            """
            SELECT p1, p2 FROM matches
            """
        )
    pairs = cur.fetchall()
    players = {}
    for p1, p2 in pairs:
        if(players.get(p1)):
            players[p1] += 1
        else:
            players[p1] = 1
        if(players.get(p2)):
            players[p2] += 1
        else:
            players[p2] = 1
    for id, count in players.items():
        cur.execute(
            """
            UPDATE players
            SET num_fights = ?
            WHERE id = ?
            """,
            (count, id, )
        )
    connection.commit()
    cur.close()
    connection.close()


if __name__ == "__main__":
    main()