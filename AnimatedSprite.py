import pygame


class AnimatedSprite:
    def __init__(self, images, frame_rate, initially_flipped=False):
        self.original_images = images
        self.images = images[:]
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.flipped = initially_flipped
        self.died_state_started = False  # Initialize the 'died' state tracker
        self.animation_completed = False

        if self.flipped:
            self.flip_images()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, surface, position):
        frame = self.images[self.current_frame]
        surface.blit(frame, position)

    def flip_images(self, force_flip=False):
        if self.flipped != True or force_flip:
            self.images = [pygame.transform.flip(img, True, False) for img in self.original_images]
            self.flipped = not self.flipped
        else:
            self.images = self.original_images[:]
            self.flipped = False

    def set_flipped(self, flipped):
        if self.flipped != flipped:
            self.flip_images()