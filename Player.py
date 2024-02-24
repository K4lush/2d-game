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
        self.jumpHeight = 6
        self.jumpVelocity = self.jumpHeight
        self.is_jumping = False
        self.onGround = False
        self.gravity = .05


    def playerCollisions(self):
        pass

    def draw(self, screen):
        if self.current_sprite:
            screen.blit(self.current_sprite, (self.x, self.y))

    def jump(self):
        print("Jumping method called")
        print(self.is_jumping, self.onGround)
        if not self.is_jumping and self.onGround:
            self.y -= 30
            self.is_jumping = True
            self.onGround = False

    def move_left(self):
        self.x -= self.speed
        self.update_rect()

    def move_right(self):
        self.x += self.speed
        self.update_rect()

    def Gravity(self):
        if self.is_jumping:
            if self.jumpVelocity >= -self.jumpHeight:
                neg = 1
                if self.jumpVelocity < 0:
                    neg = -1
                self.y -= (self.jumpVelocity ** 2) * 0.5 * neg
                self.jumpVelocity -= 1
            else:
                self.is_jumping = False
                self.jumpVelocity = self.jumpHeight
        else:
            self.y += self.gravity
            self.gravity += 0.5
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def landed(self):
        self.onGround = True
        self.is_jumping = False
        self.gravity = 1

