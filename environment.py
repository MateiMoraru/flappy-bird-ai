import time
import pygame
from brain import GeneticAlgorithm
from window import Window
from pipe import Pipe
from bird import Bird
from text import Text

class Environmnet:
    def __init__(self, window:Window, font:pygame.Font):
        self.window = window
        self.font = font

        self.population = 10
        self.GA = GeneticAlgorithm(self.population)
        self.birds = []
        self.pipes = []
        self.timer = 0
        self.generate_pipes()
        
        print('-' * 50)

    def generate_pipes(self):
        for i in range(0, 4):
            pipe = Pipe(self.window, 400 * i)
            self.pipes.append(pipe)

        
        if self.GA.generation > 1:
            self.GA.best_score()
            if self.GA.max_score != 0:
                new_genes = self.GA.spread_genes((1 / self.GA.max_score) * 0.025, 0.85)
            else:
                new_genes = self.GA.spread_genes(1, 0.6)
                
            for j in range(0, self.population):
                bird = Bird(self.window)
                bird.brain.set_genes(new_genes[j][0], new_genes[j][1])
                self.birds.append(bird)
        else:
            for j in range(0, self.population * 20):
                bird = Bird(self.window)
                self.birds.append(bird)


    def draw(self, font1, font2):
        for pipe in self.pipes:
            pipe.draw()
            pipe.set_looped(False)
        self.GA.draw_curve((0, self.window.size[1]), self.window, font2)
        for bird in self.birds:
            bird.draw()

    def loop(self, delta_time):
        self.timer += delta_time
        closest_pipe = [abs(self.birds[0].bird.pos[0] - self.pipes[0].middle.pos[0]), 0]
        idx = 0
        birds_to_remove = []
        for bird in self.birds:
            bird.looped = False
            for pipe in self.pipes:
                if closest_pipe[0] == -1 or 0 < bird.bird.pos[0] - pipe.middle.pos[0] < closest_pipe[0]:
                    closest_pipe[1] = idx
                    closest_pipe[0] = abs(bird.bird.pos[0] - pipe.middle.pos[0])
                if idx + 1 < len(self.pipes) and pipe.middle.pos[0] < bird.bird.pos[0]:
                    closest_pipe[1] = idx + 1
                    closest_pipe[0] = abs(bird.bird.pos[0] - self.pipes[idx + 1].middle.pos[0])
                if (closest_pipe[1] != -1) and not bird.looped:
                    if closest_pipe[1] >= len(self.pipes):
                        closest_pipe[1] = len(self.pipes) - 1
                        closest_pipe[0] = abs(bird.bird.pos[0] - self.pipes[closest_pipe[1]].middle.pos[0])
                    bird.loop(self.window.delta_time, self.pipes[closest_pipe[1]])
                    bird.looped = True
                if not pipe.is_looped:
                    pipe.loop()
                    pipe.increase_speed(0.00001)
                    pipe.set_looped()
                if (bird.collide(pipe.middle) or bird.bird.pos[0] > pipe.middle.pos[0]) and not bird.score_counted:
                    bird.score += 1
                    bird.score_counted = True
                    bird.last_score = time.time()
                    bird.collided = False
                    bird.dead = False
                collided_bird = bird.collide(pipe.bottom_pipe) or bird.collide(pipe.top_pipe)
                if bird.bird.pos[1] < 0 or bird.bird.pos[1] > self.window.size[1] or collided_bird:
                    birds_to_remove.append(bird)
                if pipe.middle.pos[0] < -150:
                    self.pipes.remove(pipe)
                    closest_pipe[1] -= 1
                    self.pipes.append(Pipe(self.window, 800))
                idx += 1
                
        for bird in birds_to_remove:
            if bird in self.birds:
                    self.GA.add_score(bird.fitness)
                    self.GA.add_genes(bird.brain.genes)
                    self.birds.remove(bird)

        if self.timer > 4000 * self.GA.generation:
            for bird in self.birds:
                score = bird.score
                self.GA.add_score(bird.fitness)
                self.GA.add_genes(bird.brain.genes)
                self.birds.remove(bird)
            
            print(f"Generation: {self.GA.generation}")
            print(f"Timer threshold met after {4000 * self.GA.generation}ms")
            # if score > self.GA.max_score_total:
            #     print(f"New highscore reached! Previous best: {self.GA.max_score_total}")
            self.GA.next_generation()
            self.restart()
            
        if len(self.birds) <= 0:
            self.GA.next_generation()
            self.restart()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.restart(True)


    def restart(self, restart=False):
        print(f"Generation: {self.GA.generation}")
        if self.timer > 4000 * self.GA.generation:
            print(f"Timer threshold met after {4000 * self.GA.generation}ms")
        if restart:
            print("Restarting the whole Genetic algorithm class...")
            self.GA.restart()
        
        self.timer = 0
        self.pipes = []
        self.generate_pipes()
        print('-' * 50)