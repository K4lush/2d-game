import pygame

from AnimatedSprite import AnimatedSprite
from PlatformObjects import StillObjects


class Settings:
    def __init__(self):
        self.map = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]

        self.platforms = []
        self.player_sprites = {}
        self.lava_sprites = {}
        self.create_blocks_from_map()
        self.character_sprites = self.load_characters_sprites()
        self.lavaAnimationFrames = self.load_lava_animations()
        self.lavaBlockSprite = self.loadLavaBlockSprite()
        self.background_image = None  # Add this line to initialize the background image attribute
        self.load_background_image()  # Call the method to load the background image

    def loadLavaBlockSprite(self):
        lavaSheet = pygame.image.load('assets/Terrain/lavaAnimation.png').convert_alpha()
        frame1 = lavaSheet.subsurface((0, 221, 16, 16))
        frame1_scaled = pygame.transform.scale(frame1, (1000, 1000))
        return frame1_scaled




    def load_lava_animations(self):
        lava_sheet = pygame.image.load('assets/Terrain/lavaAnimation.png').convert_alpha()
        frame_width = 16
        frame_height = 16
        num_frames = 4
        frame_offsets = [i * (frame_width + 1) for i in range(num_frames)]

        lava_frames = []
        for offset in frame_offsets:
            frame = lava_sheet.subsurface((offset, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame,
                                                  (frame_width * 3, frame_height * 3))  # Scale frame by a factor of 3
            lava_frames.append(scaled_frame)

        return lava_frames

    def updateLavaSprites(self, lavaBlocks):
        # lava id as key animated sprite instance as value
        for lava in lavaBlocks:
            sprite_key = f'{lava.id}'

            if sprite_key not in self.lava_sprites:
                frames = self.lavaAnimationFrames
                self.lava_sprites[sprite_key] = AnimatedSprite(frames, frame_rate=50)
            sprite = self.lava_sprites[sprite_key]

            sprite.update()

    def updateLavaBlock(self, lavaBlock):

        spriteKey = lavaBlock.id
        if spriteKey not in self.lava_sprites:
            frames = []
            frames.append(self.lavaBlockSprite)

            self.lava_sprites[spriteKey] = AnimatedSprite(frames, frame_rate=50)

    def load_characters_sprites(self):
        characters = {
            'NinjaFrog': {
                'idle': self.load_animation_frames('NinjaFrog', 'idle', 11),
                'run': self.load_animation_frames('NinjaFrog', 'run', 12),
                # 'died': self.load_animation_frames('NinjaFrog', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'MaskDude': {
                'idle': self.load_animation_frames('MaskDude', 'idle', 11),
                'run': self.load_animation_frames('MaskDude', 'run', 12),
                # 'died': self.load_animation_frames('MaskDude', 'died', 7),
                # Add more animations for MaskDude as needed
            },
            'PinkMan': {
                'idle': self.load_animation_frames('PinkMan', 'idle', 11),
                'run': self.load_animation_frames('PinkMan', 'run', 12),
                # 'died': self.load_animation_frames('PinkMan', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'VirtualGuy': {
                'idle': self.load_animation_frames('VirtualGuy', 'idle', 11),
                'run': self.load_animation_frames('VirtualGuy', 'run', 12),
                # 'died': self.load_animation_frames('VirtualGuy', 'died', 7),
                # Add more animations for MaskDude as needed
            }
            # Add more characters as needed
        }
        return characters

    def load_animation_frames(self, character_folder, action, num_frames,
                              scale_factor=2):  # Added scale_factor argument
        path = f'assets/MainCharacters/{character_folder}/{action}.png'
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (
                frame_width * scale_factor, frame_height * scale_factor))  # Scale frame
            frames.append(scaled_frame)

        return frames

    def update_player_sprite(self, players):

        for player in players:
            character = player.character
            action = player.action
            direction = player.direction

            sprite_key = f'{player.id}_{character}_{action}'

            if sprite_key not in self.player_sprites:
                if character in self.character_sprites and action in self.character_sprites[character]:
                    frames = self.character_sprites[character][action]
                    self.player_sprites[sprite_key] = AnimatedSprite(frames, frame_rate=50)
                    if action == 'died':
                        self.player_sprites[sprite_key].frame_rate = 200

                    if direction == 'left':
                        self.player_sprites[sprite_key].set_flipped(True)

            sprite = self.player_sprites[sprite_key]

            # Adjust sprite frame rate for 'died' state only if needed
            if player.action == 'died' and not sprite.died_state_started:
                sprite.frame_rate = 200
                sprite.died_state_started = True
            elif player.action != 'died' and sprite.died_state_started:
                sprite.frame_rate = 50
                sprite.died_state_started = False

                # Conditionally flip the sprite based on direction
            if (direction == 'left' and not sprite.flipped) or \
                    (direction == 'right' and sprite.flipped):
                sprite.set_flipped(direction == 'left')

            sprite.update()
        pass

    def create_blocks_from_map(self):
        """Creates block objects based on the map data."""
        tile_size = 80  # Size of each tile
        # Assuming self.settings.map is a 2D list indicating the type of tile at each position
        for row_index, row in enumerate(self.map):
            for col_index, tile_type in enumerate(row):
                print("PLATFORMS: ", tile_type)
                x = col_index * tile_size
                y = row_index * tile_size
                block = StillObjects(tile_type, x, y, tile_size, tile_size, sprite=None)
                self.platforms.append(block)
        self.assign_sprites_to_platforms()

    def assign_sprites_to_platforms(self):
        """Assigns sprites to platforms based on their block_id."""
        block_sprites = self.load_block_sprites()

        for block in self.platforms:
            if block.id in block_sprites:
                # block_sprite = block_sprites[block.id]
                block_sprite = pygame.transform.scale(block_sprites[block.id], (block.width, block.height))
                block.sprite = block_sprite
                # block.sprite.rect = block.sprite.image.get_rect(topleft=(block.x, block.y))

    def load_block_sprites(self):
        """Loads sprites for different block types."""
        return {
            1: pygame.image.load('assets/Terrain/block1.png').convert_alpha(),
            2: pygame.image.load('assets/Background/Yellow.png').convert_alpha(),
            # 2: pygame.image.load('assets/block2.png').convert_alpha(),
            # ... add more block types and corresponding image paths
        }


    def load_background_image(self):
        # Specify the path to your background image
        background_path = 'assets/Background/Yellow.png' # Replace 'YourBackgroundImage.png' with your actual image file name
        # Load the image and assign it to the background_image attribute
        self.background_image = pygame.image.load(background_path).convert_alpha()  # Use convert_alpha() if your image has transparency; otherwise, just use convert()
        window_size = (800, 600)  # Update these dimensions to match your game window size
        self.background_image = pygame.transform.scale(self.background_image, window_size)