
import pygame

from Button import Button


class GameOverScreen:
    def __init__(self):
        self.background_image = pygame.image.load('assets/Background/Yellow.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (800,600))
        self.restart_button = Button(150, 300, 200, 30, color=(207, 185, 151),
                                  highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                  text='Restart', font='assets/fonts/SC.ttf')

        self.switch_state = False
    def handle_event(self, events):
        for event in events:  # Iterate through the events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.switch_state = True
    def update(self):
        if self.switch_state:
            self.switch_state = False
            return "JOIN MENU"

    def render(self, screen):
        screen.blit(self.background_image, (0, 0))
        self.restart_button.draw(screen)
