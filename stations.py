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


class PolygonStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("polygon.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class StarStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("star.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Stations:
    def __init__(self, all_sprites, path):
        self.board = list()
        with open(path) as f:
            text = f.read()
        for line in text.split('\n'):
            self.board.append(list(line))
        self.stations = [[0 for _ in range(1080 // 36)] for _ in range(720 // 36)]
        self.colors = [[0 for _ in range(1080 // 36)] for _ in range(720 // 36)]
        start_stations = [0, 1, 2, 3]
        random.shuffle(start_stations)

        self.all_sprites = all_sprites
        x, y = 0, 0
        while not self.check(x, y) or x == 0:
            x = random.choice(range(4, 9))
            y = random.choice(range(10, 14))
        self.stations[x][y] = start_stations[0]
        x, y = 0, 0
        while not self.check(x, y) or x == 0:
            x = random.choice(range(4, 9))
            y = random.choice(range(16, 20))
        self.stations[x][y] = start_stations[1]
        x, y = 0, 0
        while not self.check(x, y) or x == 0:
            x = random.choice(range(11, 16))
            y = random.choice(range(10, 14))
        self.stations[x][y] = start_stations[2]
        x, y = 0, 0
        while not self.check(x, y) or x == 0:
            x = random.choice(range(11, 16))
            y = random.choice(range(16, 20))
        self.stations[x][y] = start_stations[3]

        self.duration = 5
        self.stations_cnt = 0

    def check(self, x, y):
        if x == 18 and 9 < y < 24:
            return False
        if x < 2 and y > 26:
            return
        if self.board[x][y] == "r" or self.stations[x][y]:
            return False
        if self.board[x][y - 1] == "r" or self.stations[x][y - 1]:
            return False
        if self.board[x][y + 1] == "r" or self.stations[x][y + 1]:
            return False
        if self.board[x - 1][y] == "r" or self.stations[x - 1][y]:
            return False
        if self.board[x + 1][y] == "r" or self.stations[x + 1][y]:
            return False
        if self.stations[x + 1][y + 1] or self.stations[x - 1][y - 1] \
                or self.stations[x + 1][y - 1] or self.stations[x - 1][y + 1]:
            return False
        return True

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
                elif self.stations[i][j] == 4:
                    station = PolygonStation(self.all_sprites)
                    station.set_pos(j * 36, i * 36)
                elif self.stations[i][j] == 5:
                    station = StarStation(self.all_sprites)
                    station.set_pos(j * 36, i * 36)

    def draw_station(self, x, y):
        if self.stations[x][y] == 1:
            station = CircleStation(self.all_sprites)
            station.set_pos(y * 36, x * 36)
        elif self.stations[x][y] == 2:
            station = RectangleStation(self.all_sprites)
            station.set_pos(y * 36, x * 36)
        elif self.stations[x][y] == 3:
            station = TriangleStation(self.all_sprites)
            station.set_pos(y * 36, x * 36)
        elif self.stations[x][y] == 4:
            station = PolygonStation(self.all_sprites)
            station.set_pos(y * 36, x * 36)
        elif self.stations[x][y] == 5:
            station = StarStation(self.all_sprites)
            station.set_pos(y * 36, x * 36)

    def generate_station(self):
        self.stations_cnt += 1
        if self.stations_cnt % 5 == 0:
            self.duration += 2

        x, y, = random.randint(1, 18), random.randint(1, 28)
        while not self.check(x, y):
            x, y, = random.randint(1, 18), random.randint(1, 28)
        if self.stations_cnt == 12:
            self.stations[x][y] = random.choice([4, 5])
        elif self.stations_cnt > 12:
            self.stations[x][y] = random.choice([1, 1, 1, 1, 2, 2, 3, 3, 4, 5])
        else:
            self.stations[x][y] = random.choice([1, 1, 1, 2, 3])
        self.draw_station(x, y)
        # print("Add station", x, y)

    def clear_color(self, color_index):
        for i in range(len(self.colors)):
            for j in range(len(self.colors[0])):
                if self.colors[i][j] == color_index:
                    self.colors[i][j] = 0
