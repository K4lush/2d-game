from Button import Button
# from Game import GameState

from text_input import TextInput

from Network import Network
from Server import Server
from threading import Thread
from Music import MusicPlayer


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






