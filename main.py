import sys
import os
import pygame
from pygame.locals import *
from locals import *
from itertools import product

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (1920, 1080)


class Board:
    def __init__(self, width, height, position=(0, 0), cell_size=48):
        self.width = width
        self.height = height
        self.pos = position
        self.cs = cell_size
        self.state = [[0] * height for _ in range(width)]

    def get_cell(self, mouse_pos):
        result_x = (mouse_pos[0] - self.pos[0]) // self.cs
        result_y = (mouse_pos[1] - self.pos[1]) // self.cs
        if result_x > self.width or result_x < 0 or result_y > self.width or result_y < 0:
            return None
        return result_x, result_y

    def on_click(self, cell):
        self._state[cell[0]][cell[1]] = 1 - self._state[cell[0]][cell[1]]
        print(cell)

    def process_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def draw(self, surface):
        for x, y in product(range(self._width), range(self._height)):
            pygame.draw.rect(surface, (255, 255, 255),
                         (x * self._cs + self._pos[0],
                          y * self._cs + self._pos[0],
                          self._cs, self._cs), width=1 - self._state[x][y])


def load_image(name):
     fullname = os.path.join('data', name)
     image = pygame.image.load(fullname)
     image = pygame.transform.scale(image, (48, 48))
     return image


class CircleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("circle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass


class RectangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("rectangle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass


class TriangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("triangle.png")
        self.rect = self.image.get_rect()

    def update(self):
        pass


screen = pygame.display.set_mode(WINDOW_SIZE)

all_sprites = pygame.sprite.Group()
CircleStation(all_sprites)

while True:
    screen.fill(bg_color)
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()
