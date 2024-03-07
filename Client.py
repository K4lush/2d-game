import time

import pygame
import pickle
import json

from JoinGameScreen import JoinGameScreen
from MainMenuScreen import MainMenuScreen
from LoadingScreen import LoadingScreen
from GameLogicScreen import GameLogicScreen
from GameOverScreen import GameOverScreen



class Client:
    SCREEN = pygame.display.set_mode((800, 400))
    BG_COLOR = (207, 185, 151)  # Background color

    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.clock = pygame.time.Clock()  # Create a clock object for FPS control
        self.screen = pygame.display.set_mode((800, 600))  # Example screen size
        self.network = None
        self.join_menu = JoinGameScreen(self)
        self.main_menu = MainMenuScreen(self)
        self.loading_screen = LoadingScreen()
        self.game_logic = GameLogicScreen()
        self.game_over = GameOverScreen()
        self.static_objects_received = False
        self.current_state = 'JOIN MENU'

    def run(self):
       
        while True:
           
            self.update()
            self.render()
            self.handle_events()
            # self.main_menu.render(self.screen)
            self.clock.tick(60)

    def update(self):

        if self.current_state == "JOIN MENU":
            new_state = self.join_menu.update()
            if new_state == 'MAIN MENU':
                self.current_state = 'MAIN MENU'

        elif self.current_state == "MAIN MENU":
            new_state = self.main_menu.update()
            if new_state == 'PLAYING':
                data = {
                    'state': 'READY',
                    'character': self.main_menu.character
                }
                # Update the server the current state
                self.sendToServer(data)
                self.current_state = 'PLAYING'

        elif self.current_state == "PLAYING":
            incoming_game_state = self.receiveFromServer()
            new_state = self.game_logic.update(incoming_game_state)
            if new_state == 'GAME OVER':
                self.current_state = 'GAME OVER'

        elif self.current_state == "GAME OVER":
            new_state = self.game_over.update()
            if new_state == 'JOIN MENU':
                self.current_state = 'JOIN MENU'

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
            self.sendToServer(outgoing_game_state)

        elif self.current_state == "GAME OVER":
            self.game_over.handle_event(events)


    def render(self):
       
        self.screen.fill(self.BG_COLOR)  # Use the background color variable

        if self.current_state == "PLAYING":
            self.game_logic.render(self.screen)

        elif self.current_state == "JOIN MENU":
            self.join_menu.render(self.screen)

        elif self.current_state == "MAIN MENU":
            self.main_menu.render(self.screen)

        elif self.current_state == "GAME OVER":
            self.game_over.render(self.screen)
        # Continue for other states as necessary

        pygame.display.flip()



    def sendToServer(self, data):
        try:
           

            self.network.send(data)  # Remember to use sendall for UDP
        except Exception as e:
            print(f"Error sending data to server: {e}")

    def receiveFromServer(self):
        incomingData = self.network.receive()
        if incomingData:
            try:
                # incomingData = json.loads(incomingData)
                return incomingData
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
        return []  # Return an empty list if there's an issue

if __name__ == "__main__":
    client = Client()
    client.run()
