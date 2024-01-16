import pyautogui
import pygame

class Window:
    def __init__(self, size=(1920, 1080), fullscreen=0, display_no=0, fps=0):
        self.size = size
        self.background_color = (52, 207, 235)
        self.fps = fps
        if fullscreen:
            screen_size = pyautogui.size()
            self.size = (screen_size.width, screen_size.height)
            self.scale = screen_size[0] / 1920
            print("Window size: " + str(self.size))
            self.window = pygame.display.set_mode(self.size, pygame.FULLSCREEN, vsync=1, display=display_no)
        else:
            self.window = pygame.display.set_mode(self.size, vsync=1, display=display_no)
            self.scale = self.size[0] / 1920

        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.center = (self.size[0] / 2, self.size[1] / 2)

    
    def draw_start(self):
        self.delta_time = self.clock.tick(self.fps)
        self.window.fill(self.background_color)

    
    def draw_end(self):
        pygame.display.flip()


    def get(self):
        return self.window
    

    def get_center(self):
        return (self.size[0] / 2, self.size[1] / 2)
    

    def get_fps(self):
        return int(self.clock.get_fps())


    def quit(self):
        pygame.quit()
        quit()