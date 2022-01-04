import sys
import os
import pygame
from pygame.locals import *
from locals import *
from itertools import product
import random

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (1080, 720)


class Board:
    def __init__(self, width, height, position=(0, 0), cell_size=36):
        self.width = width
        self.height = height
        self.pos = position
        self.cs = cell_size
        self.state = [[0] * height for _ in range(width)]

    def draw(self, surface):
        for x, y in product(range(self.width), range(self.height)):
            pygame.draw.rect(surface, (255, 255, 255),
                             (x * self.cs,
                              y * self.cs,
                              self.cs, self.cs), width=1 - self.state[x][y])


def load_image(name):
    fullname = os.path.join('data', name)
    img = pygame.image.load(fullname)
    return img


class CircleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("circle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class RectangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("rectangle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class TriangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("triangle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Stations:
    def __init__(self):
        self.stations = [[0 for _ in range(1080 // 36)] for _ in range(720 // 36)]
        start_stations = [0, 1, 2, 3]
        random.shuffle(start_stations)
        print(start_stations)
        self.stations[random.choice(range(4, 9))][random.choice(range(10, 14))] = start_stations[0]
        self.stations[random.choice(range(4, 9))][random.choice(range(16, 20))] = start_stations[1]
        self.stations[random.choice(range(11, 16))][random.choice(range(10, 14))] = start_stations[2]
        self.stations[random.choice(range(11, 16))][random.choice(range(16, 20))] = start_stations[3]

    def draw(self):
        for i in range(len(self.stations)):
            for j in range(len(self.stations[0])):
                if self.stations[i][j] == 1:
                    station = CircleStation(all_sprites)
                    station.set_pos(j * 36, i * 36)
                elif self.stations[i][j] == 2:
                    station = RectangleStation(all_sprites)
                    station.set_pos(j * 36, i * 36)
                elif self.stations[i][j] == 3:
                    station = TriangleStation(all_sprites)
                    station.set_pos(j * 36, i * 36)

screen = pygame.display.set_mode(WINDOW_SIZE)
all_sprites = pygame.sprite.Group()

stations = Stations()
stations.draw()
board = Board(1080, 720)
screen.fill(bg_color)
board.draw(screen)
pygame.display.flip()

while True:
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            all_sprites = pygame.sprite.Group()
            pygame.display.update()
            stations = Stations()
            stations.draw()
    clock.tick(60)
    pygame.display.update()
