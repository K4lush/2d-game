import pygame

class Button:
    def __init__(self, x, y, width, height, text='', color=(73, 73, 73), highlight_color=(189, 189, 189), font_color=(0, 0, 0), font_size=20, font=None, function=None, params=None):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Use SRCALPHA for transparent background
        self.pos = (x, y)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.base_text = text
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.font_color = font_color
        self.font_size = font_size
        # Load custom font, fall back to default if not specified or not found
        try:
            self.font = pygame.font.Font(font, font_size)
        except IOError:
            print(f"Font file {font} not found. Falling back to default font.")
            self.font = pygame.font.Font(None, font_size)
        self.function = function
        self.params = params
        self.width = width
        self.height = height
        self.highlighted = False
        self.shadow_color = (0, 0, 0)  # Shadow color; adjust as needed
        self.shadow_offset = (2, 2)  # Shadow offset; adjust as needed
        self.animation_start_time = pygame.time.get_ticks()
        self.dot_count = 0

    def update(self, mouse):
        self.highlighted = self.rect.collidepoint(mouse)
        # Call animate_text in update to ensure it's checked every frame

    def animate(self):
        self.animate_text()

    def draw(self, window):
        fill_color = self.highlight_color if self.highlighted else self.color
        self.image.fill(fill_color)
        window.blit(self.image, self.pos)
        self.draw_text(window)

    def click(self):
        if self.function:
            self.function(self.params) if self.params else self.function()

    def draw_text(self, window):
        # Draw shadow first if highlighted
        if self.highlighted:
            shadow_text_surface = self.font.render(self.text, True, self.shadow_color)
            shadow_text_rect = shadow_text_surface.get_rect(
                center=(self.width / 2 + self.shadow_offset[0], self.height / 2 + self.shadow_offset[1]))
            window.blit(shadow_text_surface, shadow_text_rect.move(self.pos))

        # Then draw the main text
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
        window.blit(text_surface, text_rect.move(self.pos))

    def animate_text(self):
        # Change the dots in the loading text based on time
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_start_time > 500:  # Change dot every 500 milliseconds
            self.dot_count = (self.dot_count + 1) % 4  # Cycle through 0 to 3
            self.text = self.base_text.rstrip('.') + '.' * self.dot_count  # Update text with new dots
            self.animation_start_time = current_time
