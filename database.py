import sqlite3

class DatabaseClient:
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self) -> None:
        with open("db.sql", "r") as f:
            statements = f.read()
            cur = self.connection.cursor()
            cur.executescript(statements)
            cur.close()

    def add_player(self, name: str) -> int:
        cur = self.connection.cursor()
        cur.execute("INSERT INTO players (name, elo) VALUES (?, 1000)", (name,))
        id = cur.lastrowid
        self.connection.commit()
        cur.close()
        return id

    def known_player(self, name: str) -> bool:
        cur = self.connection.cursor()
        cur.execute("SELECT id, name FROM players WHERE name = ?", (name,))
        players = cur.fetchall()
        cur.close()
        for player in players:
            if(name in player):
                return True
        return False
    
    def get_player_id(self, name: str) -> int:
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM players WHERE name = ?", (name,))
        id = cur.fetchone()
        cur.close()
        if(id != None):
            return id[0]
        return 0
    
    def add_match(self, p1: int, p2: int) -> int:
        cur = self.connection.cursor()
        cur.execute("INSERT INTO matches (p1, p2) VALUES (?, ?)", (p1, p2,))
        id = cur.lastrowid
        self.connection.commit()
        cur.close()
        return id
    
    def add_winner(self, id: int, winner: str) -> int:
        winner_id = self.get_player_id(winner)
        cur = self.connection.cursor()
        cur.execute("UPDATE matches SET winner = ? WHERE id = ?", (winner_id, id))
        self.connection.commit()
        cur.close()
        return winner_id

    def get_elo(self, id: int) -> int:
        cur  = self.connection.cursor()
        cur.execute("SELECT elo FROM players WHERE id = ?", (id,))
        elo = cur.fetchone()
        cur.close()
        if(elo != None):
            return elo[0]
        else:
            return 1000

    def update_elo(self, id: int, elo: int) -> None:
        cur = self.connection.cursor()
        cur.execute("UPDATE players SET elo = ? WHERE id = ?", (elo, id, ))
        self.connection.commit()
        cur.close()

    def get_players_from_match(self, id: int) -> tuple[int]:
        cur = self.connection.cursor()
        cur.execute("SELECT p1, p2 FROM matches WHERE id = ?", (id, ))
        players = cur.fetchone()
        cur.close()
        return players

    def __del__(self):
        self.connection.close()