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

        self.population = 30
        self.GA = GeneticAlgorithm(self.population)
        self.birds = []
        self.pipes = []
        self.timer = 0
        self.generate_pipes()

    def generate_pipes(self):
        for i in range(0, 4):
            pipe = Pipe(self.window, 400 * i)
            self.pipes.append(pipe)

        
        if self.GA.generation > 1:
            self.GA.best_fitness()
            print(self.GA.max_fitness < 35, self.GA.generation >= 10)
            if not (self.GA.max_fitness < 35 and self.GA.generation >= 10):
                #self.GA.next_generation()
                #self.GA.best_fitness()
                new_genes = self.GA.spread_genes()
                
                for j in range(0, self.population):
                    bird = Bird(self.window)
                    bird.brain.set_genes(new_genes[j][0], new_genes[j][1])
                    self.birds.append(bird)
            else:
                self.GA.restart()
                for j in range(0, self.population):
                    bird = Bird(self.window)
                    self.birds.append(bird)
        else:
            for j in range(0, self.population):
                bird = Bird(self.window)
                self.birds.append(bird)


    def draw(self):
        for pipe in self.pipes:
            pipe.draw()
            pipe.set_looped(False)
        for bird in self.birds:
            bird.draw()
        self.GA.draw_curve((0, self.window.size[1]), self.window.get())

    def loop(self, delta_time):
        self.timer += delta_time
        closest_pipe = [-1, -1]
        idx = 0
        for bird in self.birds:
            for pipe in self.pipes:
                if not pipe.is_looped:
                    pipe.loop()
                    pipe.set_looped()
                collided_bird = bird.collide(pipe.bottom_pipe) or bird.collide(pipe.top_pipe)
                if collided_bird:
                    bird.dead = True
                if pipe.middle.pos[0] <= bird.bird.pos[0] < pipe.middle.pos[0] - (pipe.speed * self.window.delta_time) and not pipe.score_counted:
                    bird.score += 1
                    pipe.score_counted = True
                if pipe.middle.pos[0] < -150:
                    self.pipes.pop(self.pipes.index(pipe))
                    self.pipes.append(Pipe(self.window, 1150))

                if closest_pipe[0] == -1 or abs(bird.bird.pos[0] - pipe.middle.pos[0]) < closest_pipe[0]:
                    closest_pipe[1] = idx
                    closest_pipe[0] = abs(bird.bird.pos[0] - pipe.middle.pos[0])
                idx += 1

            if closest_pipe[1] != -1 and len(self.pipes) > closest_pipe[1]:
                bird.loop(self.window.delta_time, self.pipes[closest_pipe[1]])
            if bird.bird.pos[1] < 0 or bird.bird.pos[1] > self.window.size[1] or bird.dead or bird.collided:
                self.GA.add_fitness(bird.fitness)
                self.GA.add_genes(bird.brain.genes)
                self.birds.pop(self.birds.index(bird))
                
        if self.timer > 3000 * self.GA.generation:
            for bird in self.birds:
                self.GA.add_fitness(bird.fitness)
                self.GA.add_genes(bird.brain.genes)
                self.birds.pop(self.birds.index(bird))
            print(f"Timeout hit, restarting from gen {self.GA.generation}")
            self.GA.next_generation()
            self.restart()
            
        if len(self.birds) <= 0:
            self.GA.next_generation()
            self.restart()


    def restart(self):
        self.timer = 0
        self.pipes = []
        self.generate_pipes()