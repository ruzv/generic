import math
import pygame
import generic2 as gener
#import generic as gener


class maze():

    w, h = 0, 0
    runer_x, runer_y = 0, 0
    runer_speed = 0
    runer_dist = 0
    chaser_x, chaser_y = 0, 0
    chaser_speed = 0

    def __init__(self, w, h, draw, fps=0):
        self.w = w
        self.h = h
        self.draw = draw
        self.fps = fps
        if draw == True:
            self.clock = pygame.time.Clock()
            self.sc = pygame.display.set_mode([600, 600])

    def init_runer(self, x, y, speed, dna, prams):
        self.runer_dist = 0
        self.runer_x = x
        self.runer_y = y
        self.runer_speed = speed
        self.dna = dna
        self.prams = prams

    def init_chaser(self, x, y, speed):
        self.chaser_x = x
        self.chaser_y = y
        self.chaser_speed = speed

    def get_runer_dir(self):
        net = gener.net(self.get_net_input(), self.dna, self.prams)
        output = net.calculate_net() #gener.generate_entity_net(self.dna, self.prams, self.get_net_input())
        table = [0, 0, 0, 0]
        high = output.index(max(output))
        table[high] = 1
        e = 0
        for n in range(0, 4):
            e += abs(table[n] - output[n])
        return high+1, e**2

    def move_runer(self, dir):
        if dir == 1:#up
            if self.runer_y > 0:
                self.runer_y -= self.runer_speed
                self.runer_dist += self.runer_speed
        elif dir == 2:#down
            if self.runer_y < self.h:
                self.runer_y += self.runer_speed
                self.runer_dist += self.runer_speed
        elif dir == 3:#right
            if self.runer_x < self.w:
                self.runer_x += self.runer_speed
                self.runer_dist += self.runer_speed
        elif dir == 4:#left
            if self.runer_x > 0:
                self.runer_x -= self.runer_speed
                self.runer_dist += self.runer_speed

    def angle_from_points(self, x1, y1, x2, y2):
        try:
            angle = abs(math.degrees(math.atan((y2 - y1)/(x2 - x1))))
            if x1 > x2:
                if y1 > y2:
                    angle += 180
                elif y1 < y2:
                    angle = 90 - angle
                    angle += 90
            elif x1 < x2:
                if y1 > y2:
                    angle = 360 - angle
                elif y1 < y2:
                    angle += 0
            return angle
        except:
            return 0

    def move_chaser(self):
        angle = self.angle_from_points(self.chaser_x, self.chaser_y, self.runer_x, self.runer_y)
        x = self.chaser_speed * math.cos(math.radians(angle))
        y = self.chaser_speed * math.sin(math.radians(angle))
        self.chaser_x += x
        self.chaser_y += y

    def collision_detection(self):
        if self.runer_x < self.chaser_x+20 and self.runer_x+20 > self.chaser_x and self.runer_y < self.chaser_y+20 and self.runer_y+20 > self.chaser_y:
            return True
        return False

    def main(self):
        while self.collision_detection() != True:
            a, b = self.get_runer_dir()
            self.runer_dist -= b
            self.move_runer(a)
            self.move_chaser()
            if self.draw == True:
                self.sc.fill((255, 255, 255))

                self.draw_chaser()
                self.draw_runer()
                self.draw_maze()

                self.clock.tick(self.fps)
                pygame.display.update()
            else:
                if self.runer_dist > 15000:
                    break

        return self.runer_dist

    def draw_chaser(self):
        pygame.draw.rect(self.sc, (0, 0, 0), [self.chaser_x, self.chaser_y, 20, 20])
    
    def draw_runer(self):
        pygame.draw.rect(self.sc, (200, 0, 0), [self.runer_x, self.runer_y, 20, 20])
    
    def draw_maze(self):
        pygame.draw.rect(self.sc, (0, 0, 0), [0, 0, self.w, self.h], 1)

    def get_net_input(self):
        return [self.runer_x, self.runer_y, self.chaser_x, self.chaser_y]

"""
for i in range(20):
    prams = [[5 ,4], [4, 5]]
    dna = gener.generate_dna_net(prams)


    arena = maze(400, 400, True, 30)
    arena.init_runer(50, 50, 5, dna, prams)
    arena.init_chaser(100 ,100, 2)
    print(arena.main())
    del arena
"""