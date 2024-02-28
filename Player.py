import pygame

class Player:
    def __init__(self, id, character, action, direction, x, y, width, height, colour, speed=5):
        self.id = id
        self.character = character
        self.action = action
        self.direction = direction
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.is_jumping = False
        self.on_ground = False  # Initialize the on_ground flag
        self.jump_velocity = 0  # Initialize jump velocity
        self.jump_count = 30  # Adjust this for desired jump height
        self.gravity = 0.8  # Adjust this for desired gravity strength

        print("Player Width:", self.rect.width)
        print("Player Height:", self.rect.height)       

    # In your Player class
    def apply_gravity(self):
        """Makes the player fall downwards if they're not on the ground."""
        if not self.on_ground:
            self.jump_velocity += self.gravity  # Gravity pulls down
            self.y += self.jump_velocity
            self.update_rect()  # Update rect after changing y-position

    def jump(self):
        """Starts a jump if the player is standing on the ground."""
        print("PLAYER: Should be jumping")
        if self.on_ground:
            self.jump_velocity = -15  # Negative velocity means upwards jump
            self.is_jumping = True
            self.on_ground = False
            self.update_rect()  # Update rect after changing y-position

    def handle_collisions(self, platforms):
        """Checks if the player hits the ground (replace 200 with your ground level)."""
        for platform in platforms:
            if self.rect.bottom >= platform.rect.y:
                print("this is player bottom: ",self.rect.bottom)
                print("this is platform top: ",platform.rect.y)
                self.y = platform.rect.y - self.height  # Align player with the ground
                print("AFTER this is player bottom: ",self.rect.bottom)
                print("AFTER this is platform top: ",platform.rect.y)
                self.on_ground = True
                self.jump_velocity = 0  # Stop falling when you hit the ground
            self.update_rect()  # Update rect after changing y-position

    def handleLavaCollisions(self,lavaBLocks):
        pass

    def move_left(self):
        self.x -= self.speed
        self.update_rect()

    def move_right(self):
        self.x += self.speed
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y



