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
        self.rect = pygame.Rect(x, y, width, height)  # Create the rect attribute

        print("Block Width:", self.rect.width)
        print("Block Height:", self.rect.height) 

    def draw(self, screen, position):
        if self.sprite:
            screen.blit(self.sprite, position)  # Draw if a sprite is assigned