import pygame
from typing import List
from rect import Rect
from window import Window
import random

class Pipe:
    def __init__(self, window:Window, offset_x:int=100, speed:int=0.2):
        self.window = window
        self.speed = speed

        pos = [window.size[0] + offset_x, window.size[1] / 2]
        self.top_height = random.randint(window.size[1] // 6, window.size[1] - window.size[1] // 4)
        self.pos = pos
        self.bottom_pipe = Rect((pos[0], self.top_height + 300), (75, 1000), (38, 212, 32), "PIPE_BOTTOM", window.get())
        self.middle = Rect((pos[0], self.top_height), (75, 150), (0, 0, 0), "AIR", self.window.get())
        self.top_pipe = Rect((pos[0], 0), (75, self.top_height), (38, 212, 32), "PIPE_TOP", window.get())
        self.score_counted = False
        self.looped = False

    
    def draw(self):
        self.bottom_pipe.draw()
        self.top_pipe.draw()

    
    def loop(self):
        self.pos[0] -= self.speed * self.window.delta_time

        self.bottom_pipe.set_pos((self.pos[0], self.top_height + 300))
        self.top_pipe.set_pos((self.pos[0], 0))
        self.middle.set_pos((self.pos[0], self.top_height))

    
    @property
    def is_looped(self):
        return self.looped
    

    def set_looped(self, looped=True):
        self.looped = looped