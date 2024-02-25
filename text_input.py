import pygame

# Colors (you can customize these)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

class TextInput:
    def __init__(self, x, y, w, h, initial_string=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = initial_string
        self.color = BLACK  # Set the text color
        self.font = pygame.font.Font(None, 50)
        self.txt_surface = self.font.render(initial_string, True, (255, 255, 255))  # Initialize here
        self.active = False

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() or event.unicode == '.':
                self.text += event.unicode
            # Update the rendered surface with the new text
            self.txt_surface = self.font.render(self.text, True, self.color)
    def draw(self, screen):
        # Blit the rect.
        # pygame.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))



    def get_text(self):
        return self.text