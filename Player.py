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
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform):
                collision_side = self.get_collision_side(platform)
                print(f"Collision detected on {collision_side}")  # Debugging print

                if collision_side == "bottom":
                    self.y = platform.top - self.height
                    self.on_ground = True
                    self.jump_velocity = 0

                elif collision_side == "top":
                    self.y = platform.bottom
                    self.jump_velocity = 0

                elif collision_side == "left":
                    self.x = platform.right

                elif collision_side == "right":
                    self.x = platform.left - self.width

        self.update_rect()

    def get_collision_side(self, platform):
        # Calculate the sides of the player and the platform
        player_bottom = self.rect.bottom
        player_top = self.rect.top
        player_left = self.rect.left
        player_right = self.rect.right

        platform_bottom = platform.bottom
        platform_top = platform.top
        platform_left = platform.left
        platform_right = platform.right

        # Calculate the difference between each side
        bottom_diff = abs(player_bottom - platform_top)
        top_diff = abs(player_top - platform_bottom)
        left_diff = abs(player_left - platform_right)
        right_diff = abs(player_right - platform_left)

        # Find the minimum difference to determine the collision side
        min_diff = min(bottom_diff, top_diff, left_diff, right_diff)

        if min_diff == bottom_diff:
            return 'bottom'
        elif min_diff == top_diff:
            return 'top'
        elif min_diff == left_diff:
            return 'left'
        elif min_diff == right_diff:
            return 'right'

    def get_collision_direction(self, platform):
        # Determine the direction of the collision
        # This is a simple approach and might need refinement based on your game's specifics
        if self.rect.bottom >= platform.top and self.rect.bottom - self.speed <= platform.top:
            return 'bottom'
        elif self.rect.top <= platform.bottom and self.rect.top + self.speed >= platform.bottom:
            return 'top'
        elif self.rect.left <= platform.right and self.rect.left + self.speed >= platform.right:
            return 'left'
        elif self.rect.right >= platform.left and self.rect.right - self.speed <= platform.left:
            return 'right'
    #Helo

    def update_position_from_rect(self):
        # Update the player's position based on the rect
        self.x = self.rect.x
        self.y = self.rect.y
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



