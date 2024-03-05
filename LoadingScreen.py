from Button import Button
class LoadingScreen:
    def __init__(self):
        self.loading_button = Button(325, 125, 150, 60, color=(207, 185, 151),
                                highlight_color=(90, 90, 90), font_color=(8, 15, 15), font_size=30,
                                text='Waiting for other player to join', font='assets/fonts/SC.ttf')
    def render(self, screen):
        self.loading_button.draw(screen)
        self.loading_button.animate()  # This will also animate the text

    def update(self, network):
        other_player_state = network.receive()
        
        if other_player_state == "READY":
            return "PLAYING"

    def handle_event(self, event):
        pass

