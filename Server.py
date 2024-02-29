import pickle
import socket
import pygame
from threading import Thread

from _thread import start_new_thread
import threading

from PlatformObjects import StillObjects
from Player import Player
from Settings import Settings
from MapServer import MapServer
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
        self.id = ClientHandler.client_count
        ClientHandler.client_count += 1

    def add_player(self, id, character_name):
        player = Player(id, character_name, 'idle', 'right', (200 if id == 0 else 100), 350, 50, 50,
                        (255, 0, 255 if id == 0 else 255, 200, 255))
        self.server.players.append(player)

        if len(self.server.players) == 2:
            self.server.create_rope_if_needed()

    def game(self):
        try:
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
        self.server.broadcast_state_to_client(self.client, "READY")

    def game_loop(self):
        while self.connected:
            self.server.broadcast_to_client(self.client)
            self.server.receive_from_client_update(self)

    def disconnect(self):
        self.connected = False
        self.server.remove_client_handler(self)
        self.client.close()  # Ensure the socket is closed to free up resources


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.settings = MapServer()
        self.client_handlers = []
        self.players_ready_state = [None, None]
        self.pressed_keys = {}  # In your server class

        ### Move to setting class ###
        self.platforms_sent = False
        self.rope_created = False
        self.rope = None
        self.players = []
        self.lavaBlocks = []
        self.BiglavaBlock = None
        self.CreateLava()
        self.platforms = self.create_platform_rects()  # Create platform rects
        self.CreateBigLavaBlock()

        # self.start_server()

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started, listening on IP: {self.host}")

        while True:
            client, addr = self.server.accept()
            client_handler = ClientHandler(client, addr, self)
            self.add_client_handler(client_handler)  # Use the new method to add client handlers
            start_new_thread(client_handler.game, ())

    def CreateBigLavaBlock(self):
        self.BiglavaBlock = Lava(99, 0, 848, 1000, 1000)

    def CreateLava(self):
        for i in range(20):
            ##each lava width is 48 pixels, so draw every 48 pixels accross screen.
            ## we want to draw them 64*however many blocks depths we have in self.map in order for the lava to spawn at bottom of map
            lava = Lava(i, i * 48, 800, 48, 48)
            self.lavaBlocks.append(lava)

    def create_rope_if_needed(self):
        if len(self.players) == 2 and not self.rope_created:
            self.rope = Rope(self.players[0], self.players[1], 150)
            self.rope_created = True

    def create_platform_rects(self):
        platforms = []
        block_width = 68  # The width of each block
        block_height = 68  # The height of each block

        for row_index, row in enumerate(self.settings.map):
            for col_index, cell in enumerate(row):
                if cell == 1:  # 1 represents a block
                    block_rect = pygame.Rect(col_index * block_width, row_index * block_height, block_width,
                                             block_height)
                    platforms.append(block_rect)

        return platforms

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
            'Rope': self.rope,
            'Lava': self.lavaBlocks,
            'LavaBlock': self.BiglavaBlock
        }

        data = pickle.dumps(gameState)
        client.sendall(data)

    def broadcast_state_to_client(self, client, data):
        state = pickle.dumps(data)
        client.sendall(state)

    def receive_from_client_update(self, obj):
        data = pickle.loads(obj.client.recv(4096))
        if data:
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

            print("PLAYER: Ground Flag ", player.on_ground)

            if "up" in self.pressed_keys[client_id]:  # Check if 'up' is being held down
                player.jump()
                player.action = 'run'

            # 3. Apply Gravity (conditionally)
            if not player.on_ground:
                player.apply_gravity()



            # # 4. Handle Collisions
            player.handle_collisions(self.platforms)  # Assuming you have a list of platforms

            # 5. Update Rope (if it exists)
            if self.rope:
                self.rope.update()

            for lava in self.lavaBlocks:
                lava.update()

            self.BiglavaBlock.update()
            

    def find_player_by_id(self, client_id):
        for player in self.players:
            if player.id == client_id:
                return player
        return None  # Return None if no matching player is found


# if __name__ == '__main__':
# #     print("This is correct server file")
# def create_server(ip, port):
#     server = Server(ip, port)
#     server.start_server()
