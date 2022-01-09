import sys
import os
import pygame
from pygame.locals import *
from locals import *
from itertools import product
import random
from panel import *

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (1080, 720)


class River(pygame.sprite.Sprite):
    def __init__(self, direction, group, x, y):
        super().__init__(group)
        if direction == 'basic':
            self.image = pygame.image.load("data/river.png")
        elif direction == 'bottom':
            self.image = pygame.image.load('data/river_right.png')
        elif direction == 'top':
            self.image = pygame.image.load('data/river_top.png')
        elif direction == 'left':
            self.image = pygame.image.load('data/river_left.png')
        elif direction == 'down':
            self.image = pygame.image.load('data/river_down.png')
        elif direction == 'angle':
            self.image = pygame.image.load('data/angle.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, map_file):
        self.board = list()
        with open(map_file) as f:
            text = f.read()
        for el in text.split('\n'):
            self.board.append(list(el))

    def load_map(self, group):
        for i in range(len(self.board)):
            row = self.board[i]
            for j in range(len(row)):
                tile = row[j]
                if tile == 'r':
                    River('basic', group, j * 36, i * 36)
                elif tile == 'a':
                    River('bottom', group, j * 36, i * 36)
                elif tile == 't':
                    River('top', group, j * 36, i * 36)
                elif tile == 'l':
                    River('left', group, j * 36, i * 36)
                elif tile == 'd':
                    River('down', group, j * 36, i * 36)
                elif tile == 'h':
                    River('angle', group, j * 36, i * 36)

    def draw_net(self, surface):
        state = [[0] * 720 for _ in range(1080)]
        for x, y in product(range(1080), range(720)):
            pygame.draw.rect(surface, (255, 255, 255),
                             (x * 36,
                              y * 36,
                              36, 36), width=1 - state[x][y])


class CircleStation(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("data/circle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class RectangleStation(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("data/Rectangle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class TriangleStation(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("data/triangle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass

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
interface_sprites = pygame.sprite.Group()

board = Board('data/map_peter.txt')
stations = Stations()
board.load_map(all_sprites)

panel = Panel(interface_sprites)

while True:
    screen.fill(bg_color)
    # board.draw_net(screen)
    stations.draw()
    all_sprites.draw(screen)
    interface_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if panel.buttons[0].rect.collidepoint(mouse_pos):
                panel.trigger(0)
            elif panel.buttons[1].rect.collidepoint(mouse_pos):
                panel.trigger(1)
            elif panel.buttons[2].rect.collidepoint(mouse_pos):
                panel.trigger(2)

    clock.tick(60)
    pygame.display.update()
