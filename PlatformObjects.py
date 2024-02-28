import pygame
class StillObjects:
    def __init__(self, id, x, y, width, height, collision=False, sprite=None):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collision = collision  # Typo Fix: collision, not collsion
        self.sprite = sprite
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, position, offset_x=0, offset_y=0):
        if self.sprite:
            screen.blit(self.sprite, position)
            # screen.blit(self.sprite, position, pygame.Rect(self.x - offset_x, self.y - offset_y, sprite_width, sprite_height))  # Draw if a sprite is assigned