import pygame
import math
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

            # Apply pull to each player if they are not on the ground
            if not self.player1.on_ground:
                self.player1.x += direction_x * pull_amount / 2
                self.player1.y += direction_y * pull_amount / 2
                self.player1.update_rect()

            if not self.player2.on_ground:
                self.player2.x -= direction_x * pull_amount / 2
                self.player2.y -= direction_y * pull_amount / 2
                self.player2.update_rect()

    def draw(self, screen, offset_x=0, offset_y=0):
        # start_pos = (self.player1.x + self.player1.width // 2, self.player1.y + self.player1.height // 2)
        # end_pos = (self.player2.x + self.player2.width // 2, self.player2.y + self.player2.height // 2)
        print(f"Drawing rope with offsets: {offset_x}, {offset_y}")
        start_pos = (self.player1.rect.centerx - offset_x, self.player1.rect.centery - offset_y)
        end_pos = (self.player2.rect.centerx - offset_x, self.player2.rect.centery - offset_y)
        print("BEING DRAWN")
        distance = math.sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2)

        # Dynamic color based on tension
        color_intensity = 255 if distance >= self.max_length else min(255, max(0, 155 + int(distance / 2)))
        rope_color = (color_intensity, color_intensity // 2, 0)

        # Generate Bezier curve points
        curve_points = []
        if distance < self.max_length:
            curve_intensity = max(0, min(50, 100 - (distance / self.max_length) * 100))
            control_point1 = (start_pos[0], start_pos[1] + curve_intensity)
            control_point2 = (end_pos[0], end_pos[1] + curve_intensity)
            for t in range(0, 101, 5):
                t /= 100
                bx = (1 - t) ** 3 * start_pos[0] + 3 * (1 - t) ** 2 * t * control_point1[0] + 3 * (1 - t) * t ** 2 * \
                     control_point2[0] + t ** 3 * end_pos[0]
                by = (1 - t) ** 3 * start_pos[1] + 3 * (1 - t) ** 2 * t * control_point1[1] + 3 * (1 - t) * t ** 2 * \
                     control_point2[1] + t ** 3 * end_pos[1]
                curve_points.append((bx, by))

        # Draw Bezier curve or straight line
        if distance >= self.max_length or len(curve_points) < 2:
            pygame.draw.line(screen, rope_color, start_pos, end_pos, self.thickness)
        else:
            pygame.draw.lines(screen, rope_color, False, curve_points, self.thickness)
