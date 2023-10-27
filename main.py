from twitchwsclient import TwitchWsClient, Credentials
import json

def main():
    with open("login.json", "r") as credentials_file:
        data = json.load(credentials_file)
        creds = Credentials(data.get("name"), data.get("oauth_token"))
    print(f"Hello {creds.name}")
    client = TwitchWsClient(creds)
    client.start()
    print("Listening for messages!")
    messages = client.messages()
    for msg in messages:
        print(msg)

if __name__ == "__main__":
    main()