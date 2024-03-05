import pygame


class Flag(pygame.sprite.Sprite):
    """A class representing a lava object in a game, animated and scalable."""

    def __init__(self, id, x, y, width, height, action, collision=False):
        """Initializes the lava object with position, dimensions, animation frames, and scaling factor."""
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collision = collision
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)
        

    def to_json(self):
        """
        Serializes the Lava object into a JSON-compatible dictionary.
        """

        return {
            'id': self.id,  # Store player IDs for reference
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'action': self.action,
            'collision':self.collision

           
            }