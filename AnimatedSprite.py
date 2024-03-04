import pygame


class AnimatedSprite:
    
    def __init__(self, images, frame_rate, initially_flipped=False, lava=None):
        self.original_images = images
        self.images = images[:]
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.flipped = initially_flipped
        self.lava = lava    
        self.lava = lava    
        self.died_state_started = False  # Initialize the 'died' state tracker
        self.animation_completed = False
        self.completed_once = False
        self.flagDone = False

        if self.flipped:
            self.flip_images()

    
    def update(self, action=None):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            print("this is action: ",action)
            if action == 'died':
                    print("Action is died in sprite class")
                    if self.died_state_started and not self.completed_once:
                        self.animation_completed = True
                        self.completed_once = True
                        print("game over in animated sprite class", self.completed_once)
            if action == 'gotten':
                if self.current_frame == len(self.images):
                    self.flagDone = True

   
    def draw(self, surface, position, offset_x=0, offset_y=0):
        print(offset_y, offset_x)
        # print(f"Drawing AnimatedSprite at position: {position} with offset: ({offset_x}, {offset_y})")
        # Apply the offset to the position
        # if self.lava is None:
        #     offset_position = (position[0] - offset_x, position[1] - offset_y)
        # elif self.lava is not None:
        #     offset_position = (self.lava[0] - offset_x, self.lava[1] - offset_y)
        # if self.lava is None:
        #     offset_position = (position[0] - offset_x, position[1] - offset_y)
        # elif self.lava is not None:
        #     offset_position = (self.lava[0] - offset_x, self.lava[1] - offset_y)
        offset_position = (position[0] - offset_x, position[1] - offset_y)
        # Draw the current frame of the animation on the given surface.
        frame = self.images[self.current_frame]
        surface.blit(frame, offset_position)
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