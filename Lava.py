import pygame

class Lava(pygame.sprite.Sprite):
    """A class representing a lava object in a game, animated and scalable."""

    def __init__(self, id, x, y, width, height,speed=1):
        """Initializes the lava object with position, dimensions, animation frames, and scaling factor."""
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.NoCollision = False
        self.image = None

    def update(self):
        if not self.NoCollision:
            self.y -= 0.2
        self.rect.y = self.y

    