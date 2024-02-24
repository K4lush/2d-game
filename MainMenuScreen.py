from Button import Button
# from Game import GameState

from text_input import TextInput
import text_input
import pygame

class MainMenuScreen:
    def __init__(self):
        self.font = pygame.font.Font('assets/fonts/SC.ttf', 12)
        self.ip_label = self.font.render("Enter IP:", True, (255, 255, 255))
        self.port_label = self.font.render("Enter Port:", True, (255, 255, 255))
        self.join_button = Button(100, 300, 200, 30, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Join Game', font='assets/fonts/SC.ttf')
        # Create TextInput instances *without* initial strings
        self.ip_input = TextInput(100, 50, 200, 30)
        self.port_input = TextInput(100, 100, 200, 30)

    def handle_event(self, event):
        self.ip_input.update(event)
        self.port_input.update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.join_button.rect.collidepoint(pygame.mouse.get_pos()):
                ip_address = self.ip_input.get_text()
                port = int(self.port_input.get_text())  # Assuming port input is numerical
                # Do something with ip_address and port
                print("IP:", ip_address)
                print("Port:", port)


    def update(self):
        if self.join_button.rect.collidepoint(pygame.mouse.get_pos()):
            # return GameState.CHARACTER_SELECT  # Return the new desired state
            pass

    def render(self, screen):
        # Draw the labels
        screen.blit(self.ip_label, (100, 25))
        screen.blit(self.port_label, (100, 75))

        # Draw the input fields
        self.ip_input.draw(screen)
        self.port_input.draw(screen)

        # Draw the buttons
        self.join_button.draw(screen)


