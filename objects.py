import pygame
class stillObjects:
    def __init__(self, x, y, width, height, sprite=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.sprite = pygame.transform.scale(sprite, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window, offset_x=0):
        window.blit(self.sprite, (self.x - offset_x, self.y))
