import math
from typing import *
import pygame

class Rect:
    def __init__(self, pos:Tuple[float], size:Tuple[float], color:Tuple[int], type:str, window:pygame.Surface, texture:pygame.Surface=None):
        self.pos = pos
        self.size = size
        self.type = type
        self.color = color
        self.window = window
        self.texture = texture
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        self.light = 0

    def draw(self, block_offset:tuple=(0, 0)):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        pos = [self.pos[0] + block_offset[0], self.pos[1] + block_offset[1]]

        if self.texture == None:
            if self.type != "air":
                pygame.draw.rect(self.window, self.color, self.rect)
        else:
            self.window.blit(self.texture, pos)
        if self.light > 0:
            rect(self.window, pos, self.size, (255, 255, 255, self.light))
        elif self.light < 0:
            rect(self.window, pos, self.size, (0, 0, 0, -self.light))


    def collide_point(self, point, block_offset:tuple=(0, 0)):
        pos = [self.pos[0] + block_offset[0], self.pos[1] + block_offset[1]]
        collide_x = point[0] > pos[0] and point[0] < pos[0] + self.size[0]
        collide_y = point[1] > pos[1] and point[1] < pos[1] + self.size[1]

        return collide_x and collide_y
    
    
    def collide_rect(self, rect:pygame.Rect, block_offset:tuple=(0, 0)):
        block = pygame.Rect(self.pos[0] + block_offset[0], self.pos[1] + block_offset[1], self.size[0], self.size[1])

        return rect.colliderect(block)
    

    def set_type(self, type:str):
        self.type = type

    
    def set_texture(self, tex:pygame.Surface):
        self.texture = pygame.transform.scale(tex, self.size)

    
    def set_size(self, size:Tuple[float]):
        self.size = size

    
    def set_pos(self, pos:Tuple[float]):
        self.pos = pos


    def move(self, x:int=0, y:int=0):
        self.pos = (self.pos[0] + x, self.pos[1] + y)


    def add_light(self, light:int):# If light's value is greater than 255, 
        self.light += light
        if self.light > 255:
            self.light = 255
        elif self.light < -255:
            self.light = -255

    def set_light(self, light:int):
        self.light = light
        if self.light > 255:
            self.light = 255
        elif self.light < -255:
            self.light = -255


    def rm_texture(self):
        self.texture = None
        self.type = "air"


def rect(window: pygame.Surface, pos: tuple, size: tuple, color: tuple):
    surf = pygame.Surface(size)
    surf.set_alpha(color[3])
    surf.fill(color)
    window.blit(surf, pos)


def collide_point(rect:List[int], point:List[int]):
    collide_x = point[0] > rect[0] and point[0] < rect[0] + rect[2]
    collide_y = point[1] > rect[1] and point[1] < rect[1] + rect[3]
    return collide_x and collide_y


def dist_block(point:tuple, rect:Rect):
    dx = abs(point[0] - (rect.rect.x + rect.rect.w / 2)) ** 2
    dy = abs(point[1] - (rect.rect.y + rect.rect.h / 2)) ** 2

    return math.sqrt(dx + dy) 
    
    
def dist_point(point:tuple, point2:tuple):
    dx = abs(point[0] - point2[0]) ** 2
    dy = abs(point[1] - point2[1]) ** 2

    return math.sqrt(dx + dy) 