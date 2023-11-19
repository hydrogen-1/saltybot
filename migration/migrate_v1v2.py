import sqlite3

def main():
    connection = sqlite3.connect("../players.db")
    cur = connection.cursor()
    with open("v2.sql", "r") as script:
        cur.executescript(script.read())
    connection.commit()
    cur.close()
    connection.close()

if __name__ == "__main__":
    main()