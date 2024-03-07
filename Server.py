import pickle
import socket
import time

import pygame
from threading import Thread

from _thread import start_new_thread
import threading

import json

from PlatformObjects import StillObjects
from Player import Player
from Settings import Settings
from MapServer import MapServer
from Lava import Lava
from Flag import Flag
from Arrow import Arrows

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
        player = Player(id, character_name, 'idle', 'right', (200 if id == 0 else 300), 2380, 50, 50,
                        (255, 0, 255 if id == 0 else 255, 200, 255))
        self.server.players.append(player)

        if len(self.server.players) == 2:
            self.server.create_rope_if_needed()

    def game(self):
        try:
            
            self.wait_until_ready()

            # print("WAITING FOR BOTH  CLIENTS TO BE READY")
            # self.wait_until_all_ready()

           
            self.game_loop()
        except Exception as e:
            print(f"Exception in client handler: {e}")
        finally:
            self.disconnect()

    def wait_until_ready(self):
        while not self.ready:
            data = self.server.receive_from_client_state(self)
            state = data['state']
            character = data['character']

            if state == "READY":
                self.add_player(self.id, character)
                self.ready = True
                self.server.players_ready_state[self.id] = True


    ### Needs to be JSON ###
    # def wait_until_all_ready(self):
    #     print(self.server.players_ready_state)
    #     while not all(self.server.players_ready_state):
    #         self.server.broadcast_state_to_client(self.client, "NOT READY")
    #     self.server.broadcast_state_to_client(self.client, "READY")

    def game_loop(self):
        while self.connected:
            self.server.receive_from_client_update(self)

            self.server.broadcast_to_client(self.client)


            # self.server.new_broadcast()

            # time.sleep(0.1)


    def disconnect(self):
        self.connected = False
        self.server.remove_client_handler(self)
        self.client.close()  # Ensure the socket is closed to free up resources


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Change to UDP

        self.lock = threading.Lock()
        self.settings = MapServer()
        self.client_handlers = []
        self.players_ready_state = [None, None]
        self.pressed_keys = {}  # In your server class
        self.Arrows = []
        ### Move to setting class ###
        self.platforms_sent = False
        self.rope_created = False
        self.rope = None
        self.rope_data = None
        self.players = []
        self.lavaBlocks = []
        
        self.lavaData = []
        self.BiglavaBlock = None
        self.lavaColl = False
        self.lavaColl = False
        self.flags = []
        self.CreateLava()
        self.nonBlockingPlatforms = []
        self.platforms = self.create_platform_rects()  # Create platform rects
        self.CreateBigLavaBlock()
        self.createFlag()
        self.playerSprites = self.load_characters_sprites()
        self.createArrows()
        self.twoPlayers = False

        # self.start_server()

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
     

        while True:  # Main combined loop
            client, addr = self.server.accept()
            client_handler = ClientHandler(client, addr, self)
            self.add_client_handler(client_handler)
            start_new_thread(client_handler.game, ())

            # Game logic updates:
            # self.update_game_state()

    def createArrows(self):
        Arrow1 = Arrows(1,250,950,75,75)
        Arrow2 = Arrows(2,550,950,75,75)
        self.Arrows.append(Arrow1)
        self.Arrows.append(Arrow2)



  
    def createFlag(self):
        
        self.flag1 = Flag('flag', 16*32 , (100*32)-75, 75, 75, 'ungotten')
        self.flag2 = Flag('flag', 18*32 , (90*32)-75, 75, 75, 'ungotten')
        self.flag3 = Flag('flag', 10*32 , (80*32)-75, 75, 75, 'ungotten')
        self.flag4 = Flag('flag', 11*32 , (70*32)-75, 75, 75, 'ungotten')
        self.flag5 = Flag('flag', 12*32 , (60*32)-75, 75, 75, 'ungotten')
        self.flag6 = Flag('flag', 13*32 , (50*32)-75, 75, 75, 'ungotten')
        self.flag7 = Flag('flag', 14*32 , (40*32)-75, 75, 75, 'ungotten')
        self.flags.append(self.flag1)
        self.flags.append(self.flag2)
        self.flags.append(self.flag3)
        self.flags.append(self.flag4)
        self.flags.append(self.flag5)
        self.flags.append(self.flag6)
        self.flags.append(self.flag7)

    def add_client_handler(self, client_handler):
        with self.lock:
            self.client_handlers.append(client_handler)

    def remove_client_handler(self, client_handler):
        with self.lock:
            if client_handler in self.client_handlers:
                self.client_handlers.remove(client_handler)
                

    def broadcast_to_client(self, client):

        if self.rope:
            self.rope_data = self.rope.to_json()
          

        block = self.BiglavaBlock.to_json()
        # flags = self.flag.to_json()

       
            

        block = self.BiglavaBlock.to_json()
        

       
        gameState = {
            # 'Players': self.players,
            'Players': [player.to_json() for player in self.players], # Serialize players
            
            

            'Rope': self.rope_data,

            'Lava': [lava.to_json() for lava in self.lavaBlocks],

            'LavaBlock':block,

            'Flag':[flag.to_json() for flag in self.flags],

            'Arrow': [arrow.to_json() for arrow in self.Arrows]
        }


        data = json.dumps(gameState)

       

        client.send(data.encode())

   

    def receive_from_client_update(self, client):
      

        buffer_size = 4096  # Adjust buffer size if needed

        json_data = client.client.recv(buffer_size).decode('utf-8')  # Receive as bytes, decode to string

        data = json.loads(json_data)  # Deserialize JSON string into Python data



        self.update_objects(client.id, data)

    def receive_from_client_state(self, client):
        buffer_size = 4096  # Adjust buffer size if needed
        json_data = client.client.recv(buffer_size).decode('utf-8')  # Receive as bytes, decode to string
        data = json.loads(json_data)  # Deserialize JSON string into Python data

        #print("SERVER: received data (state)", data)
        #print("SERVER: received data (state)", data)

        return data

    def update_objects(self, client_id, pressed_keys):
        player = self.find_player_by_id(client_id)
        self.pressed_keys[client_id] = pressed_keys  # Update which keys this client is pressing
       

        #print("SERVER: Received keys:", pressed_keys, "for player", player.id)  # Enhanced logging
        #print("SERVER: Received keys:", pressed_keys, "for player", player.id)  # Enhanced logging
        
        if player:
            if pressed_keys == ['idle']:
                player.action = 'idle'
            
            if player.collision:
                player.action = 'died'

            # 1. Apply Movement
            if "left" in pressed_keys and not player.collision:
                player.move_left()
                player.action = 'run'
                player.direction = 'left'  # Add direction attribute

            if "right" in pressed_keys and not player.collision:
                player.move_right()
                player.action = 'run'
                player.direction = 'right'  # Add direction attribute

            # print("PLAYER: Ground Flag ", player.on_ground)

            if "up" in self.pressed_keys[client_id] and not player.collision:  # Check if 'up' is being held down
                player.jump()
                player.action = 'run'
            

            # 3. Apply Gravity (conditionally)
            if not player.on_ground:
                player.apply_gravity()

            if len(self.players) == 2:
                self.players[0].twoPlayers = True
                self.players[1].twoPlayers = True

            # # 4. Handle Collisions
            player.handle_collisions(self.platforms)  # Assuming you have a list of platforms
            #player.handlePixelPerfectCollisions(self.platforms, self.playerSprites)
            player.handleLavaCollisions(self.lavaBlocks)
            player.hanldeFlagCollision(self.flags)
            player.updateScore()
           
            # 5. Update Rope (if it exists)
            if self.rope:
                self.rope.update()

           


            
                

            
            # if not self.lavaColl:
            #     for lava in self.lavaBlocks:
            #         lava.update()
            #     self.BiglavaBlock.update()


            if player.collision:
                player.action = 'died'
                self.lavaColl = True

            

            
            

    def find_player_by_id(self, client_id):
        for player in self.players:
            if player.id == client_id:
                return player
        return None  # Return None if no matching player is found


    def CreateBigLavaBlock(self):
        self.BiglavaBlock = Lava(99, -480, 3160, 2000, 2000)

    def CreateLava(self):
        for i in range(10):
            ##each lava width is 48 pixels, so draw every 48 pixels accross screen.
            ## we want to draw them 64*however many blocks depths we have in self.map in order for the lava to spawn at bottom of map
            lava = Lava(i, (i * 160)-480, 3000, 160, 160)
            self.lavaBlocks.append(lava)

    def create_rope_if_needed(self):
        if len(self.players) == 2 and not self.rope_created:
            self.rope = Rope(self.players[0], self.players[1], 200)
            self.rope_created = True

    def create_platform_rects(self):
        platforms = []
        block_width = 34  # The width of each block
        block_height = 34  # The height of each block

        for row_index, row in enumerate(self.settings.map):
            for col_index, cell in enumerate(row):
                if cell == 1:  # 1 represents a block
                    block_rect = pygame.Rect((col_index * block_width)-300, row_index * block_height, block_width,
                                             block_height)
                    platforms.append(block_rect)
                if cell == 3:
                    block_rect = pygame.Rect((col_index * block_width)-300, row_index * block_height, block_width,
                                             block_height)
                    self.nonBlockingPlatforms.append(block_rect)

        return platforms
    
    def load_characters_sprites(self):
        characters = {
            'NinjaFrog': {
                'idle': self.load_animation_frames('NinjaFrog', 'idle', 11),
                'run': self.load_animation_frames('NinjaFrog', 'run', 12),
                'died': self.load_animation_frames('NinjaFrog', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'MaskDude': {
                'idle': self.load_animation_frames('MaskDude', 'idle', 11),
                'run': self.load_animation_frames('MaskDude', 'run', 12),
                'died': self.load_animation_frames('MaskDude', 'died', 7),
                # Add more animations for MaskDude as needed
            },
            'PinkMan': {
                'idle': self.load_animation_frames('PinkMan', 'idle', 11),
                'run': self.load_animation_frames('PinkMan', 'run', 12),
                'died': self.load_animation_frames('PinkMan', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'VirtualGuy': {
                'idle': self.load_animation_frames('VirtualGuy', 'idle', 11),
                'run': self.load_animation_frames('VirtualGuy', 'run', 12),
                'died': self.load_animation_frames('VirtualGuy', 'died', 7),
                # Add more animations for MaskDude as needed
            }
            # Add more characters as needed
        }
        return characters

    def load_animation_frames(self, character_folder, action, num_frames, target_width=50, target_height=50):
        path = f'assets/MainCharacters/{character_folder}/{action}.png'
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (target_width, target_height))  # Scale frame to target size
            frames.append(scaled_frame)

        return frames
    



