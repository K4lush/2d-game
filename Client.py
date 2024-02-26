import time

import pygame
import pickle

from JoinGameScreen import JoinGameScreen
from MainMenuScreen import MainMenuScreen
from LoadingScreen import LoadingScreen
from GameLogicScreen import GameLogicScreen

class Client:
    SCREEN = pygame.display.set_mode((800, 400))
    BG_COLOR = (207, 185, 151)  # Background color

    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.clock = pygame.time.Clock()  # Create a clock object for FPS control
        self.screen = pygame.display.set_mode((800, 600))  # Example screen size
        self.network = None
        self.join_menu = JoinGameScreen(self)
        self.main_menu = MainMenuScreen()
        self.loading_screen = LoadingScreen()
        self.game_logic = GameLogicScreen()
        self.static_objects_received = False
        self.current_state = 'JOIN MENU'

    def run(self):
        while True:
            self.update()
            self.render()
            self.handle_events()
            self.clock.tick(60)  # Limit to 60 FPS

    def update(self):
        if self.current_state == "PLAYING":
            incoming_game_state = self.receiveFromServer()
            print("CLIENT: Received state:", incoming_game_state)  # Enhanced logging
            self.game_logic.update(incoming_game_state)

        elif self.current_state == "JOIN MENU":
            new_state = self.join_menu.update()
            if new_state == 'MAIN MENU':
                self.current_state = 'MAIN MENU'

        elif self.current_state == "MAIN MENU":
            new_state = self.main_menu.update()
            if new_state == 'PLAYING':
                data = {
                    'state': 'READY',
                    'character': 'NinjaFrog'
                }
                # Update the server the current state
                self.sendToServer(data)
                self.current_state = 'PLAYING'

        # elif self.current_state == "LOADING SCREEN":
        #     new_state = self.loading_screen.update(self.network)
        #     if new_state == 'PLAYING':
        #         self.current_state = 'PLAYING'

        elif self.current_state == "GAME OVER":
            pass

    def handle_events(self):
        events = pygame.event.get()

        # Handle events outside of the loop, affecting global behavior as needed
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Handle state-specific events
        if self.current_state == "JOIN MENU":
            self.join_menu.handle_event(events)  # Pass the entire event list

        elif self.current_state == "MAIN MENU":
            self.main_menu.handle_event(events)

        elif self.current_state == "LOADING SCREEN":
            pass  # You might have logic to update the loading screen here

        elif self.current_state == "PLAYING":
            keys = pygame.key.get_pressed()
            outgoing_game_state = self.game_logic.handle_event(keys)
            print("THIS IS WHAT THE CLIENT IS SENDING", outgoing_game_state)
            self.sendToServer(outgoing_game_state)

    def render(self):
        self.screen.fill((90, 90, 90))  # Sample background color

        if self.current_state == "PLAYING":
            self.game_logic.render(self.screen)

        if self.current_state == "JOIN MENU":
            self.join_menu.render(self.screen)

        if self.current_state == "MAIN MENU":
            self.main_menu.render(self.screen)

        if self.current_state == "LOADING SCREEN":
            self.loading_screen.render(self.screen)
        # ... Add more elif blocks for other states

        pygame.display.flip()

    def sendToServer(self, data):
        try:
            self.network.send(data)
        except Exception as e:
            print(f"Error sending data to server: {e}")

    def receiveFromServer(self):
        incomingData = self.network.receive()
        if incomingData:
            try:
                incomingData = pickle.loads(incomingData)
                return incomingData
            except pickle.UnpicklingError as e:
                print(f"Error unpickling data: {e}")
        return []

if __name__ == "__main__":
    client = Client()
    client.run()
