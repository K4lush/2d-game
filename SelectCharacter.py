import pygame
from Button import Button

class SelectCharacter:
    def __init__(self):
        self.character = 'NinjaFrog'
        self.ninja_button = Button(60, 50, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Ninja Frog',
                              font='assets/fonts/SC.ttf')  # Set up button parameters
        self.mask_button = Button(60, 125, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                             text='Mask Dude',
                             font='assets/fonts/SC.ttf')

        self.pink_button = Button(60, 200, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                             text='Pink Man',
                             font='assets/fonts/SC.ttf')  # Set up button parameters
        self.virtual_button = Button(60, 275, 300, 60, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                text='Virtual Guy',
                                font='assets/fonts/SC.ttf')

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def render(self, screen):
        # Draw buttons
        self.ninja_button.draw(screen)
        self.mask_button.draw(screen)
        self.pink_button.draw(screen)
        self.virtual_button.draw(screen)