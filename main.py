from database import DatabaseClient
import json
import re
from twitchchat_wss import TwitchChatClient


def play(client: TwitchChatClient, db: DatabaseClient):
    current_match = 0
    for msg in client.messages():
        if(msg.find("waifu4u") == -1):
            continue
        if msg.find("(exhibitions)") != -1:
            current_match = 0
            continue

        elif msg.find("Bets are OPEN") != -1:
            m = re.search(r"Bets are OPEN for (.+) vs (.+)!", msg)
            player1, player2 = m.groups()
            p1_id, p1_games = db.known_player(player1)
            p2_id, p2_games = db.known_player(player2)
            current_match = db.add_match(p1_id, p2_id)
            if p1_games >= 10 and p2_games >= 10:
                print("--------------------------------")
                print(f"{player1}: {db.get_elo(p1_id)}\n{player2}: {db.get_elo(p2_id)}")
                print("--------------------------------\n")

        elif msg.find("Bets are locked.") != -1:
            m = re.search(r"\$([0-9,]*),.*\$([0-9,]*)", msg)
            pot1, pot2 = [int(x.replace(",", "")) for x in m.groups()]
            if(current_match != 0):
                db.add_pot(current_match, pot1, pot2)

        elif msg.find("wins!") != -1:
            m = re.search(r"#saltybet :(.+) wins!", msg)
            winner = m.groups()[0]
            if current_match != 0:
                winner = db.add_winner(current_match, winner)

                p1, p2 = db.get_players_from_match(current_match)
                outcome = 1 if winner == p1 else 0
                p1_elo = db.get_elo(p1)
                p2_elo = db.get_elo(p2)

                p1_e = 1 / (1 + pow(10, (p2_elo - p1_elo) / 400))
                p2_e = 1 - p1_e

                p1_elo = p1_elo + 32 * (outcome - p1_e)
                p2_elo = p2_elo + 32 * ((1 - outcome) - p2_e)

                db.update_elo(p1, int(p1_elo))
                db.update_elo(p2, int(p2_elo))


def main():
    with open("login.json", "r") as credentials_file:
        data = json.load(credentials_file)
        username = data.get("name")
        oauth_token = data.get("oauth_token")
    print(f"Hello {username}")
    client = TwitchChatClient(username, oauth_token, ["saltybet"])
    client.start()
    db = DatabaseClient("players.db")
    try:
        play(client, db)
    except KeyboardInterrupt:
        print("Quitting now")
    finally:
        db.close()
        client.close()


if __name__ == "__main__":
    main()
