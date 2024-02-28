from Button import Button
# from Game import GameState

from text_input import TextInput
from Network import Network
import text_input
import pygame

class JoinGameScreen:
    def __init__(self, client_script):
        self.client_script = client_script
        self.switch_state = False
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

    def handle_event(self, events):
        for event in events:  # Iterate through the events
            self.ip_input.update(event)
            self.port_input.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.join_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.switch_state = True

    def update(self):
        if self.switch_state:
            # return GameState.CHARACTER_SELECT  # Return the new desired state
            ip_address = self.ip_input.get_text()
            port = int(self.port_input.get_text())  # Assuming port input is numerical
            self.client_script.network = Network(ip_address, port)
            return "MAIN MENU"


    def render(self, screen):
        # Draw the labels
        # screen.blit(self.join_your_friend, (100, 50))
        screen.blit(self.game_name, (270, 100))
        screen.blit(self.ip_label, (150, 200))
        screen.blit(self.port_label, (150, 300))

        # Draw the input fields
        self.ip_input.draw(screen)
        self.port_input.draw(screen)

        # Draw the buttons
        self.join_button.draw(screen)


