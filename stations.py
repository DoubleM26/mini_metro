import pygame
from utils import load_image
import random


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
    def __init__(self, all_sprites):
        self.stations = [[0 for _ in range(1080 // 36)] for _ in range(720 // 36)]
        start_stations = [0, 1, 2, 3]
        random.shuffle(start_stations)
        print(start_stations)
        self.all_sprites = all_sprites
        self.stations[random.choice(range(4, 9))][random.choice(range(10, 14))] = start_stations[0]
        self.stations[random.choice(range(4, 9))][random.choice(range(16, 20))] = start_stations[1]
        self.stations[random.choice(range(11, 16))][random.choice(range(10, 14))] = start_stations[2]
        self.stations[random.choice(range(11, 16))][random.choice(range(16, 20))] = start_stations[3]

    def draw(self):
        for i in range(len(self.stations)):
            for j in range(len(self.stations[0])):
                if self.stations[i][j] == 1:
                    station = CircleStation(self.all_sprites)
                    station.set_pos(j * 36, i * 36)
                elif self.stations[i][j] == 2:
                    station = RectangleStation(self.all_sprites)
                    station.set_pos(j * 36, i * 36)
                elif self.stations[i][j] == 3:
                    station = TriangleStation(self.all_sprites)
                    station.set_pos(j * 36, i * 36)
