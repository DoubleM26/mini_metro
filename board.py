from river import River
from itertools import product
import pygame


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

    def draw_grid(self, surface):
        state = [[0] * 720 for _ in range(1080)]
        for x, y in product(range(1080), range(720)):
            pygame.draw.rect(surface, (255, 255, 255),
                             (x * 36,
                              y * 36,
                              36, 36), width=1 - state[x][y])