from Button import Button
# from Game import GameState

import pygame

from text_input import TextInput
from Button import Button


class MainMenuScreen:
    def __init__(self):
        # Default Character if no character is chosen
        self.character = 'NinjaFrog'
        self.screen = None
        self.character_sprites = self.load_characters_sprites()
        self.last_hovered_character = None
        self.current_state = "MAIN"
        self.ninja_button = Button(60, 50, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Ninja Frog',
                              font='assets/fonts/SC.ttf')  # Set up button parameters
        self.mask_button = Button(60, 125, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                             text='Mask Dude',
                             font='assets/fonts/SC.ttf')

        self.pink_button = Button(60, 200, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                             text='Pink Man',
                             font='assets/fonts/SC.ttf')  # Set up button parameters
        self.virtual_button = Button(60, 275, 300, 60, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                text='Virtual Guy',
                                font='assets/fonts/SC.ttf')

        self.return_button = Button(450, 275, 300, 60, color=(207, 185, 151),
                               highlight_color=(207, 185, 151), font_color=(255, 255, 0), font_size=30,
                               text='Return',
                               font='assets/fonts/SC.ttf')
        self.start_button = Button(250, 125, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                              text='Start Game',
                             font='assets/fonts/SC.ttf')

        self.select_character_button = Button(250, 225, 300, 60, color=(207, 185, 151),
                                         highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=30,
                                         text='Select Character',
                                        font='assets/fonts/SC.ttf')

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("THIS IS EVENT", event)

                if self.ninja_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'NinjaFrog'

                elif self.mask_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'MaskDude'

                elif self.pink_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'PinkMan'

                elif self.virtual_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'VirtualGuy'

                elif self.select_character_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.current_state = "SHOW CHARACTER"

                elif self.return_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.current_state = "MAIN"



    def update(self):
        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
            return "PLAYING"

        # In your select_character method's loop
        self.ninja_button.update(pygame.mouse.get_pos())
        self.mask_button.update(pygame.mouse.get_pos())
        self.pink_button.update(pygame.mouse.get_pos())
        self.virtual_button.update(pygame.mouse.get_pos())
        self.return_button.update(pygame.mouse.get_pos())

        # Update the last hovered character based on button highlights
        if self.ninja_button.highlighted:
            self.last_hovered_character = 'NinjaFrog'
        elif self.mask_button.highlighted:
            self.last_hovered_character = 'MaskDude'
        elif self.pink_button.highlighted:
            self.last_hovered_character = 'PinkMan'
        elif self.virtual_button.highlighted:
            self.last_hovered_character = 'VirtualGuy'

    def render(self, screen):
        if not self.screen:
            self.screen = screen

        if self.current_state == "MAIN":
            self.start_button.draw(screen)
            self.select_character_button.draw(screen)

        elif self.current_state == "SHOW CHARACTER":
            self.ninja_button.draw(screen)
            self.mask_button.draw(screen)
            self.pink_button.draw(screen)
            self.virtual_button.draw(screen)
            self.virtual_button.draw(screen)
            self.return_button.draw(screen)

        # Render the run animation if a character is hovered
        if self.last_hovered_character and self.current_state == 'SHOW CHARACTER':
            self.display_run_animation(self.last_hovered_character, screen)

    def display_run_animation(self, character, screen, scale_factor=3):  # Added scale_factor argument
            frames = self.character_sprites[character]['idle']
            current_time = pygame.time.get_ticks()
            frame_index = (current_time // 50) % len(frames)
            current_frame = frames[frame_index]

            # Scale the current frame
            scaled_frame = pygame.transform.scale(current_frame, (
            current_frame.get_width() * scale_factor, current_frame.get_height() * scale_factor))

            animation_pos = (500, 50)  # Adjust as necessary
            screen.blit(scaled_frame, animation_pos)

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



