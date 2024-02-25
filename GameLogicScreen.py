import pygame

from AnimatedSprite import AnimatedSprite

class GameLogicScreen:
    def __init__(self):
        self.character_sprites = self.load_characters_sprites()
        self.player_sprites = {}
        self.players = None
        self.rope = None

    def update(self, data):
        print("GameLogicClass: Data Received:", data)  # Enhanced logging

        self.players = data['Players']
        self.rope = data['Rope']

        for player in self.players:
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
    def render(self, screen):
        print(self.players)  # Keep this for debugging
        if self.players:
            for player in self.players:
                sprite_key = f'{player.id}_{player.character}_{player.action}'
                if sprite_key in self.player_sprites:  # Make sure the sprite exists
                    sprite = self.player_sprites[sprite_key]
                    sprite.draw(screen, (player.x, player.y))
        if self.rope:
            self.rope.draw(screen)

    def load_characters_sprites(self):
        characters = {
            'NinjaFrog': {
                'idle': self.load_animation_frames('NinjaFrog', 'idle', 11),
                'run': self.load_animation_frames('NinjaFrog', 'run', 12),
                'died': self.load_animation_frames('NinjaFrog', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'MaskDude': {
                'idle': self.load_animation_frames('MaskDude', 'idle', 11),
                'run': self.load_animation_frames('MaskDude', 'run', 12),
                'died': self.load_animation_frames('MaskDude', 'died', 7),
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

