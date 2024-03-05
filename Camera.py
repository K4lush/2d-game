import pygame

class Camera:
    def __init__(self, width, height, screen_width, screen_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, entity):
        # Check if the entity is a pygame.Rect or has a rect attribute
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        else:
            return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # debugging
    

        # Center the camera on the target
        x = -target.rect.x + int(self.screen_width / 2)
        y = -target.rect.y + int(self.screen_height / 2)

        # Applying boundaries to keep the camera within the bounds of the game world
        # For x: making sure camera does not go past the left or right bounds of the game world
        x = max(-(self.width - self.screen_width), min(0, x))

        # For y: making sure camera stays above a certain level, and does not go below the game world
        min_y = -(self.height - self.screen_height)  # The lowest the camera can go
        max_y_above_platform = max(min_y, -target.rect.y + self.screen_height - 550)  #  550  distance above the platform
        y = max(min_y, min(y, max_y_above_platform))

        # Set the camera position
        self.camera = pygame.Rect(x, y, self.width, self.height)

        # Printing out final camera position
       

    def apply_rect(self, rect):
        # This method shifts a rectangle by the camera offset.
        return rect.move(self.camera.topleft)
