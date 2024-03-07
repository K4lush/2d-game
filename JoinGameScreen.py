from Button import Button
# from Game import GameState

from text_input import TextInput

from Network import Network
from Server import Server
from threading import Thread
from Music import MusicPlayer

import pygame
import random

class JoinGameScreen:
    def __init__(self, client_script):
        self.client_script = client_script
        self.background_image = pygame.image.load('assets/Background/Yellow.png').convert()
        self.dynamic_image = pygame.image.load('assets/Background/Brown.png').convert()
        self.dynamic_image = pygame.transform.scale(self.dynamic_image, (800,600))
        self.background_image = pygame.transform.scale(self.background_image, (800,600))
        self.input_background_color = (0, 0, 0)  # Black background for text input
        self.input_border_color = (255, 255, 255)  # White border for text input
        self.input_border_thickness = 2  # Thickness of the border around the text input

        self.current_state = "MAIN"
        self.switch_state = False
        self.create_server = False
        self.font = pygame.font.Font("assets/fonts/SC.ttf", 40)
        self.join_your_friend = self.font.render("JOIN A GAME", True, (255, 255, 255))
        self.game_name = self.font.render("Rope Runners", True, (255, 255, 255))
        self.game_name_scale = 1.0
        self.game_name_scale_speed = 0.005
        self.game_name_max_scale = 1.1  # max scale factor
        self.game_name_min_scale = 0.9  # min scale factor

        self.ip_label = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label = self.font.render("Enter Port:", True, (255, 255, 255))
        self.join_button = Button(150, 300, 200, 30, color=(207, 185, 151),
                                  highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                  text='Join Game', font='assets/fonts/SC.ttf')
        # Create TextInput instances *without* initial strings
        self.ip_input = TextInput(450, 190, 150, 50)
        self.port_input = TextInput(450, 290, 150, 50)

        self.return_to_menu = Button(150, 400, 200, 50, color=(207, 185, 151),
                                     highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                     text='Return', font='assets/fonts/SC.ttf')

        self.start_game = Button(450, 400, 200, 50, color=(207, 185, 151),
                                 highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                 text='Start Game', font='assets/fonts/SC.ttf')

        ### Host a game ###
        self.host_game = Button(430, 300, 200, 30, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                text='Host Game', font='assets/fonts/SC.ttf')

        self.start_server = Button(400, 400, 200, 50, color=(207, 185, 151),
                                   highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=29,
                                   text='Start Server', font='assets/fonts/SC.ttf')

        self.toggle_music_button = Button(50, 550, 200, 30, color=(207, 185, 151),
                                          highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                          text='Play Music', font='assets/fonts/SC.ttf')

        self.pause_music_button = Button(300, 550, 200, 30, color=(207, 185, 151),
                                         highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                         text='Pause Music', font='assets/fonts/SC.ttf')
        self.play_music_button = Button(530, 550, 200, 30, color=(207, 185, 151),
                                        highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                        text='Keep Playing', font='assets/fonts/SC.ttf')

        self.volume_icon = pygame.image.load('assets/Menu/Buttons/Volume.png').convert_alpha()
        self.volume_icon = pygame.transform.scale(self.volume_icon, (30, 30))  # You can adjust the size as needed
        self.next_icon = pygame.image.load('assets/Menu/Buttons/Next.png').convert_alpha()
        self.next_icon = pygame.transform.scale(self.next_icon, (50, 50))  # Adjust the scale as needed

        self.back_icon = pygame.image.load('assets/Menu/Buttons/Back.png').convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (50, 50))  # Adjust the scale as needed

        self.play_icon = pygame.image.load('assets/Menu/Buttons/Play.png').convert_alpha()
        self.play_icon = pygame.transform.scale(self.play_icon, (50, 50))  # Adjust the scale as needed

        # Add a flag to track the music menu state
        self.show_music_options = False

        # Create TextInput instances *without* initial strings
        self.ip_input_Server = TextInput(450, 190, 150, 50)
        self.port_input_Server = TextInput(450, 290, 150, 50)

        self.ip_label_Server = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label_Server = self.font.render("Enter Port:", True, (255, 255, 255))

        self.music_player = MusicPlayer('Game_music.mp3')
        self.music_player.play_music()  # Add this to test if music plays immediately

        self.characters = self.load_characters_sprites()
        self.moving_sprites = []
        for character_name, animations in self.characters.items():
            for _ in range(1):  # Number of instances for each character
                sprite = {
                    "frames": animations['run'],
                    "frame_index": 0,
                    "position": [random.randint(-100, -50), random.randint(0, 600)],
                    "speed": random.randint(2, 5)
                }
                self.moving_sprites.append(sprite)

        self.server_started_message = ""  # Initially an empty string

    def handle_event(self, events):
        for event in events:  # Iterate through the events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state == "MAIN":
                    if self.join_button.rect.collidepoint(pygame.mouse.get_pos()):
                       
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

                if self.start_server.rect.collidepoint(pygame.mouse.get_pos()):
                    self.create_server = True
                    self.server_started_message = "Server started! Invite your friends to join your game."

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
        self.animate_and_move_sprites()

        self.game_name_scale += self.game_name_scale_speed
        if self.game_name_scale > self.game_name_max_scale or self.game_name_scale < self.game_name_min_scale:
            self.game_name_scale_speed *= -1  # Reverse the scaling direction

        # Server creation logic
        if self.create_server:
            ip_address = self.ip_input_Server.get_text()
            port = int(self.port_input_Server.get_text())

            def start_server_thread():  # Function to start the server in a thread
                self.server = Server(ip_address, port)
                self.server.start_server()

            server_thread = Thread(target=start_server_thread)
            server_thread.start()

            print("Server has been created")
            self.create_server = False  # Reset the flag

        # State switching logic
        if self.switch_state:
            ip_address = self.ip_input.get_text()
            port = int(self.port_input.get_text())
            self.client_script.network = Network(ip_address, port)
            return "MAIN MENU"



    def render(self, screen):
        screen.blit(self.background_image, (0, 0))


        # Your existing rendering code for different states
        if self.current_state == "MAIN":
            # Draw the buttons
            self.join_button.draw(screen)
            self.host_game.draw(screen)
            self.toggle_music_button.draw(screen)
            icon_x = self.toggle_music_button.rect.right + 10  # 10 pixels to the right from the button
            icon_y = self.toggle_music_button.rect.y + (
                    self.toggle_music_button.rect.height - self.volume_icon.get_height()) // 2  # Vertically centered

            # Blit the volume icon onto the screen at the calculated position
            screen.blit(self.volume_icon, (icon_x, icon_y))

            scaled_game_name = pygame.transform.scale(
                self.game_name,
                (int(self.game_name.get_width() * self.game_name_scale),
                 int(self.game_name.get_height() * self.game_name_scale))
            )
            game_name_rect = scaled_game_name.get_rect(center=(400, 100))  # Centered horizontally
            screen.blit(scaled_game_name, game_name_rect.topleft)
            for sprite in self.moving_sprites:
                frame = sprite["frames"][sprite["frame_index"]]
                screen.blit(frame, sprite["position"])

        elif self.current_state == "JOIN":
            screen.blit(self.dynamic_image, (0, 0))
            # Draw the input fields and buttons
            screen.blit(self.ip_label, (150, 200))
            screen.blit(self.port_label, (150, 300))
            self.ip_input.draw(screen)
            self.port_input.draw(screen)
            self.start_game.draw(screen)
            self.return_to_menu.draw(screen)
            icon_x = self.start_game.rect.right + 10  # X position: 10 pixels to the right from the button
            icon_y = self.start_game.rect.y + (
                        self.start_game.rect.height - self.next_icon.get_height()) // 2  # Y position: Vertically centered

            # Blit the next icon onto the screen at the calculated position
            screen.blit(self.next_icon, (icon_x, icon_y))
            # Calculate the icon's position to be beside the "Return" button
            icon_x = self.return_to_menu.rect.left - self.back_icon.get_width() - 10  # X position: 10 pixels to the left from the button
            icon_y = self.return_to_menu.rect.y + (
                        self.return_to_menu.rect.height - self.back_icon.get_height()) // 2  # Y position: Vertically centered

            # Blit the back icon onto the screen at the calculated position
            screen.blit(self.back_icon, (icon_x, icon_y))

        elif self.current_state == "HOST":
            screen.blit(self.dynamic_image, (0, 0))
            # Draw the labels and input fields for hosting
            screen.blit(self.ip_label_Server, (150, 200))
            screen.blit(self.port_label_Server, (150, 300))
            self.ip_input_Server.draw(screen)
            self.port_input_Server.draw(screen)
            self.return_to_menu.draw(screen)
            self.start_server.draw(screen)
            # Calculate the icon's position to be beside the "Return" button
            icon_x = self.return_to_menu.rect.left - self.back_icon.get_width() - 10  # X position: 10 pixels to the left from the button
            icon_y = self.return_to_menu.rect.y + (
                        self.return_to_menu.rect.height - self.back_icon.get_height()) // 2  # Y position: Vertically centered

            # Blit the back icon onto the screen at the calculated position
            screen.blit(self.back_icon, (icon_x, icon_y))
            icon_x = self.start_server.rect.right + 10  # X position: 10 pixels to the right from the button
            icon_y = self.start_server.rect.y + (
                        self.start_server.rect.height - self.play_icon.get_height()) // 2  # Y position: Vertically centered

            # Blit the play icon onto the screen at the calculated position
            screen.blit(self.play_icon, (icon_x, icon_y))
            if self.server_started_message:
                message_font = pygame.font.Font("assets/fonts/SC.ttf", 24)
                message_rendered = message_font.render(self.server_started_message, True, (255, 255, 255))
                message_rect = message_rendered.get_rect(center=(400, 550))  # Adjust the position as needed
                screen.blit(message_rendered, message_rect)

        if self.show_music_options:
            # Draw the buttons as before
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

    def animate_and_move_sprites(self):
        for sprite in self.moving_sprites:
            sprite["frame_index"] = (sprite["frame_index"] + 1) % len(sprite["frames"])
            sprite["position"][0] += sprite["speed"]
            if sprite["position"][0] > 800:  # Reset position when off-screen
                sprite["position"] = [0, random.randint(0, 600)]




