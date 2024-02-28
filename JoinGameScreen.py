from Button import Button
# from Game import GameState

from text_input import TextInput

from Network import Network
from Server import create_server

import pygame

class JoinGameScreen:
    def __init__(self, client_script):
        self.client_script = client_script
        self.current_state = "MAIN"
        self.switch_state = False
        self.create_server = False
        self.font = pygame.font.Font("assets/fonts/SC.ttf", 30)
        self.join_your_friend = self.font.render("JOIN A GAME", True, (255, 255, 255))
        self.game_name = self.font.render("Rope Runners", True, (255, 255, 255))
        self.ip_label = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label = self.font.render("Enter Port:", True, (255, 255, 255))
        self.join_button = Button(150, 400, 200, 30, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Join Game', font='assets/fonts/SC.ttf')
        # Create TextInput instances *without* initial strings
        self.ip_input = TextInput(450, 190, 150, 50)
        self.port_input = TextInput(450, 290, 150, 50)


        self.return_to_menu = Button(430, 450, 200, 30, color=(207, 185, 151),
                                  highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                  text='Return', font='assets/fonts/SC.ttf')

        self.start_game = Button(150, 100, 200, 30, color=(207, 185, 151),
                                     highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                     text='Start Game', font='assets/fonts/SC.ttf')

        ### Host a game ###
        self.host_game = Button(430, 400, 200, 30, color=(207, 185, 151),
                                  highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                  text='Host Game', font='assets/fonts/SC.ttf')

        self.start_server = Button(150, 450, 200, 30, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                text='Start Server', font='assets/fonts/SC.ttf')

        # Create TextInput instances *without* initial strings
        self.ip_input_Server = TextInput(450, 190, 150, 50)
        self.port_input_Server = TextInput(450, 290, 150, 50)

        self.ip_label_Server = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label_Server = self.font.render("Enter Port:", True, (255, 255, 255))




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



            self.ip_input.update(event)
            self.port_input.update(event)

            self.ip_input_Server.update(event)
            self.port_input_Server.update(event)


    def update(self):
        print(self.current_state)

        if self.create_server:
            ip_address = self.ip_input_Server.get_text()
            port = int(self.port_input_Server.get_text())  # Assuming port input is numerical
            create_server(ip_address, port)
            print("server has been created")

        if self.switch_state:
            # return GameState.CHARACTER_SELECT  # Return the new desired state
            ip_address = self.ip_input.get_text()
            port = int(self.port_input.get_text())  # Assuming port input is numerical
            self.client_script.network = Network(ip_address, port)
            return "MAIN MENU"


    def render(self, screen):
        if self.current_state == "MAIN":
            screen.blit(self.game_name, (270, 100))

            # Draw the buttons
            self.join_button.draw(screen)
            self.host_game.draw(screen)

        elif self.current_state == "JOIN":
            # Draw the input fields
            screen.blit(self.ip_label, (150, 200))
            screen.blit(self.port_label, (150, 300))

            self.ip_input.draw(screen)
            self.port_input.draw(screen)
            self.start_game.draw(screen)
            self.return_to_menu.draw(screen)


        elif self.current_state == "HOST":
            # Draw the labels
            screen.blit(self.ip_label_Server, (150, 200))
            screen.blit(self.port_label_Server, (150, 300))

            # Draw the input fields
            self.ip_input_Server.draw(screen)
            self.port_input_Server.draw(screen)
            self.return_to_menu.draw(screen)
            self.start_server.draw(screen)






