import pygame
from window import Window
from environment import Environmnet
from text import Text

class Main:
    def __init__(self):
        print("Initialising pygame...")
        pygame.init()
        print("Loading fonts...")
        self.font = pygame.Font("assets/font.ttf", 30)
        self.font15 = pygame.Font("assets/font.ttf", 15)
        print("Initialising objects...")
        self.window = Window(size=(800, 1000), fps=180)
        self.environment = Environmnet(self.window, self.font)
        print("Done!")
        
        self.running = True


    def run(self):
        self.loop()


    def loop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_END:
                        self.quit()
            
            self.draw()
            self.environment.loop(self.window.delta_time)
        

    def draw(self):
        self.window.draw_start()
        self.environment.draw()
        Text(self.font, f"FPS: {self.window.get_fps()}", (50, 50, 50), (0, 0)).draw(self.window.get())
        Text(self.font, f"Remaining: {len(self.environment.birds)}", (50, 50, 50), (0, 30)).draw(self.window.get())
        Text(self.font, f"Generation: {self.environment.GA.generation}", (50, 50, 50), (0, 60)).draw(self.window.get())
        Text(self.font, f"Timeout: {self.environment.timer} <  {3000 * self.environment.GA.generation}", (50, 50, 50), (0, 90)).draw(self.window.get())
        Text(self.font, f"Highscore: {self.environment.GA.max_fitness_total}", (50, 50, 50), (0, 120)).draw(self.window.get())
        #Text(self.font, f"INPUT: {self.environment.birds[0].brain.input_nodes}", (50, 50, 50), (0, 60)).draw(self.window.get())
        #Text(self.font, f"HIDDEN: {self.environment.birds[0].brain.hidden_layer}", (50, 50, 50), (0, 90)).draw(self.window.get())
        #Text(self.font, f"OUTPUT: {self.environment.birds[0].brain.output_layer}", (50, 50, 50), (0, 120)).draw(self.window.get())
        #Text(self.font, f"BEST FITNESS: {self.environment.birds[0].fitness}", (50, 50, 50), (0, 60)).draw(self.window.get())
        #i = 0
        #for bird in self.environment.birds:
        #    Text(self.font15, f"HIDDEN: {bird.brain.hidden_layer}", (50, 50, 50), (0, 90 + 15 * i)).draw(self.window.get())
        #    i += 1
        self.environment.birds[0].brain.draw(self.window.get(), (0, 150))
        self.window.draw_end()


    def quit(self, code:int=0):
        print(f"Exited program with exit code: {code}")
        self.window.quit()
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
    main.run()