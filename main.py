from twitchwsclient import TwitchWsClient, Credentials
from database import DatabaseClient
import json
import re

def main():
    with open("login.json", "r") as credentials_file:
        data = json.load(credentials_file)
        creds = Credentials(data.get("name"), data.get("oauth_token"))
    print(f"Hello {creds.name}")
    client = TwitchWsClient(creds)
    client.start()
    db = DatabaseClient("players.db")
    messages = client.messages()
    current_match = 0
    for msg in messages:
        print(msg)
        if(msg.find("(exhibitions)") != -1):
            current_match = 0
            continue
        elif(msg.find("Bets are OPEN") != -1):
            m = re.search(r"Bets are OPEN for (.+) vs (.+)!", msg)
            player1, player2 = m.groups()
            if(not db.known_player(player1)):
                p1_id = db.add_player(player1)
            else:
                p1_id = db.get_player_id(player1)
            if(not db.known_player(player2)):
                p2_id = db.add_player(player2)
            else:
                p2_id = db.get_player_id(player2)
            current_match = db.add_match(p1_id, p2_id)
            
        elif(msg.find("wins!") != -1):
            m = re.search(r"#saltybet :(.+) wins!", msg)
            winner = m.groups()[0]
            if(current_match != 0):
                winner = db.add_winner(current_match, winner)


                p1, p2 = db.get_players_from_match(current_match)
                outcome = 1 if winner == p1 else 0
                p1_elo = db.get_elo(p1)
                p2_elo = db.get_elo(p2)

                p1_e = 1/(1+ pow(10,(p2_elo - p1_elo) / 400))
                p2_e = 1- p1_e

                p1_elo = p1_elo + 32 * (outcome - p1_e)
                p2_elo = p2_elo + 32 * ((1-outcome) - p2_e)

                db.update_elo(p1, int(p1_elo))
                db.update_elo(p2, int(p2_elo))



if __name__ == "__main__":
    main()