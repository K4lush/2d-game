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

    # def addPlayer(self, id):
    #     if id == 0:
    #         player = Player(id, 'NinjaFrog', 'idle',  'right', 200, 200, 50, 50, (255, 0, 255))
    #         self.server.players.append(player)
    #     else:
    #         player = Player(id, 'MaskDude', 'idle', 'right', 200, 100, 50, 50, (255, 200, 255))
    #         self.server.players.append(player)
    #         self.server.create_rope_if_needed()

    def addPlayer(self, id, character_name):
        player = Player(id, character_name, 'idle', 'right', 200, (200 if id == 0 else 100), 50, 50,
                        (255, 0, 255 if id == 0 else 255, 200, 255))
        self.server.players.append(player)
        if len(self.server.players) == 2:
            self.server.create_rope_if_needed()

    def game(self):
        try:
            # Send objects that needs to be sent once.
            self.server.broadcast_platforms(self.client)

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

            if state == 'READY':
                self.addPlayer(self.id, character)
                self.ready = True
                self.server.players_ready_state[self.id] = True
            time.sleep(0.4)

    def wait_until_all_ready(self):
        while not all(self.server.players_ready_state):
            self.server.broadcast_state_to_client(self.client, "NOT READY")
            time.sleep(0.4)
        self.server.broadcast_state_to_client(self.client, "READY")
        # time.sleep(0.5)

    def game_loop(self):
        while self.connected:
            self.server.broadcast_to_client(self.client)
            if self.server.rope_created:
                self.server.rope.update()
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
        self.settings = Settings()
        self.client_handlers = []
        self.players = []
        self.platforms = []
        self.lavaObj = []
        self.players_ready_state = [None, None]
        self.game_started = False
        self.lavaSent = False
        self.lavaBlock = []
        self.rope = None
        self.rope_created = False
        self.CreateTerrain_sprites()
        self.CreateLava_Objs()
        self.CreateLava()

    def create_rope_if_needed(self):
        if len(self.players) == 2 and not self.rope_created:
            self.rope = Rope(self.players[0], self.players[1])
            self.rope_created = True


    def CreateLava(self):
        #lavaSheet = pygame.image.load('assets/Terrain/lavaAnimation.png').convert_alpha()
        #frame1 = lavaSheet.subsurface((0, 221, 16, 16))
        lavaObj = Lava(99, 0, 548, 1000, 1000)
        self.lavaBlock.append(lavaObj)

    def CreateLava_Objs(self):
        for i in range(20):
            ##each lava width is 48 pixels, so draw every 48 pixels accross screen. 
            ## we want to draw them 64*however many blocks depths we have in self.map in order for the lava to spawn at bottom of map
            lava = Lava(i,i*48, 500, 48, 48)
            self.lavaObj.append(lava)

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started, listening on IP: {self.host}")

        while True:
            client, addr = self.server.accept()
            client_handler = ClientHandler(client, addr, self)
            self.add_client_handler(client_handler)  # Use the new method to add client handlers
            start_new_thread(client_handler.game, ())

    def add_client_handler(self, client_handler):
        with self.lock:
            self.client_handlers.append(client_handler)

    def remove_client_handler(self, client_handler):
        with self.lock:
            if client_handler in self.client_handlers:
                self.client_handlers.remove(client_handler)
                print(f"Client {client_handler.address} disconnected")
    
    def CreateTerrain_sprites(self):
        tile_size = 64  # Size of each tile
        # Assuming self.settings.map is a 2D list indicating the type of tile at each position
        for row_index, row in enumerate(self.settings.map):
            for col_index, tile_type in enumerate(row):
                if tile_type == 1:
                    x = col_index * tile_size
                    y = row_index * tile_size
                    block = stillObjects(x,y,tile_size,tile_size,sprite=None)
                    self.platforms.append(block)

    def loopLava(self):
        for lava in self.lavaObj:
            lava.update()
        for lava in self.lavaBlock:
            lava.update()
            

    def broadcast_to_client(self, client):  
        self.loopLava()
        gameState = {
            'Players':self.players,
            'Lava':self.lavaObj,
            'Rope':self.rope,
            'LavaBlock':self.lavaBlock
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
        # player.Gravity()
        # self.checkForBlockCollisions(player)
        # self.lavaCollision()
        if player.action == 'died':
            # Handle idle state if necessary, such as updating a last active timestamp
            pass
        elif pressed_keys == ['idle']:
            player.action = 'idle'
            # Handle idle state if necessary, such as updating a last active timestamp
            pass
        else:
            if "left" in pressed_keys:
                player.move_left()
                player.action = 'run'
                player.direction = 'left'  # Add direction attribute
            if "right" in pressed_keys:
                
                player.move_right()
                player.action = 'run'
                player.direction = 'right'  # Add direction attribute

            if "Jump" in pressed_keys:
                print("Jump in pressed keys")
                player.jump()

    def find_player_by_id(self, client_id):
        for player in self.players:
            if player.id == client_id:
                return player
        return None  # Return None if no matching player is found

    def lavaCollision(self):
            p1 = self.players[0]
            p2 = self.players[1]

            for lava in self.lavaObj:   
                if (p1.y + p1.height >= lava.y or p2.y + p2.height >= lava.y) and abs(p1.y - p2.y) < 1:
                    print("Both playres have touched lava")
                    lava.NoCollision = True
                    for lavaB in self.lavaBlock:
                        lavaB.NoCollision = True
                    p1.action = 'died'
                    p2.action = 'died'
                    p1.jump()
                    p2.jump()
                if p1.y + p1.height >= lava.y or p2.y + p2.height >= lava.y:
                    lava.NoCollision = True
                    for lavaB in self.lavaBlock:
                        lavaB.NoCollision = True
                    if p1.y > p2.y:
                        print(p1.y, p2.y)
                        print("this one")
                        p1.jump()
                        p1.action = 'died'
                    else:
                        p2.jump()
                        print("that one")
                        p2.action = 'died'

                    


    def checkForBlockCollisions(self, player):
        for block in self.platforms:
            if player.rect.colliderect(block.rect):
                # Calculate the collision's depth in each direction
                dx_right = block.rect.right - player.rect.left
                dx_left = player.rect.right - block.rect.left
                dy_bottom = block.rect.bottom - player.rect.top
                dy_top = player.rect.bottom - block.rect.top

                # Find out the minimum amount of overlap
                min_dx = min(dx_right, dx_left)
                min_dy = min(dy_bottom, dy_top)

                # Resolve the collision by moving the player out of the block in the direction of least overlap
                if min_dx < min_dy:
                    # Horizontal collision
                    if dx_right < dx_left:
                        # Collision was on the left
                        player.x += dx_right
                    else:
                        # Collision was on the right
                        player.x -= dx_left
                else:
                    # Vertical collision
                    if dy_bottom < dy_top:
                        # Collision was on the top
                        player.y += dy_bottom
                        
                        # player.landed()  # Call this if you have a method to handle landing logic
                        # print("Player.onGround should be false: ", player.onGround)
                    else:
                        # Collision was on the bottom
                        player.y -= dy_top
                        print("This collision")
                        player.landed()
                        # print("Player.onGround should be false: ", player.onGround)
                        

                player.update_rect()  # Update player's rect with new position


if __name__ == '__main__':
    print("This is correct server file")
    server = Server()
    server.start_server()
