import pygame
pygame.mixer.init()
pygame.init()

class MusicPlayer:
    def __init__(self, music_file):
        self.music_file = music_file
        pygame.mixer.music.load(self.music_file)
        self.is_playing = False

    def play_music(self):
        if not self.is_playing:
            pygame.mixer.music.play(-1)  # Play indefinitely
            self.is_playing = True

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()  # Pause the music
            self.is_playing = False

    def unpause_music(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()  # Resume the music
            self.is_playing = True

    def toggle_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()  # or .play(-1) depending on how you want it to behave
        self.is_playing = not self.is_playing

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
