from Button import Button
# from Game import GameState

from text_input import TextInput

from Network import Network
from Server import Server
from threading import Thread
from Music import MusicPlayer
from Rope import Rope

import pygame

class JoinGameScreen:
    def __init__(self, client_script):
        self.client_script = client_script
        self.background_image = pygame.image.load('assets/Background/Yellow.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (800,600))
        self.current_state = "MAIN"
        self.switch_state = False
        self.create_server = False
        self.font = pygame.font.Font("assets/fonts/SC.ttf", 30)
        self.join_your_friend = self.font.render("JOIN A GAME", True, (255, 255, 255))
        self.game_name = self.font.render("Rope Runners", True, (255, 255, 255))
        self.ip_label = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label = self.font.render("Enter Port:", True, (255, 255, 255))
        self.join_button = Button(150, 300, 200, 30, color=(207, 185, 151),
                                  highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                  text='Join Game', font='assets/fonts/SC.ttf')
        # Create TextInput instances *without* initial strings
        self.ip_input = TextInput(450, 190, 150, 50)
        self.port_input = TextInput(450, 290, 150, 50)

        self.return_to_menu = Button(430, 250, 200, 30, color=(207, 185, 151),
                                     highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                     text='Return', font='assets/fonts/SC.ttf')

        self.start_game = Button(150, 250, 200, 30, color=(207, 185, 151),
                                 highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                 text='Start Game', font='assets/fonts/SC.ttf')

        ### Host a game ###
        self.host_game = Button(430, 300, 200, 30, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                text='Host Game', font='assets/fonts/SC.ttf')

        self.start_server = Button(430, 350, 200, 30, color=(207, 185, 151),
                                   highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                   text='Start Server', font='assets/fonts/SC.ttf')

        self.toggle_music_button = Button(150, 350, 200, 30, color=(207, 185, 151),
                                          highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                          text='Toggle Music', font='assets/fonts/SC.ttf')

        self.pause_music_button = Button(150, 390, 200, 30, color=(207, 185, 151),
                                         highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                         text='Pause Music', font='assets/fonts/SC.ttf')
        self.play_music_button = Button(150, 430, 200, 30, color=(207, 185, 151),
                                        highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                        text='Keep Playing', font='assets/fonts/SC.ttf')

        # Add a flag to track the music menu state
        self.show_music_options = False

        # Create TextInput instances *without* initial strings
        self.ip_input_Server = TextInput(450, 190, 150, 50)
        self.port_input_Server = TextInput(450, 290, 150, 50)

        self.ip_label_Server = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label_Server = self.font.render("Enter Port:", True, (255, 255, 255))

        self.music_player = MusicPlayer('Game_music.mp3')
        self.music_player.play_music()  # Add this to test if music plays immediately
        self.character_sprites = self.load_characters_sprites()
        self.rope_color = (255, 255, 255)  # White color for the rope
        self.rope_width = 5  # Width of the rope

        # Load characters sprites (NinjaFrog and MaskDude)
        self.ninja_frog_sprite = self.character_sprites['NinjaFrog']['idle'][0]  # First frame of idle animation
        self.mask_dude_sprite = self.character_sprites['MaskDude']['idle'][0]  # First frame of idle animation

        # Sprite positions (adjust as needed)
        self.ninja_frog_pos = (100, 200)  # (x, y) coordinates
        self.mask_dude_pos = (300, 200)  # (x, y) coordinates

        self.ninja_frog_frame = 0
        self.mask_dude_frame = 0

        # Sprite starting positions
        self.ninja_frog_pos = [100, 200]
        self.mask_dude_pos = [300, 200]

        # Movement speed
        self.sprite_speed = 2

    def handle_event(self, events):
        for event in events:  # Iterate through the events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state == "MAIN":
                    if self.join_button.rect.collidepoint(pygame.mouse.get_pos()):
                        print("Changing state to JOIN")
                        self.current_state = "JOIN"
                    if self.host_game.rect.collidepoint(pygame.mouse.get_pos()):
                        self.current_state = "HOST"

                if self.current_state == "JOIN":
                    if self.return_to_menu.rect.collidepoint(pygame.mouse.get_pos()):
                        self.current_state = "MAIN"
                    if self.start_game.rect.collidepoint(pygame.mouse.get_pos()):
                        self.switch_state = True

                if self.current_state == "HOST":
                    if self.return_to_menu.rect.collidepoint(pygame.mouse.get_pos()):
                        self.current_state = "MAIN"
                    if self.start_server.rect.collidepoint(pygame.mouse.get_pos()):
                        self.create_server = True


                if self.toggle_music_button.rect.collidepoint(pygame.mouse.get_pos()):
                    # Toggle the display of music options
                    self.show_music_options = not self.show_music_options

                    # Check whether the music options are shown
                if self.show_music_options:
                    if self.pause_music_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # Pause the music only if it's currently playing
                        if self.music_player.is_playing:
                            self.music_player.pause_music()

                    if self.play_music_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # Play the music only if it's currently paused
                        if not self.music_player.is_playing:
                            self.music_player.unpause_music()


            self.ip_input.update(event)
            self.port_input.update(event)
            self.ip_input_Server.update(event)
            self.port_input_Server.update(event)



    def update(self):
        # print(self.current_state)
        # Update the positions of the sprites
        self.ninja_frog_pos[0] += self.sprite_speed
        self.mask_dude_pos[0] += self.sprite_speed

        # Wrap around the screen if they go off the edge
        screen_width = 800  # Assuming your screen width is 800
        if self.ninja_frog_pos[0] > screen_width:
            self.ninja_frog_pos[0] = -self.character_sprites['NinjaFrog']['run'][0].get_width()
        if self.mask_dude_pos[0] > screen_width:
            self.mask_dude_pos[0] = -self.character_sprites['MaskDude']['run'][0].get_width()

        # Update animation frames
        current_time = pygame.time.get_ticks()
        if current_time % 50 == 0:  # Change frame every 50 milliseconds
            self.ninja_frog_frame = (self.ninja_frog_frame + 1) % len(self.character_sprites['NinjaFrog']['run'])
            self.mask_dude_frame = (self.mask_dude_frame + 1) % len(self.character_sprites['MaskDude']['run'])

        if self.create_server:
            ip_address = self.ip_input_Server.get_text()
            port = int(self.port_input_Server.get_text())

            def start_server_thread():  # Create a function to start the server in a thread
                self.server = Server(ip_address, port)
                self.server.start_server()  # Start the server (which internally handles client connections)

            server_thread = Thread(target=start_server_thread)
            server_thread.start()

            print("Server has been created")
            self.create_server = False  # Reset the flag

        if self.switch_state:
            # return GameState.CHARACTER_SELECT  # Return the new desired state
            ip_address = self.ip_input.get_text()
            port = int(self.port_input.get_text())  # Assuming port input is numerical
            self.client_script.network = Network(ip_address, port)
            return "MAIN MENU"

    def render(self, screen):
        screen.blit(self.background_image, (0, 0))



        # Your existing rendering code for different states
        if self.current_state == "MAIN":
            screen.blit(self.game_name, (270, 100))
            # Draw the buttons
            self.join_button.draw(screen)
            self.host_game.draw(screen)
            self.toggle_music_button.draw(screen)
            ninja_frog_current_frame = self.character_sprites['NinjaFrog']['run'][self.ninja_frog_frame]
            mask_dude_current_frame = self.character_sprites['MaskDude']['run'][self.mask_dude_frame]

            # Draw the rope connecting the sprites
            rope_end_pos = (self.mask_dude_pos[0] + mask_dude_current_frame.get_width() // 2, self.mask_dude_pos[1])
            pygame.draw.line(screen, self.rope_color, self.ninja_frog_pos, rope_end_pos, self.rope_width)

            # Draw the sprites
            screen.blit(ninja_frog_current_frame, self.ninja_frog_pos)
            screen.blit(mask_dude_current_frame, self.mask_dude_pos)


        elif self.current_state == "JOIN":
            # Draw the input fields and buttons
            screen.blit(self.ip_label, (150, 200))
            screen.blit(self.port_label, (150, 300))
            self.ip_input.draw(screen)
            self.port_input.draw(screen)
            self.start_game.draw(screen)
            self.return_to_menu.draw(screen)

        elif self.current_state == "HOST":
            # Draw the labels and input fields for hosting
            screen.blit(self.ip_label_Server, (150, 200))
            screen.blit(self.port_label_Server, (150, 300))
            self.ip_input_Server.draw(screen)
            self.port_input_Server.draw(screen)
            self.return_to_menu.draw(screen)
            self.start_server.draw(screen)

        if self.show_music_options:
            # Always draw both buttons when music options are shown
            self.pause_music_button.draw(screen)
            self.play_music_button.draw(screen)


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





