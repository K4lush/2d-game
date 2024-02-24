from Player import Player
from Server import Server

class ClientHandler:
    client_count = 0  # Class variable to keep track of the number of connected clients

    def __init__(self, client, address, server):
        self.client = client
        self.address = address
        self.connected = True
        self.id = ClientHandler.client_count  # Assign the current count as the unique ID
        ClientHandler.client_count += 1  # Increment the count for the next client
        self.addPlayer()

    def addPlayer(self):
        if ClientHandler.client_count == 0:
            player = Player(ClientHandler.client_count, 200, 200, 50, 50, (255, 0, 255))
            self.server.players.append(player)
        else:
            player = Player(ClientHandler.client_count, 200, 100, 50, 50, (255, 200, 255))
            self.server.players.append(player)


    def handle(self):
        print("CONNECTED")
        while self.connected:
            try:
                self.server.broadcast()
                # self.recieve()
                # self.updateObjs()

            except:
                pass