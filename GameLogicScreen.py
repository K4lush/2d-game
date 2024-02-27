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

    def render(self, screen):
        for block in self.settings.platforms:
            if block.sprite:  # Ensure a sprite is assigned
                block.draw(screen, (block.x, block.y))

        print(self.players)  # Keep this for debugging
        if self.players:
            for player in self.players:
                sprite_key = f'{player.id}_{player.character}_{player.action}'
                if sprite_key in self.settings.player_sprites:  # Make sure the sprite exists
                    sprite = self.settings.player_sprites[sprite_key]
                    sprite.draw(screen, (player.x, player.y))
        if self.rope:
            self.rope.draw(screen)
        if self.lavaBlocks:
            for lava in self.lavaBlocks:
                sprite_key = f'{lava.id}'
                if sprite_key in self.settings.lava_sprites:
                    sprite = self.settings.lava_sprites[sprite_key]
                    sprite.draw(screen, (lava.x, lava.y))
        if self.BigLavaBlock is not None:
            key = self.BigLavaBlock.id
            if key in self.settings.lava_sprites:
                sprite = self.settings.lava_sprites[key]
                sprite.draw(screen, (self.BigLavaBlock.x, self.BigLavaBlock.y))
                print("It should be drawn")














