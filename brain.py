import time
import numpy as np 
from typing import List, Tuple
import random
import pygame

class Brain:
    def __init__(self, genes:List=None):
        if genes is None:
            self.generate_nodes()
        else:
            self.input_nodes = [0, 0]
            self.weights_nr = (6, 2)
            self.weights = genes[0][0]
            self.biases_nr = (2, 1)
            self.biases = genes[0][1]
            self.hidden_layer_nr = 2
            self.hidden_layer = [0, 0]
            self.output_layer = [0]
        

    def generate_nodes(self):
        self.input_nodes = [0, 0]
        self.weights_nr = (6, 2)
        self.weights = []
        for weights_nr in self.weights_nr:
            weights = []
            for weight in range(0, weights_nr):
                weights.append(rand(-1, 1))
            self.weights.append(weights)
        #print(self.weights)
        self.biases_nr = (2, 1)
        self.biases = []
        for biases_nr in self.biases_nr:
            biases = []
            for bias in range(0, biases_nr):
                biases.append(rand(-1, 1))
            self.biases.append(biases)
        self.hidden_layer_nr = 2
        self.hidden_layer = [0, 0]
        self.output_layer = [0]

    
    def update_nodes(self):
        #self.input_nodes = [0, 0, 0]
        self.hidden_layer = [0, 0]
        self.output_layer = [0]

        
    def update_input(self, input_nodes:List=[0, 0]):
        for i in range(0, len(input_nodes)):
            input_nodes[i] = sigmoid(input_nodes[i] / 100)
        self.input_nodes = input_nodes

    
    def loop(self):
        self.update_nodes()
        idx = 0
        for j in range(0, self.hidden_layer_nr):
            for i in range(0, self.weights_nr[0] // self.hidden_layer_nr):
                self.hidden_layer[j] += self.input_nodes[i] * self.weights[0][idx]
                idx += 1
        for i in range(0, len(self.hidden_layer)):
            self.hidden_layer[i] += self.biases[0][i]
        self.hidden_layer[0] = sigmoid(self.hidden_layer[0])
        self.hidden_layer[1] = sigmoid(self.hidden_layer[1])

        for i in range(0, self.weights_nr[1]):
            self.output_layer[0] += self.hidden_layer[i] * self.weights[1][i]
        self.output_layer[0] += self.biases[1][0]
        self.output_layer[0] = sigmoid(self.output_layer[0])

    
    def draw(self, window:pygame.Surface, offset:Tuple=(0, 0)):
        input_pos = []
        node_color = (50, 50, 50)
        node_radius = 15
        for i in range(0, len(self.input_nodes)):
            pos = (offset[0] + node_radius, offset[1] + node_radius + 50 * i)
            pygame.draw.circle(window, node_color, pos, node_radius)
            input_pos.append(pos)
        hidden_pos = []
        for i in range(0, len(self.hidden_layer)):
            pos = (offset[0] + node_radius + 70, offset[1] + node_radius + 30 + 50 * i)
            color = (150, 0, 0)
            if self.hidden_layer[i] < 0:
                color = (0, 0, 150)
            pygame.draw.circle(window, color, pos, node_radius)
            hidden_pos.append(pos)
        idx = 0
        for start in input_pos:
            for end in hidden_pos:
                color = (150, 0, 0)
                if self.weights[0][idx] < 0:
                    color = (0, 0, 150)
                pygame.draw.line(window, color, start, end, 2)
                idx += 1
        output_pos = []
        color = (150, 0, 0)
        if self.output_layer[0] < 0.5:
            color = (0, 0, 150)
        pos = (offset[0] + node_radius + 140, offset[1] + node_radius + 60)
        pygame.draw.circle(window, color, pos, node_radius)
        for i in range(0, len(hidden_pos)):
            color = (150, 0, 0)
            if self.weights[1][i] < 0:
                color = (0, 0, 150)
            pygame.draw.line(window, color, hidden_pos[i], pos)
         


    def set_genes(self, weights, biases):
        self.weights = weights
        self.biases = biases

    @property
    def prediction(self, p:bool=False):
            if p:
                print("Input:", self.input_nodes)
                print("Hidden:", self.hidden_layer)
                print("Output:", self.output_layer)
            return self.output_layer[0] > 0.5
    

    @property
    def genes(self):
        return [self.weights, self.biases]
    

    def rand(self, x:float=0, y:float=1):
        return random.uniform(x, y)


class GeneticAlgorithm:
    def __init__(self, population:int):
        self.population = population
        self.generation = 1
        self.best_fitness_total = []
        self.fitness = []
        self.max_fitness_total = -1
        self.genes = []

    def add_fitness(self, fitness):
        self.fitness.append(fitness)

    def add_genes(self, genes):
        self.genes.append(genes)


    def best_fitness(self):
        max_fitness = -1
        if len(self.fitness) < self.population:
            max_fitness = self.fitness[0]
            self.parent_bird_genes = self.genes[0]
            return
        for i in range(0, self.population):
            if len(self.fitness) < i:
                max_fitness = self.fitness[0]
                self.parent_bird_genes = self.genes[0]
                return
            if self.fitness[i] > max_fitness:
                max_fitness = self.fitness[i]
                self.parent_bird_genes = self.genes[i]
        self.max_fitness = max_fitness
        self.best_fitness_total.append(max_fitness)
        if self.max_fitness > self.max_fitness_total:
            self.max_fitness_total = self.max_fitness

    
    def mutate_genes(self, mutation_mult:int=10, mutation_chance:float=0.0):
        best_genes = self.parent_bird_genes
        new_genes = []
        weights = [[], []]
        biases = [[], []]
        
        for weight in best_genes[0][0]:
            current_weight = weight
            if random.random() > mutation_chance:
                current_weight += rand(-1, 1) * mutation_mult
            weights[0].append(current_weight)
        for weight in best_genes[0][1]:
            current_weight = weight
            if random.random() > mutation_chance:
                current_weight += rand(-1, 1) * mutation_mult
            weights[1].append(current_weight)

        for bias in best_genes[1][0]:
            current_bias = bias
            if random.random() > mutation_chance:
                current_bias += rand(-1, 1) * mutation_mult
            biases[0].append(current_bias)
        for bias in best_genes[1][1]:
            current_bias = bias
            if random.random() > mutation_chance:
                current_bias += rand(-1, 1) * mutation_mult
            biases[1].append(current_bias)

        new_genes.append(weights)
        new_genes.append(biases)
        return new_genes


    def spread_genes(self, mutation_mult:int=100, mutation_chance:float=0.7):
        new_genes = []
        for i in range(0, self.population):
            genes = self.mutate_genes(mutation_mult, mutation_chance)
            new_genes.append(genes) 
        self.fitness = []
        self.genes = []
        return new_genes
    

    def next_generation(self):
        self.generation += 1


    def draw_curve(self, bottom, window:pygame.Surface):
        last_pos = bottom
        idx = 0
        for fitness in self.best_fitness_total:
            pos = (bottom[0] + idx * 20, bottom[1] - fitness)
            pygame.draw.circle(window, (0, 0, 0), pos, 5)
            pygame.draw.line(window, (0, 0, 0), last_pos, pos)
            last_pos = pos
            idx += 1

        
    def restart(self):
        self.generation = 1
        self.best_fitness_total = []
        self.fitness = []
        self.genes = []


def sigmoid(x):
    return 1/(1 + np.exp(-x))


def rand(x:float=0, y:float=1):
    return random.uniform(x, y)