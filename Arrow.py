import pygame

class Arrows(pygame.sprite.Sprite):
    """A class representing a lava object in a game, animated and scalable."""

    def __init__(self, id, x, y, width, height):
        """Initializes the lava object with position, dimensions, animation frames, and scaling factor."""
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
    def to_json(self):
        """
        Serializes the Lava object into a JSON-compatible dictionary.
        """

        return {

            'id':self.id,
            'arrowX': self.x,  # Store player IDs for reference
            'arrowY': self.y,
            'arrowHeight':self.height,
            'arrowWidth':self.width
           
            }
