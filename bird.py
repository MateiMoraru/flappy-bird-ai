import math
import time
from typing import List, Tuple
import pygame
from window import Window
from rect import Rect
from brain import Brain
from pipe import Pipe

class Bird:
    def __init__(self, window:Window, genes:List=None):
        self.window = window
        self.bird = Rect((self.window.size[0] / 5 - 100, self.window.size[1] / 2 - 25), (20, 20), (248, 255, 48), "BIRD", window.get())
        self.velocity = 0
        self.acceleration = 0.04 * self.window.scale
        self.collided = False
        self.dead = False
        self.score = 0
        self.brain = Brain(genes)
        self.inputs = [0, 0]
        self.fitness = 0
        self.score_counted = False
        self.last_score = 0
        self.looped = False

    def draw(self):
        #self.bird.draw()
        if self.dead or self.collided:
            self.bird.color = (255, 0, 0)
        pygame.draw.circle(self.window.get(), self.bird.color, (self.bird.pos[0] + 10, self.bird.pos[1] + 10), self.bird.size[0] / 0.8)
        pygame.draw.circle(self.window.get(), (0, 0, 0), (self.bird.pos[0] + 10, self.bird.pos[1] + 10), self.bird.size[0] / 0.8, 1)
        #self.bird.draw()
        #surface = pygame.Surface((self.bird.size[0] * 2.6, self.bird.size[1] * 2.6), pygame.SRCALPHA)
        #pygame.draw.circle(surface, (248, 255, 48, 255), (self.bird.size[0] / .8, self.bird.size[0] / .8), self.bird.size[0] / 0.8)
        #surface.fill((248, 255, 48, 100))
        #self.window.get().blit(surface, self.bird.pos)
        #pygame.draw.line(self.window.get(), (255, 0, 0), (self.bird.pos[0] + self.bird.size[0] * 0.8, self.bird.pos[1] + self.bird.size[1] * 0.8), (self.bird.pos[0] + (self.inputs[0] * 1), self.bird.pos[1]), 2)
        #pygame.draw.line(self.window.get(), (255, 0, 0), self.bird.pos, (self.bird.pos[0], self.bird.pos[1] + self.inputs[1]), 2)


    def loop(self, delta_time, next_pipe:Pipe):
        #print(next_pipe.middle.center[1] - self.bird.pos[1], self.bird.pos[1])
        self.fitness = self.score
        try:
            self.fitness += 1 / abs((next_pipe.middle.pos[1] + next_pipe.middle.size[1] / 2) - (self.bird.pos[1] + self.bird.size[1] / 2))
        except:
            self.fitness += 1
        self.velocity += self.acceleration * delta_time
        self.bird.move(y=self.velocity)
        
        if self.bird.pos[1] > self.window.size[1] or self.bird.pos[1] < 0:
            self.dead = True

        self.handle_keys()

        self.loop_brain(next_pipe)
        if self.score and time.time() - self.last_score > 1:
            self.score_counted = False
        self.looped = True


    def loop_brain(self, next_pipe:Pipe):
        inputs = [0, 0, 0]
        inputs[0] = abs(next_pipe.middle.pos[0] - self.bird.pos[0])
        inputs[1] = next_pipe.middle.pos[1] - self.bird.pos[1]
        inputs[2] = self.velocity
        self.inputs = (inputs[0], inputs[1], inputs[2])
        
        self.brain.update_input(inputs)
        self.brain.loop()


    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if self.brain.prediction and self.velocity > 2 and not self.collided or keys[pygame.K_SPACE]:
            self.jump()


    def jump(self):
        self.velocity = -4

    
    def collide(self, rect):
        if self.bird.collide_rect(rect.rect):
            return True

        return False