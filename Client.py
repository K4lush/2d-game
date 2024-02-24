import time
from Network import Network
import pickle
from AnimatedSprite import AnimatedSprite
import pygame
from Player import Player
# from Client import Client
from Button import Button
from text_input import TextInput


class Client:
    SCREEN = pygame.display.set_mode((800, 400))
    BG_COLOR = (207, 185, 151)  # Background color

    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.clock = pygame.time.Clock()  # Create a clock object for FPS control
        self.ready = False
        self.font = pygame.font.Font('assets/fonts/SC.ttf', 12)
        self.network = None
        # self.network = Network()
        self.character = 'NinjaFrog' #Default
        self.selected_character_label = Button(0, 0, 300, 60, color=(207, 185, 151),
                                               highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=12,
                                               text=f'Character: {self.character}',
                                               font='assets/fonts/SC.ttf')
        self.platforms = []
        self.platforms_received = False
        self.loading = True
        self.backgroundDrawn = False
        self.last_hovered_character = None
        self.sprites = self.load_characters_sptires()
        self.sprites = {}
        # self.load_terrain_sprites()
        self.character_sprites = self.load_characters_sprites()
        self.lavaBlockSprite = self.loadLavaBlockSprite()
        self.player_sprites = {}
        self.lavas = []
        self.rope = None
        self.current_frame = 0
        self.last_frame_update_time = pygame.time.get_ticks()
        self.run()

    def run(self):
        ip, port = self.interface2_screen()
        self.network = Network(ip, port)
        time.sleep(1)
        self.load_terrain_from_server()
        self.interface_screen()
        # self.loading_screen()
        self.main_game_loop()

    # def join(self, ip, port):
    #     print(ip, port)
    #     self.network = Network(ip, port)

    def interface2_screen(self):
        # Create labels
        ip_label = self.font.render("Enter IP:", True, (255,255,255))
        port_label = self.font.render("Enter Port:", True, (255,255,255))

        join_button = Button(100, 300, 200, 30, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Join Game', font='assets/fonts/SC.ttf')

        # Create TextInput instances *without* initial strings
        ip_input = TextInput(100, 50, 200, 30)
        port_input = TextInput(100, 100, 200, 30)

        # Get the initial time
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            self.SCREEN.fill(self.BG_COLOR)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if join_button.rect.collidepoint(pygame.mouse.get_pos()):
                        ip_address = ip_input.get_text()
                        port = int(port_input.get_text())
                        return ip_address, port

                ip_input.update(event)
                port_input.update(event)
                # join_button.update(event)

            # Drawing loop:
            self.SCREEN.blit(ip_label, (100, 25))
            self.SCREEN.blit(port_label, (100, 75))
            ip_input.draw(self.SCREEN)
            port_input.draw(self.SCREEN)
            join_button.draw(self.SCREEN)

            pygame.display.update()

            # Here's an example of using a timestamp to perform an action after a delay
            # Check if 5000 milliseconds (5 seconds) have passed
            if pygame.time.get_ticks() - start_time > 5000:
                # 5 seconds have passed; you can perform some action here
                # Reset start_time if you want to repeat the action every 5 seconds
                start_time = pygame.time.get_ticks()

    def interface_screen(self):
        start_button = Button(250, 125, 300, 60,color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30, text='Start Game',
                              function=self.start_game, font='assets/fonts/SC.ttf')

        select_character_button = Button(250, 225, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30, text='Select Character',
                            function=self.select_character, font='assets/fonts/SC.ttf')

        # Get the initial time
        start_time = pygame.time.get_ticks()

        while not self.ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                        start_button.click()
                    if select_character_button.rect.collidepoint(pygame.mouse.get_pos()):
                        select_character_button.click()
            self.SCREEN.fill(self.BG_COLOR)

            start_button.update(pygame.mouse.get_pos())
            start_button.draw(self.SCREEN)
            select_character_button.draw(self.SCREEN)
            self.selected_character_label.draw(self.SCREEN)
            pygame.display.flip()

            # Here's an example of using a timestamp to perform an action after a delay
            # Check if 5000 milliseconds (5 seconds) have passed
            if pygame.time.get_ticks() - start_time > 5000:
                # 5 seconds have passed; you can perform some action here
                # Reset start_time if you want to repeat the action every 5 seconds
                start_time = pygame.time.get_ticks()


    def select_character(self):
        ninja_button = Button(60, 50, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30, text='Ninja Frog',
                              font='assets/fonts/SC.ttf')  # Set up button parameters
        mask_button = Button(60, 125, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30, text='Mask Dude',
                             font='assets/fonts/SC.ttf')

        pink_button = Button(60, 200, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Pink Man',
                              font='assets/fonts/SC.ttf')  # Set up button parameters
        virtual_button = Button(60, 275, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                             text='Virtual Guy',
                             font='assets/fonts/SC.ttf')

        return_button = Button(450, 275, 300, 60, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 0), font_size=30,
                                text='Return',
                                font='assets/fonts/SC.ttf')

        # Get the initial time
        start_time = pygame.time.get_ticks()

        character_picked = False
        while not character_picked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ninja_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.character = 'NinjaFrog'
                        self.selected_character_label.text = f'Character: Ninja Frog'  # Update the label text

                    elif mask_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.character = 'MaskDude'
                        self.selected_character_label.text = f'Character: Mask Dude'

                    elif pink_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.character = 'PinkMan'
                        self.selected_character_label.text = f'Character: Pink Man'

                    elif virtual_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.character = 'VirtualGuy'
                        self.selected_character_label.text = f'Character: Virtual Guy'

                    elif return_button.rect.collidepoint(pygame.mouse.get_pos()):
                        character_picked = True

            self.SCREEN.fill(self.BG_COLOR)

            # Draw buttons
            ninja_button.draw(self.SCREEN)
            mask_button.draw(self.SCREEN)
            pink_button.draw(self.SCREEN)
            virtual_button.draw(self.SCREEN)
            return_button.draw(self.SCREEN)
            self.selected_character_label.draw(self.SCREEN)


            # In your select_character method's loop
            ninja_button.update(pygame.mouse.get_pos())
            mask_button.update(pygame.mouse.get_pos())
            pink_button.update(pygame.mouse.get_pos())
            virtual_button.update(pygame.mouse.get_pos())
            return_button.update(pygame.mouse.get_pos())

            # Update the last hovered character based on button highlights
            if ninja_button.highlighted:
                self.last_hovered_character = 'NinjaFrog'
            elif mask_button.highlighted:
                self.last_hovered_character = 'MaskDude'
            elif pink_button.highlighted:
                self.last_hovered_character = 'PinkMan'
            elif virtual_button.highlighted:
                self.last_hovered_character = 'VirtualGuy'

            if self.last_hovered_character:
                self.display_run_animation(self.last_hovered_character)

            pygame.display.flip()

            # Here's an example of using a timestamp to perform an action after a delay
            # Check if 5000 milliseconds (5 seconds) have passed
            if pygame.time.get_ticks() - start_time > 5000:
                # 5 seconds have passed; you can perform some action here
                # Reset start_time if you want to repeat the action every 5 seconds
                start_time = pygame.time.get_ticks()

            self.clock.tick(60)

    def display_run_animation(self, character, scale_factor=3):  # Added scale_factor argument
        frames = self.character_sprites[character]['idle']
        current_time = pygame.time.get_ticks()
        frame_index = (current_time // 50) % len(frames)
        current_frame = frames[frame_index]

        # Scale the current frame
        scaled_frame = pygame.transform.scale(current_frame, (
        current_frame.get_width() * scale_factor, current_frame.get_height() * scale_factor))

        animation_pos = (500, 50)  # Adjust as necessary
        self.SCREEN.blit(scaled_frame, animation_pos)

    def start_game(self):
        # Placeholder for the start game logic
        # So we break out of the loop and proceed to the next one
        self.ready = True

        data = {
            'state': 'READY',
            'character': self.character
        }

        # Update the server the current state
        self.sendToServer(data)


    def loadLavaBlockSprite(self):
        lavaSheet = pygame.image.load('assets/Terrain/lavaAnimation.png').convert_alpha()
        frame1 = lavaSheet.subsurface((0, 221, 16, 16))
        return frame1

    def load_terrain_from_server(self):
        incomingData = self.receiveFromServer()
        if incomingData:
            self.platforms = incomingData
            self.platforms_received = True

    def loading_screen(self):
        loading_button = Button(325, 125, 150, 60, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(8, 15, 15), font_size=30,
                                text='Waiting for other player to join', font='assets/fonts/SC.ttf')

        # Get the initial time
        start_time = pygame.time.get_ticks()

        while self.loading:
            other_player_state = self.receiveFromServer()
            if other_player_state == "READY":
                self.loading = False
            else:

                # Here's an example of using a timestamp to perform an action after a delay
                # Check if 5000 milliseconds (5 seconds) have passed
                if pygame.time.get_ticks() - start_time > 10000:
                    # 5 seconds have passed; you can perform some action here
                    # Reset start_time if you want to repeat the action every 5 seconds
                    start_time = pygame.time.get_ticks()

                self.SCREEN.fill(self.BG_COLOR)
                loading_button.animate()  # This will also animate the text
                loading_button.draw(self.SCREEN)
                pygame.display.flip()
                self.clock.tick(60)


    def main_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Data received from the server (Players Objects)
            Data = self.receiveFromServer()
            # Players rendered on the screen
            self.render(Data)
            
            # Check for input, data is forwarded to the server
            self.handleKeyBoardInput()

            pygame.display.flip()  # Update the full display Surface to the screen
            self.clock.tick(60)  # Cap the game at 60 frames per second

    def idFromServer(self):
        incomingData = self.network.receive()
        if incomingData:
            try:
                incomingData = pickle.loads(incomingData)
                return incomingData
            except pickle.UnpicklingError as e:
                print(f"Error unpickling data: {e}")
        return []

    def receiveFromServer(self):
        incomingData = self.network.receive()

        if incomingData:
            try:
                incomingData = pickle.loads(incomingData)
                return incomingData
            except pickle.UnpicklingError as e:
                print(f"Error unpickling data: {e}")
        return []

    def handleKeyBoardInput(self):
        keys = pygame.key.get_pressed()
        pressed_keys = []
        if keys[pygame.K_LEFT]:
            pressed_keys.append("left")

        if keys[pygame.K_SPACE]:
            pressed_keys.append("jump")

        if keys[pygame.K_RIGHT]:
            pressed_keys.append("right")
        if keys[pygame.K_UP]:
            pressed_keys.append("up")
        if keys[pygame.K_DOWN]:
            pressed_keys.append("down")

        # Send pressed keys if any, else send 'idle'
        self.sendToServer(pressed_keys if pressed_keys else ['idle'])

    def sendToServer(self, data):
        try:
            self.network.send(data)
        except Exception as e:
            print(f"Error sending data to server: {e}")

    def load_animation_frames(self, character_folder, action, num_frames,
                              scale_factor=2):  # Added scale_factor argument
        path = f'assets/MainCharacters/{character_folder}/{action}.png'
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (
            frame_width * scale_factor, frame_height * scale_factor))  # Scale frame
            frames.append(scaled_frame)

        return frames

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
                # 'died': self.load_animation_frames('PinkMan', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'VirtualGuy': {
                'idle': self.load_animation_frames('VirtualGuy', 'idle', 11),
                'run': self.load_animation_frames('VirtualGuy', 'run', 12),
                # 'died': self.load_animation_frames('VirtualGuy', 'died', 7),
                # Add more animations for MaskDude as needed
            }
            # Add more characters as needed
        }
        return characters
    def scale_image(self, image, scale_factor):
        """Scales an image by the given scale factor."""
        return pygame.transform.scale(image, (int(image.get_width() * scale_factor),
                                              int(image.get_height() * scale_factor)))

    def render_sprite(self, obj, sprite_key, frames=None, scale_factor = 3):

        if sprite_key not in self.player_sprites:
            if frames is not None:
                scaled_frames = [self.scale_image(frame, scale_factor) for frame in frames]
                self.player_sprites[sprite_key] = AnimatedSprite(scaled_frames, frame_rate=50)

        sprite = self.player_sprites[sprite_key]
        sprite.update()
        sprite.draw(Client.SCREEN, (obj.x, obj.y))

    def render(self, gameState):
        self.SCREEN.fill(Client.BG_COLOR)  # Fill the screen with background color
        if not self.backgroundDrawn:
            if 2 in self.sprites:
                yellow_background = self.sprites[2]
                block_width = 64
                block_height = 64
                screen_width = 1000
                screen_height = 1000

                # Calculate the number of blocks needed horizontally and vertically
                num_blocks_horizontal = screen_width // block_width
                num_blocks_vertical = screen_height // block_height

                # Loop to draw blocks
                for row in range(num_blocks_vertical):
                    for col in range(num_blocks_horizontal):
                        # Calculate the position of each block
                        x = col * block_width
                        y = row * block_height
                        # Draw the block at the calculated position
                        # You would replace this with your drawing function
                        # pygame.draw.rect(Client.SCREEN, (255, 255, 255), (x, y, block_width, block_height))
                        self.SCREEN.blit(yellow_background, (x, y))  # Draw the yellow background
                #self.backgroundDrawn = True
        # for platform in self.platforms:
        #     blockSprite = pygame.transform.scale(self.sprites[1], (platform.width, platform.height))
        #     platform.sprite = blockSprite
        #     platform.draw(Client.SCREEN)
            

        if 'Players' in gameState:
            players_list = gameState['Players']
            for player in players_list:
                print("this is player.action : ",player.action)
                character = player.character  # Assuming these are attributes sent from the server
                action = player.action
                direction = player.direction  # Assuming direction is also sent from the server


            # Key to identify the unique sprite animation for each player
                sprite_key = f'{player.id}_{character}_{action}'

                if sprite_key not in self.player_sprites:
                    if character in self.character_sprites and action in self.character_sprites[character]:
                        frames = self.character_sprites[character][action]
                        self.player_sprites[sprite_key] = AnimatedSprite(frames, frame_rate=50)
                        if action == 'died':
                            self.player_sprites[sprite_key].frame_rate = 200

                        # Initially flip frames if the direction is 'left'
                        if direction == 'left':
                            self.player_sprites[sprite_key].set_flipped(True)
                else:
                    # Use the set_flipped method to adjust sprite orientation based on the direction
                    needs_flipping = (direction == 'left' and not self.player_sprites[sprite_key].flipped) or \
                                    (direction == 'right' and self.player_sprites[sprite_key].flipped)
                    if needs_flipping:
                        self.player_sprites[sprite_key].set_flipped(direction == 'left')

                sprite = self.player_sprites[sprite_key]
                sprite.update()
                sprite.draw(Client.SCREEN, (player.x, player.y))


        if 'Lava' in gameState:
            lava_objects = gameState['Lava']
            for lavaObj in lava_objects:
                lava_id = lavaObj.id
                lava_frames = self.load_lava_animations()
                lava_sprite_key = f'lava_{lava_id}'

                self.render_sprite(lavaObj, lava_sprite_key, frames=lava_frames)

        if 'LavaBlock' in gameState:
            lavaBlocklist = gameState['LavaBlock']
            lavaBlock = lavaBlocklist[0]
            lavaBlock_id = lavaBlock.id
            lavaFrames = []
            lava_frame = self.lavaBlockSprite
            lavaFrames.append(lava_frame)
            lava_sprite_key = f'lava_{lavaBlock_id}'

            self.render_sprite(lavaBlock, lava_sprite_key, lavaFrames, 50)

        if 'Rope' in gameState:
            rope_object = gameState['Rope']
            if len(players_list) == 2:
               rope_object.draw(Client.SCREEN)




    def load_lava_animations(self):
        lava_sheet = pygame.image.load('assets/Terrain/lavaAnimation.png').convert_alpha()
        frame_width = 16
        frame_height = 16
        num_frames = 4
        frame_offsets = [i * (frame_width + 1) for i in range(num_frames)]

        lava_frames = []
        for offset in frame_offsets:
            frame = lava_sheet.subsurface((offset, 0, frame_width, frame_height))
            lava_frames.append(frame)

        return lava_frames


    def load_terrain_sprites(self):
        sprite_sheet = pygame.image.load('assets/Terrain/Terrain.png').convert_alpha()
        frame = sprite_sheet.subsurface((96, 64, 48, 48))
        # Populate self.sprites dictionary
        self.sprites = {
            1: frame,
            2: pygame.image.load('assets/Background/Yellow.png').convert_alpha(),
        }


    def load_characters_sptires(self):
        def load_animation_frames(character_folder, action, num_frames):
            path = f'assets/MainCharacters/{character_folder}/{action}.png'
            sprite_sheet = pygame.image.load(path).convert_alpha()
            frame_width = sprite_sheet.get_width() // num_frames
            frame_height = sprite_sheet.get_height()

            frames = []
            for i in range(num_frames):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                scaled_frame = pygame.transform.scale(frame, (50, 50))
                frames.append(scaled_frame)

            return frames

        characters = {
            'NinjaFrog': {
                'idle': load_animation_frames('NinjaFrog', 'idle', 11),
                'run': load_animation_frames('NinjaFrog', 'run', 12),
                'died': load_animation_frames('NinjaFrog', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'MaskDude': {
                'idle': load_animation_frames('MaskDude', 'idle', 11),
                'run': load_animation_frames('MaskDude', 'run', 12),
                'died': load_animation_frames('MaskDude', 'died', 7),
                # Add more animations for MaskDude as needed
            }
        }

        return characters

if __name__ == "__main__":
    client = Client()
