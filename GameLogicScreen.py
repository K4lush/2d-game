import pygame
import pickle
from Lava import Lava
from Rope import Rope
from Settings import Settings
from Button import Button

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
        self.Alpha_value = 255
        self.gameOver = False
        
       
        self.FS = 20
      

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
        self.score = 0
        self.resetGame = False
        self.backgroundCounter = 0
        self.showInstructions = True

    def fade_in_game_over(self, screen):
           
            font = pygame.font.Font(None, self.font_size)

            text = font.render("GAME OVER", True, (255, 255, 255))
            text_width, text_height = font.size("GAME OVER")

            score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            score_text_width, score_text_height = font.size("Score: " + str(self.score))


            if text_width < self.screen_width and text_height < self.screen_height:
                self.font_size += 5  # Increase the font size
            self.alpha_value += 5  # Increase the alpha value
            if self.alpha_value > 255:
                self.alpha_value = 255  # Ensure alpha doesn't exceed 255
            text.set_alpha(self.alpha_value)
            score_text.set_alpha(self.alpha_value)
            screen.blit(text, ((self.screen_width - text_width) // 2, (self.screen_height - text_height) // 2))  # Center the text
            screen.blit(score_text, ((self.screen_width - score_text_width) // 2, (self.screen_height - text_height) // 2 + text_height + 10))
            
    def fade_out_countdown(self, screen):
            font = pygame.font.Font(None, self.font_size)

            text = font.render("LAVA INBOUND - RUN", True, (255, 255, 255))
            text_width, text_height = font.size("LAVA INBOUND - RUN")

            if text_width < self.screen_width and text_height < self.screen_height:
                self.font_size += 5  # Increase the font size
            self.Alpha_value -= 5  # Decrease the alpha value
            if self.Alpha_value < 0:
                self.Alpha_value = 0  # Ensure alpha doesn't go below 0
                self.stopCountdown = True
            text.set_alpha(self.Alpha_value)
            
            screen.blit(text, ((self.screen_width - text_width) // 2, (self.screen_height - text_height) // 2))  # Center the text
    
    def printInstructions(self, screen):
        font_path = "assets/fonts/SC.ttf"  # Path to the custom font file
        font = pygame.font.Font(font_path, self.FS)

        # Instructions split into three lines
        line1 = "Reach The Top of the Map"
        line2 = "Before the Lava Catches You!"
        line3 = "Collect as the flags"
        line4 = "on your way to earn more points!"
        lines = [line1, line2, line3, line4]  # Add more lines if needed

        # Render each line separately and get the max width and total height
        text_surfaces = []
        total_height = 0
        max_width = 0
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_width, text_height = font.size(line)
            total_height += text_height
            max_width = max(max_width, text_width)
            text_surfaces.append((text_surface, text_width, text_height))

        # Render each line at the top left corner of the screen
        x = 10  # Adjust the horizontal position as needed
        y = 10  # Adjust the vertical position as needed
        for text_surface, _, text_height in text_surfaces:
            screen.blit(text_surface, (x, y))
            y += text_height  # Move down to the next line

        # Optional: Draw a rectangle around the instructions
        pygame.draw.rect(screen, (255, 255, 255), (x - 5, 5, max_width + 10, total_height), 2)


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

       
        return pressed_keys if pressed_keys else ['idle'] 
        
    def update(self, data):
       
        if self.settings.gameOver is True:
          
            self.gameOver = True
       
        
        if 'Players' in data and data['Players'] is not None:
            self.players = data['Players']

        if 'Rope' in data and data['Rope'] is not None:
            self.rope = True
            # Extract player data
            self.player1 = data['Players'][0]
            self.player2 = data['Players'][1]

            # Calculate start and end positions using player data
            self.start_pos = (self.player1['rect_centerx'], self.player1['rect_centery'])
            self.end_pos = (self.player2['rect_centerx'], self.player2['rect_centery'])

            self.rope_color = data['Rope']['color']

            # Calculate distance
            self.distance = math.sqrt((self.start_pos[0] - self.end_pos[0]) ** 2 + (self.start_pos[1] - self.end_pos[1]) ** 2)
          

        if 'Lava' in data:
            self.lavaData = data['Lava']
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
        elif self.players!= None:
            #
            mid_x = (players[0]['x'])
            mid_y = (players[0]['y'])

            camera_offset_x = mid_x - WINDOW_WIDTH / 2
            camera_offset_y = mid_y - WINDOW_HEIGHT / 2
        else:
            camera_offset_x, camera_offset_y = 0, 600

       

        return camera_offset_x, camera_offset_y
    
    def get_camera_view_coordinates(self, camera_offset_x, camera_offset_y):
    # Calculate the visible area based on camera position and screen size
        top_left_x = camera_offset_x
        top_left_y = camera_offset_y
        bottom_right_x = camera_offset_x + self.screen_width
        bottom_right_y = camera_offset_y + self.screen_height

        return top_left_x, top_left_y, bottom_right_x, bottom_right_y


    def render(self, screen):

     


        camera_offset_x, camera_offset_y = self.calculate_camera_offset(self.players)
        cameraInfo = self.get_camera_view_coordinates(camera_offset_x, camera_offset_y)
        topLeftX = cameraInfo[0]
        topLeftY = cameraInfo[1]
        bottomRightX = cameraInfo[2]
        bottomRightY = cameraInfo[3]
        if self.settings.background_image:
            block_height = 32
            block_width = 32
          
           

            num_blocks_horizontal = 3000 // block_width + 1
            num_blocks_vertical = 3000 // block_height + 1


            

            # Draw the background blocks
            for row in range(num_blocks_vertical):
                for col in range(num_blocks_horizontal):
                    block_x = topLeftX + col * block_width  - camera_offset_x -300
                    block_y = topLeftY + row * block_height - camera_offset_y
                    if block_x < self.screen_width and block_y < self.screen_height:  # Draw only within the screen boundaries
                        block_rect = pygame.Rect(block_x, block_y + self.backgroundCounter, block_width, block_height)
                        screen.blit(self.settings.background_image, block_rect)

            #self.backgroundCounter += 2

        for block in self.settings.platforms:
            if block.sprite:  # Ensure a sprite is assigned
                block.draw(screen, (block.x - camera_offset_x, block.y - camera_offset_y))

        for block in self.settings.nonBlockingPlatforms:
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
                if len(self.players) ==2:
                   
                    player1score = self.players[0]['score']
                    player2score = self.players[1]['score']

                    self.score = max(player1score,player2score)
                    
                    my_font = pygame.font.SysFont('Comic Sans MS', 30)
                    text_surface = my_font.render(str(self.score), True, (255, 255, 255))  # Convert score to a string
                    screen.blit(text_surface, (20 , 20))  # Use a tuple for coordinates
                # if self.players[0]['twoPlayers'] == True:
                #     self.showCountdown = True
                #     print("CLIENT KNOWS THERE ARE TWO PLAYERS")
                



        if self.flag:
            id = self.flag['id']
            action = self.flag['action']
            key = f'{id}_{action}'
            if key in self.settings.flagSpritesDict:
                sprite = self.settings.flagSpritesDict[key]
                sprite.draw(screen, (self.flag['x']- camera_offset_x, self.flag['y']- camera_offset_y))

        if self.Arrows:
   
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

        # if self.showCountdown and not self.stopCountdown:
        #     self.fade_out_countdown(screen)
        #     print("FADEOUT METHOD CALLED")
        if self.players:
            if len(self.players) == 2:

                if self.showInstructions: 
                    self.printInstructions(screen)
                    if self.players[0]['y'] <2200 or self.players[1]['y'] < 2200:
                        self.showInstructions = False

            else:
                if self.showInstructions: 
                    self.printInstructions(screen)
                    if self.players[0]['y'] <2200:
                        self.showInstructions = False



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
        
        if self.gameOver is True:
            
            self.fade_in_game_over(screen)









