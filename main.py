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
            
            self.environment.loop(self.window.delta_time)
            self.draw()
        

    def draw(self):
        self.window.draw_start()
        self.environment.draw(self.font, self.font15)
        try:
            Text(self.font, f"SCORE: {self.environment.birds[0].fitness}", (50, 50, 50), (0, 0)).draw(self.window.get())
            Text(self.font, f"Remaining: {len(self.environment.birds)}", (50, 50, 50), (0, 30)).draw(self.window.get())
            Text(self.font, f"Generation: {self.environment.GA.generation}", (50, 50, 50), (0, 60)).draw(self.window.get())
            Text(self.font, f"Timeout: {self.environment.timer} <  {4000 * self.environment.GA.generation}", (50, 50, 50), (0, 90)).draw(self.window.get())
            Text(self.font, f"Highscore: {self.environment.GA.max_score_total}", (50, 50, 50), (0, 120)).draw(self.window.get())   
            self.environment.birds[0].brain.draw(self.window.get(), (0, 150))
        except Exception as e:
            print(e)
        self.window.draw_end()


    def quit(self, code:int=0):
        print(f"Exited program with exit code: {code}")

        out = ""
        out += f"Best genes occured in generation {self.environment.GA.max_score_generation} (score: {self.environment.GA.max_score_total})\n"
        out += f"Genes: \n{self.environment.GA.max_score_genes}"
        fout = open("data/best_genes.txt", 'a')
        fout.write(out)
        fout.close()
        

        self.window.quit()
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
    main.run()