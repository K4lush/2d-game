import pickle
import socket
import pygame  
from _thread import start_new_thread
import threading
from objects import stillObjects
from Player import Player
from Settings import Settings
import time
from Lava import Lava
from Rope import Rope

class ClientHandler:
    client_count = 0  # Class variable to keep track of the number of connected clients

    def __init__(self, client, address, server):
        self.client = client
        self.address = address
        self.server = server
        self.connected = True
        self.ready = False
        self.platforms_sent = False
        self.id = ClientHandler.client_count
        ClientHandler.client_count += 1

    def add_player(self, id, character_name):
        player = Player(id, character_name, 'idle', 'right', (200 if id == 0 else 100), 200, 50, 50,
                        (255, 0, 255 if id == 0 else 255, 200, 255))
        self.server.players.append(player)

        if len(self.server.players) == 2:
            self.server.create_rope_if_needed()

    def game(self):
        try:
            # # Send objects that needs to be sent once.
            # self.server.broadcast_platforms(self.client)

            print("ENTERING FOR CLIENT TO BE READY")
            self.wait_until_ready()

            # print("WAITING FOR BOTH  CLIENTS TO BE READY")
            # self.wait_until_all_ready()


            print("ENTERING GAME LOOP")
            self.game_loop()
        except Exception as e:
            print(f"Exception in client handler: {e}")
        finally:
            self.disconnect()

    def wait_until_ready(self):
        print("Server reached this point")
        while not self.ready:
            data = self.server.receive_from_client_state(self)
            print(data)

            state = data['state']
            character = data['character']

            if state == "READY":
                self.add_player(self.id, character)
                self.ready = True
                self.server.players_ready_state[self.id] = True


    def wait_until_all_ready(self):
        print(self.server.players_ready_state)
        while not all(self.server.players_ready_state):
            self.server.broadcast_state_to_client(self.client, "NOT READY")
            # time.sleep(0.4)
        self.server.broadcast_state_to_client(self.client, "READY")
        # time.sleep(0.5)

    def game_loop(self):
        while self.connected:
            self.server.broadcast_to_client(self.client)
            # if self.server.rope_created:
            #     self.server.rope.update()
            self.server.receive_from_client_update(self)

    def disconnect(self):
        self.connected = False
        self.server.remove_client_handler(self)
        self.client.close()  # Ensure the socket is closed to free up resources

class Server:
    def __init__(self, host="0.0.0.0", port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.client_handlers = []
        self.players_ready_state = [None, None]
        self.pressed_keys = {}  # In your server class

        ### Move to setting class ###
        self.rope_created = False
        self.rope = None
        self.players = []

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started, listening on IP: {self.host}")

        while True:
            client, addr = self.server.accept()
            client_handler = ClientHandler(client, addr, self)
            self.add_client_handler(client_handler)  # Use the new method to add client handlers
            start_new_thread(client_handler.game, ())

    def create_rope_if_needed(self):
        if len(self.players) == 2 and not self.rope_created:
            self.rope = Rope(self.players[0], self.players[1], 150)
            self.rope_created = True

    def add_client_handler(self, client_handler):
        with self.lock:
            self.client_handlers.append(client_handler)

    def remove_client_handler(self, client_handler):
        with self.lock:
            if client_handler in self.client_handlers:
                self.client_handlers.remove(client_handler)
                print(f"Client {client_handler.address} disconnected")

    def broadcast_to_client(self, client):
        gameState = {
            'Players': self.players,
            'Rope': self.rope
        }
        data = pickle.dumps(gameState)
        client.sendall(data)

    def broadcast_state_to_client(self, client, data):
        state = pickle.dumps(data)
        client.sendall(state)

    def broadcast_platforms(self, client):
        data = pickle.dumps(self.platforms)
        client.sendall(data)

    def receive_from_client_update(self, obj):
        data = pickle.loads(obj.client.recv(4096))
        if data:
            #print(f"Received data from client {obj.id}: {data}")
            # Update game objects based on received data
            # This is where you would update player positions, etc.
            self.update_objects(obj.id, data)

    def receive_from_client_state(self, obj):
        data = pickle.loads(obj.client.recv(4096))
        return data

    def update_objects(self, client_id, pressed_keys):
        player = self.find_player_by_id(client_id)
        self.pressed_keys[client_id] = pressed_keys  # Update which keys this client is pressing
        print(self.pressed_keys)

        print("SERVER: Received keys:", pressed_keys, "for player", player.id)  # Enhanced logging

        if player:
            if pressed_keys == ['idle']:
                player.action = 'idle'

            # 1. Apply Movement
            if "left" in pressed_keys:
                player.move_left()
                player.action = 'run'
                player.direction = 'left'  # Add direction attribute

            if "right" in pressed_keys:
                player.move_right()
                player.action = 'run'
                player.direction = 'right'  # Add direction attribute

            if "up" in self.pressed_keys[client_id]:  # Check if 'up' is being held down
                player.jump()

            # 3. Apply Gravity (conditionally)
            player.apply_gravity()

            # 4. Handle Collisions
            player.handle_collisions()  # Assuming you have a list of platforms

            # 5. Update Rope (if it exists)
            if self.rope:
                self.rope.update()



    def find_player_by_id(self, client_id):
        for player in self.players:
            if player.id == client_id:
                return player
        return None  # Return None if no matching player is found

if __name__ == '__main__':
    print("This is correct server file")
    server = Server()
    server.start_server()
