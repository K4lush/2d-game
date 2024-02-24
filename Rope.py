import pygame
import math

class Rope:
    def __init__(self, player1, player2, max_length=150):
        self.player1 = player1
        self.player2 = player2
        self.max_length = max_length

    def get_edge_point(self, player, offset_x, offset_y):
        # Calculate the edge point with given offsets
        edge_x = player.rect.centerx + offset_x
        edge_y = player.rect.centery + offset_y
        return (edge_x, edge_y)

    def update(self):
        # Calculate the distance and vector between players
        dx = self.player1.x - self.player2.x
        dy = self.player1.y - self.player2.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Check if the distance is zero to avoid division by zero during normalization
        if distance == 0:
            return  # Skip this update cycle

        direction = pygame.math.Vector2(dx, dy).normalize()

        # Adjust positions if the distance is greater than max_length
        if distance > self.max_length:
            overlap = distance - self.max_length
            self.player1.x -= direction.x * overlap / 2
            self.player1.y -= direction.y * overlap / 2
            self.player2.x += direction.x * overlap / 2
            self.player2.y += direction.y * overlap / 2

            self.player1.update_rect()
            self.player2.update_rect()

    def draw(self, screen):
        # Calculate attachment points
        start_pos = (self.player1.rect.centerx, self.player1.rect.centery)
        end_pos = (self.player2.rect.centerx, self.player2.rect.centery)

        # Calculate the distance between attachment points
        distance = math.sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2)

        # Determine the curvature based on distance
        curve_intensity = max(0, min(50, 100 - (distance / self.max_length) * 100))

        # Calculate control points for the Bezier curve
        control_point1 = (start_pos[0], start_pos[1] + curve_intensity)
        control_point2 = (end_pos[0], end_pos[1] + curve_intensity)

        # Calculate Bezier curve points
        curve_points = []
        for t in range(0, 101, 5):
            t /= 100
            bx = (1 - t) ** 3 * start_pos[0] + 3 * (1 - t) ** 2 * t * control_point1[0] + 3 * (1 - t) * t ** 2 * \
                 control_point2[0] + t ** 3 * end_pos[0]
            by = (1 - t) ** 3 * start_pos[1] + 3 * (1 - t) ** 2 * t * control_point1[1] + 3 * (1 - t) * t ** 2 * \
                 control_point2[1] + t ** 3 * end_pos[1]
            curve_points.append((bx, by))

        # Dynamic color based on tension
        color_intensity = 255 if distance >= self.max_length else min(255, max(0, 155 + int(distance / 2)))
        rope_color = (color_intensity, color_intensity // 2, 0)  # Reddish color indicates tension

        # Draw Bezier curve or straight line based on the distance
        if distance >= self.max_length:
            pygame.draw.line(screen, rope_color, start_pos, end_pos, 4)  # Draw straight line for fully stretched rope
        else:
            pygame.draw.lines(screen, rope_color, False, curve_points, 4)  # Draw Bezier curve for stretchy rope


        #ok


