import pygame

class Rope:
    def __init__(self, player1, player2, max_length, thickness=5, color=(0, 0, 0)):
        self.player1 = player1
        self.player2 = player2
        self.max_length = max_length
        self.thickness = thickness
        self.color = color

    def update(self):
        # 1. Calculate Distance and Direction
        dx = self.player2.x - self.player1.x  # Difference in x coordinates
        dy = self.player2.y - self.player1.y  # Difference in y coordinates
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # 2. Check if rope needs to pull a player
        if distance > self.max_length:
            pull_amount = distance - self.max_length

            # Normalize (calculate direction with magnitude 1)
            if distance > 0:  # Prevent divide-by-zero
                direction_x = dx / distance
                direction_y = dy / distance
            else:
                direction_x = 0
                direction_y = 0

            # Apply pull (assuming equal force on both players for now)
            self.player1.x += direction_x * pull_amount / 2
            self.player1.update_rect()
            self.player2.x -= direction_x * pull_amount / 2
            self.player2.update_rect()

    def draw(self, screen):
        start_pos = (self.player1.x + self.player1.width // 2, self.player1.y + self.player1.height // 2)
        end_pos = (self.player2.x + self.player2.width // 2, self.player2.y + self.player2.height // 2)
        pygame.draw.line(screen, self.color, start_pos, end_pos, self.thickness)
