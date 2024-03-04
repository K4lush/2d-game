import pygame
import pickle
from Lava import Lava
from Rope import Rope
from Settings import Settings

import math


# from AnimatedSprite import AnimatedSprite

class GameLogicScreen:
    def __init__(self):
        self.settings = Settings()
        self.players = None
        self.rope = None
        self.lavaBlocks = []
        self.BigLavaBlock = None
        self.gameOver = False
        self.screen_width = 800
        self.screen_height = 600
        self.font_size = 30
        self.alpha_value = 0

        ### ROPE VALUES TO BE MOVED ###
        self.player1 = None
        self.player2 = None
        self.start_pos = None
        self.end_pos = None
        self.distance = None
        self.rope_color = None
        self.lavaData = None
        self.flag = None
        self.Arrows = None


    def fade_in_game_over(self, screen):
            print("method called")
            font = pygame.font.Font(None, self.font_size)
            text = font.render("GAME OVER", True, (255, 255, 255))
            text_width, text_height = font.size("GAME OVER")
            if text_width < self.screen_width and text_height < self.screen_height:
                self.font_size += 5  # Increase the font size
            self.alpha_value += 5  # Increase the alpha value
            if self.alpha_value > 255:
                self.alpha_value = 255  # Ensure alpha doesn't exceed 255
            text.set_alpha(self.alpha_value)
            screen.blit(text, ((self.screen_width - text_width) // 2, (self.screen_height - text_height) // 2))  # Center the text


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

        #return pressed_keys if pressed_keys else ['idle']
    #     if (self.players[0] is not None and self.players[0].action == 'died') or (self.players[1] is not None and self.players[1].action == 'died'):
    # # Your code here

    #         return ['died']
    #     else:
        return pressed_keys if pressed_keys else ['idle'] 
        
    def update(self, data):
        print("GameLogicClass: Data Received:", data)  # Enhanced logging
        if self.settings.gameOver is True:
            print("gameOver in gameLogicScreen")
            self.gameOver = True
        if 'Players' in data and data['Players'] is not None:
            self.players = data['Players']

        if 'Rope' in data and data['Rope'] is not None:
            self.rope = True
            self.player1 = data['Players'][0]
            self.player2 = data['Players'][1]

            self.start_pos = (self.player1['rect_centerx'], self.player1['rect_centery'])
            self.end_pos = (self.player2['rect_centerx'], self.player2['rect_centery'])

            self.rope_color = data['Rope']['color']

            # Calculate distance
            self.distance = math.sqrt((self.start_pos[0] - self.end_pos[0]) ** 2 + (self.start_pos[1] - self.end_pos[1]) ** 2)
            print("Rope Start:", self.start_pos, "End:", self.end_pos, "Color:", self.rope_color)

        if 'Lava' in data:
            self.lavaData = data['Lava']
        if 'LavaBlock' in data:
            self.BigLavaBlock  = data['LavaBlock']
        if 'Flag' in data:
            self.flag = data['Flag']
        if 'Arrow' in data:
            self.Arrows = data['Arrow']
           
            





        
        self.settings.update_player_sprite(self.players)
        self.settings.updateLavaSprites(self.lavaData)
        self.settings.updateLavaBlock(self.BigLavaBlock)
        self.settings.updateFlagSprites(self.flag)
        self.settings.updateArrowSprites(self.Arrows)



    def calculate_camera_offset(self, players):
        # Constants for game window dimensions - adjust as necessary
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

        if players and len(players) >= 2:
            # Calculate midpoint between the players
            mid_x = (players[0]['x'] + players[1]['x']) / 2
            mid_y = (players[0]['y'] + players[1]['y']) / 2

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

        # if not self.gameOver:
        if self.players:
                for player in self.players:
                    id = player['id']
                    character = player['character']
                    action = player['action']
                    direction = player['direction']
                    sprite_key = f'{id}_{character}_{action}'
                    if sprite_key in self.settings.player_sprites:  # Make sure the sprite exists
                        sprite = self.settings.player_sprites[sprite_key]
                        sprite.draw(screen, (player['x'] - camera_offset_x, player['y'] - camera_offset_y))
                # if len(self.players) ==2:
                #     player1score = self.players[0]['score']
                #     player2score = self.players[1]['score']

                #     score = max(player1score,player2score)
                #     print("This is score value: ", score)
                #     my_font = pygame.font.SysFont('Comic Sans MS', 30)
                #     text_surface = my_font.render(str(score), True, (255, 255, 255))  # Convert score to a string
                #     screen.blit(text_surface, (20 , 20))  # Use a tuple for coordinates

                



        if self.flag:
            id = self.flag['id']
            action = self.flag['action']
            key = f'{id}_{action}'
            if key in self.settings.flagSpritesDict:
                sprite = self.settings.flagSpritesDict[key]
                sprite.draw(screen, (self.flag['x']- camera_offset_x, self.flag['y']- camera_offset_y))

        if self.Arrows:
            print("HERE")
            for arrow in self.Arrows:
                id = arrow['id']
                if id in self.settings.arrowSpritesDict:
                    sprite = self.settings.arrowSpritesDict[id]
                    sprite.draw(screen, (arrow['arrowX'] - camera_offset_x, arrow['arrowY'] - camera_offset_y))


        if self.lavaData:
            for lava in self.lavaData:
                sprite_key = lava['lavaX']
                if sprite_key in self.settings.lava_sprites:
                    sprite = self.settings.lava_sprites[sprite_key]
                    sprite.draw(screen, (lava['lavaX'] - camera_offset_x, lava['lavaY'] - camera_offset_y))
                    # sprite.draw(screen, (lava.x - camera_offset_x, lava.y - camera_offset_y))


        if self.BigLavaBlock is not None:
            key = self.BigLavaBlock['lavaX'] - 999
            if key in self.settings.lava_sprites:
                sprite = self.settings.lava_sprites[key]
                # sprite.draw(screen, (self.BigLavaBlock.x - camera_offset_x, self.BigLavaBlock.y - camera_offset_y))
                sprite.draw(screen, (self.BigLavaBlock['lavaX'] - camera_offset_x, self.BigLavaBlock['lavaY'] - camera_offset_y))
        if not self.gameOver:
            if self.rope:
                # Calculate updated positions with camera offset
                updated_start_pos = (self.start_pos[0] - camera_offset_x, self.start_pos[1] - camera_offset_y)
                updated_end_pos = (self.end_pos[0] - camera_offset_x, self.end_pos[1] - camera_offset_y)

                # Calculate distance
                distance = math.sqrt(
                    (updated_start_pos[0] - updated_end_pos[0]) ** 2 + (updated_start_pos[1] - updated_end_pos[1]) ** 2)

                # Dynamic color based on tension
                max_length = 150  # Hardcoded max length value
                color_intensity = 255 if distance >= max_length else min(255, max(0, 155 + int(distance / 2)))
                rope_color = (color_intensity, color_intensity // 2, 0)

                # Generate Bezier curve points
                curve_points = []
                if distance < max_length:
                    curve_intensity = max(0, min(50, 100 - (distance / max_length) * 100))
                    control_point1 = (updated_start_pos[0], updated_start_pos[1] + curve_intensity)
                    control_point2 = (updated_end_pos[0], updated_end_pos[1] + curve_intensity)
                    for t in range(0, 101, 5):
                        t /= 100
                        bx = (1 - t) ** 3 * updated_start_pos[0] + 3 * (1 - t) ** 2 * t * control_point1[0] + 3 * (
                                    1 - t) * t ** 2 * control_point2[0] + t ** 3 * updated_end_pos[0]
                        by = (1 - t) ** 3 * updated_start_pos[1] + 3 * (1 - t) ** 2 * t * control_point1[1] + 3 * (
                                    1 - t) * t ** 2 * control_point2[1] + t ** 3 * updated_end_pos[1]
                        curve_points.append((bx, by))

                # Draw bezier curve or straight line
                if distance >= max_length or len(curve_points) < 2:
                    pygame.draw.line(screen, rope_color, updated_start_pos, updated_end_pos, 5)
                else:
                    pygame.draw.lines(screen, rope_color, False, curve_points, 5)

                # Don't forget to update the display
            pygame.display.flip()
        print("this is self.gameOver",self.gameOver)
        if self.gameOver is True:
            print("calling method")
            self.fade_in_game_over(screen)









