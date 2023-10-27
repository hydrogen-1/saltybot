import websocket
from dataclasses import dataclass
from collections.abc import Iterator
import threading
from queue import Queue

@dataclass
class Credentials():
    name: str
    token:str


class TwitchWsClient():
    def __init__(self, credentials: Credentials) -> None:
        self.wsapp = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv:443", on_message=self.handle_message, on_open=self.handle_connect, on_ping=self.handle_ping)
        self.creds = credentials
        self.message_queue = Queue()

    def handle_message(self, wsapp :websocket.WebSocketApp, msg: str) -> None:
        if(msg.startswith(":waifu4u!")):
            self.message_queue.put(msg)
        elif(msg == "PING"):
            print("PING")
            wsapp.send("PONG :tmi.twitch.tv")

    def handle_connect(self, wsapp: websocket.WebSocketApp) -> None:
        wsapp.send(f"PASS {self.creds.token}")
        wsapp.send(f"NICK {self.creds.name}")
        wsapp.send("JOIN #saltybet")

    def handle_ping(self, wsapp: websocket.WebSocketApp, msg: str) -> None:
        ...

    def start(self) -> None:
        self.ws_thread = threading.Thread(target=self.wsapp.run_forever)
        self.ws_thread.start()

    def messages(self) -> Iterator[str]:
        while(True):
            message = self.message_queue.get()
            yield(message)