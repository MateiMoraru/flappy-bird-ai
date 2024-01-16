import math
from typing import List, Tuple
import pygame
from window import Window
from rect import Rect
from brain import Brain
from pipe import Pipe

class Bird:
    def __init__(self, window:Window, genes:List=None):
        self.window = window
        self.bird = Rect((self.window.size[0] / 5, self.window.size[1] / 2 - 25), (50, 50), (248, 255, 48), "BIRD", window.get())
        self.velocity = 0
        self.acceleration = 0.05 * self.window.scale
        self.collided = False
        self.dead = False
        self.score = 0
        self.brain = Brain(genes)
        self.inputs = [0, 0]
        self.fitness = 0

    def draw(self):
        #self.bird.draw()
        pygame.draw.circle(self.window.get(), self.bird.color, (self.bird.pos[0] + 25, self.bird.pos[1] + 25), self.bird.size[0] / 2)
        pygame.draw.circle(self.window.get(), (0, 0, 0), (self.bird.pos[0] + 25, self.bird.pos[1] + 25), self.bird.size[0] / 2, 1)
        #pygame.draw.line(self.window.get(), (255, 0, 0), self.bird.pos, (self.bird.pos[0] + (self.inputs[0] * 1), self.bird.pos[1]), 2)
        #pygame.draw.line(self.window.get(), (255, 0, 0), self.bird.pos, (self.bird.pos[0], self.bird.pos[1] + self.inputs[1]), 2)


    def loop(self, delta_time, next_pipe:Pipe):
        self.fitness += delta_time / 100
        self.velocity += self.acceleration * delta_time
        self.bird.move(y=self.velocity)
        
        if self.bird.pos[1] > self.window.size[1] or self.bird.pos[1] < 0:
            self.dead = True

        self.handle_keys()

        self.loop_brain(next_pipe)


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
        self.velocity = -5

    
    def collide(self, rect):
        # rleft, rtop = rect.pos
        # width, height = rect.size

        # center_x, center_y = self.bird.pos
        # radius = self.bird.size[0] / 2
        # # complete boundbox of the rectangle
        # rright, rbottom = rleft + width/2, rtop + height/2

        # # bounding box of the circle
        # cleft, ctop     = center_x-radius, center_y-radius
        # cright, cbottom = center_x+radius, center_y+radius

        # # trivial reject if bounding boxes do not intersect
        # if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        #     return False  # no collision possible

        # # check whether any point of rectangle is inside circle's radius
        # for x in (rleft, rleft+width):
        #     for y in (rtop, rtop+height):
        #         # compare distance between circle's center point and each point of
        #         # the rectangle with the circle's radius
        #         if math.hypot(x-center_x, y-center_y) <= radius:
        #             print("DIED")
        #             self.died = True
        #             return True  # collision detected

        # # check if center of circle is inside rectangle
        # #print(rleft , center_x , rright , '; ', rtop , center_y , rbottom)
        # if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        #     self.died = True
        #     print("DIED")
        #     return True  # overlaid
        if self.bird.collide_rect(rect.rect):
            return True

        return False  # no collision detected
    # def collide(self, rect:Rect):
    #     pos = self.bird.pos
    #     S = (pos, self.bird.size[0])
    #     point_in_rect = point_in_rectangle((pos[0], pos[1]), rect)
    #     intersect_1 = intersect_circle(S, (rect.pos, (rect.pos[0] + rect.size[0], rect.pos[1])))
    #     intersect_2 = intersect_circle(S, ((rect.pos[0] + rect.size[0], rect.pos[1]), (rect.pos[0] + rect.size[0], rect.pos[1] + rect.size[1])))
    #     intersect_3 = intersect_circle(S, ((rect.pos[0] + rect.size[0], rect.pos[1] + rect.size[1]), (rect.pos[0], rect.pos[1] + rect.size[1])))
    #     intersect_4 = intersect_circle(S, ((rect.pos[0], rect.pos[1] + rect.size[1]), rect.pos))
    #     collided = point_in_rect or intersect_1 or intersect_2 or intersect_3 or intersect_4
    #     if collided and rect.type != "AIR":
    #         self.died = True
    #     return collided
    

def point_in_rectangle(p1, rect:Rect):
    return p1[0] > rect.pos[0] and p1[0] < rect.pos[0] + rect.size[0] and p1[1] > rect.pos[1] and p1[1] < rect.pos[1] + rect.size[1]


def intersect_circle(circle:Tuple, line, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = line[0], line[1], circle[0]
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle[1] ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return False
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return True
        else:
            return False