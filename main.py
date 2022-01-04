import sys
import os
import pygame
from pygame.locals import *
from locals import *
from itertools import product

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


screen = pygame.display.set_mode(WINDOW_SIZE)
all_sprites = pygame.sprite.Group()

board = Board('data/map_peter.txt')
board.load_map(all_sprites)

while True:
    screen.fill(bg_color)
    all_sprites.draw(screen)
    # board.draw_net(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()
