import pygame
import pickle
from Lava import Lava
from Settings import Settings


# from AnimatedSprite import AnimatedSprite

class GameLogicScreen:
    def __init__(self):
        self.settings = Settings()
        self.players = None
        self.rope = None
        self.lavaBlocks = []
        self.BigLavaBlock = None

    def handle_event(self, keys):
        pressed_keys = []

        if keys[pygame.K_LEFT]:
            pressed_keys.append("left")

        if keys[pygame.K_RIGHT]:
            pressed_keys.append("right")

        if keys[pygame.K_UP]:
            pressed_keys.append("up")

        if keys[pygame.K_DOWN]:
            pressed_keys.append("down")

        # Send pressed keys if any, else send 'idle'
        return pressed_keys if pressed_keys else ['idle']

    def update(self, data):
        print("GameLogicClass: Data Received:", data)  # Enhanced logging

        self.players = data['Players']

        self.rope = data['Rope']

        if 'Lava' in data:
            self.lavaBlocks = data['Lava']
        if 'LavaBlock' in data:
            self.BigLavaBlock = data['LavaBlock']

            print(self.BigLavaBlock)
            self.settings.updateLavaBlock(self.BigLavaBlock)

        self.settings.update_player_sprite(self.players)
        self.settings.updateLavaSprites(self.lavaBlocks)



    def calculate_camera_offset(self, players):
        # Constants for game window dimensions - adjust as necessary
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

        if players and len(players) >= 2:
            # Calculate midpoint between the players
            mid_x = (players[0].x + players[1].x) / 2
            mid_y = (players[0].y + players[1].y) / 2

            # Calculate camera offset to center on midpoint
            camera_offset_x = mid_x - WINDOW_WIDTH / 2
            camera_offset_y = mid_y - WINDOW_HEIGHT / 2
        else:
            camera_offset_x, camera_offset_y = 0, 0

        # Optional: Clamp the camera_offset values to ensure the camera doesn't move outside your game world bounds
        # Example clamping (adjust with your game's actual bounds):
        # camera_offset_x = max(0, min(camera_offset_x, GAME_WORLD_WIDTH - WINDOW_WIDTH))
        # camera_offset_y = max(0, min(camera_offset_y, GAME_WORLD_HEIGHT - WINDOW_HEIGHT))

        return camera_offset_x, camera_offset_y

    def render(self, screen):
        camera_offset_x, camera_offset_y = self.calculate_camera_offset(self.players)
        if self.settings.background_image:
            screen.blit(self.settings.background_image, (0, 0))

        for block in self.settings.platforms:
            if block.sprite:  # Ensure a sprite is assigned
                block.draw(screen, (block.x - camera_offset_x, block.y - camera_offset_y))



        print(self.players)  # Keep this for debugging
        if self.players:
            for player in self.players:
                sprite_key = f'{player.id}_{player.character}_{player.action}'
                if sprite_key in self.settings.player_sprites:  # Make sure the sprite exists
                    sprite = self.settings.player_sprites[sprite_key]
                    sprite.draw(screen, (player.x - camera_offset_x, player.y - camera_offset_y))
                    # sprite.draw(800, 400, (player.x, player.y), offset_x=+camera_offset_x,
                    #             offset_y=+camera_offset_y)
        if self.rope:
            # self.rope.draw(800, 400, (self.rope.x, self.rope.y), offset_x=+camera_offset_x, offset_y=+camera_offset_y)
            # self.rope.draw(screen, (self.rope.x - camera_offset_x, self.rope.y - camera_offset_y))

            self.rope.draw(screen, camera_offset_x, camera_offset_y)
        if self.lavaBlocks:
            for lava in self.lavaBlocks:
                sprite_key = f'{lava.id}'
                if sprite_key in self.settings.lava_sprites:
                    sprite = self.settings.lava_sprites[sprite_key]
                    sprite.draw(screen, (lava.x - camera_offset_x, lava.y - camera_offset_y))
                    # sprite.draw(screen, (lava.x - camera_offset_x, lava.y - camera_offset_y))
        if self.BigLavaBlock is not None:
            key = self.BigLavaBlock.id
            if key in self.settings.lava_sprites:
                sprite = self.settings.lava_sprites[key]
                # sprite.draw(screen, (self.BigLavaBlock.x - camera_offset_x, self.BigLavaBlock.y - camera_offset_y))
                sprite.draw(screen, (self.BigLavaBlock.x - camera_offset_x, self.BigLavaBlock.y - camera_offset_y))

                print("It should be drawn")














