import time
import pygame

class MusicPlayer:

    def __init__(self, music_file):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
    
    def play(self, t=0):
        if t > 0:
            pygame.mixer.music.play(loops=-1, fade_ms=t)
        else:
            pygame.mixer.music.play(loops=-1)
    
    def stop(self, t=0):
        if t > 0:
            pygame.mixer.music.fadeout(t)
        else:
            pygame.mixer.music.stop()

# def play_music(music_file, flag):
#     pygame.mixer.init()
#     pygame.mixer.music.load(music_file)
#     pygame.mixer.music.play()

#     while not flag:
#         time.sleep(1)
    
#     pygame.mixer.music.stop()
    