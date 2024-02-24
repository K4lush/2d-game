import pygame


class AnimatedSprite:
    def __init__(self, images, frame_rate, initially_flipped=False):
        self.original_images = images  # Keep a copy of the original images
        self.images = images[:]  # A list of Pygame surfaces representing the animation frames.
        self.frame_rate = frame_rate  # How many milliseconds each frame should be displayed.
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.flipped = initially_flipped  # Track whether the images are flipped
        self.animation_completed = False

        if self.flipped:
            self.flip_images()  # Flip images if initially set to flipped

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)

    

    def draw(self, surface, position):
        # Draw the current frame of the animation on the given surface.
        frame = self.images[self.current_frame]
        surface.blit(frame, position)

    def flip_images(self, force_flip=False):
        """
        Flip the images horizontally. If force_flip is True, it will force the flip regardless of the current state.
        """
        # Only flip if we haven't already, or if force flipping is requested
        if self.flipped != True or force_flip:
            self.images = [pygame.transform.flip(img, True, False) for img in self.original_images]
            self.flipped = not self.flipped  # Toggle the flipped state
        else:
            # If already flipped and not force flipping, revert to original orientation
            self.images = self.original_images[:]
            self.flipped = False

    def set_flipped(self, flipped):
        """
        Set the flipped state of the sprite. If the new state is different from the current, flip the images.
        """
        if self.flipped != flipped:
            self.flip_images()
