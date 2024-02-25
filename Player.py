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
        self.jump_count = 10  # Adjust this for desired jump height
        self.gravity = 5  # Adjust this for desired gravity strength

    # In your Player class
    def apply_gravity(self):
        if self.is_jumping:
            self.jump_velocity += self.gravity * 0.5  # Smoother gravity
            self.y += self.jump_velocity

            # Check if the jump has ended
            if self.jump_velocity > 0:
                self.is_jumping = False

    def jump(self):
        print("PLAYER: Should be jumping")
        if self.on_ground:
            self.jump_velocity = -14  # Adjust jump strength as needed
            self.is_jumping = True
            self.on_ground = False

    def handle_collisions(self):
        # Resetting on_ground after collisions
        if self.rect.bottom >= 350:
            self.y = 350 - self.height
            self.on_ground = True
            self.jump_velocity = 0  # Reset jump velocity

    def move_left(self):
        self.x -= self.speed
        self.update_rect()

    def move_right(self):
        self.x += self.speed
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y



