from enum import Enum
import pygame

# from JoinGameScreen import MainMenuScreen
from SelectCharacter import SelectCharacter

class GameState(Enum):
    MAIN_MENU = 1
    CHARACTER_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Example screen size
        self.clock = pygame.time.Clock()
        self.current_state = GameState.MAIN_MENU
        self.main_menu = MainMenuScreen()
        self.character_select_screen = SelectCharacter()
        # Placeholder for other screens:
        self.character_select_screen = None
        self.game_logic = None

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.current_state == GameState.MAIN_MENU:
                self.main_menu.handle_event(event)

    def update(self):
        if self.current_state == GameState.MAIN_MENU:
            new_state = self.main_menu.update()
            if new_state == GameState.CHARACTER_SELECT:
                self.current_state = new_state

        elif self.current_state == GameState.CHARACTER_SELECT:
            new_state = self.character_select_screen.update()
            if new_state == GameState.PLAYING:
                pass

        elif self.current_state == GameState.PLAYING:
            # Update game logic here (if you have a GameLogic class)
            pass

        # ... Add more elif blocks for other states

    def render(self):
        self.screen.fill((90, 90, 90))  # Sample background color
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.render(self.screen)

        elif self.current_state == GameState.CHARACTER_SELECT:
            self.character_select_screen.render(self.screen)


        elif self.current_state == GameState.PLAYING:
            # Render game elements here
            pass

        # ... Add more elif blocks for other states
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
