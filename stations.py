import pygame
from utils import load_image
import random


class CircleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.frames = {0: pygame.image.load('data/circle.png'), 1: pygame.image.load('data/circle_red.png')}
        self.cur_frame = 0
        self.image = load_image("circle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
        else:
            self.image = self.frames[0]


class RectangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.frames = {0: pygame.image.load('data/Rectangle.png'), 1: pygame.image.load('data/rectangle_red.png')}
        self.cur_frame = 0
        self.image = load_image("rectangle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
        else:
            self.image = self.frames[0]


class TriangleStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.frames = {0: pygame.image.load('data/triangle.png'), 1: pygame.image.load('data/triangle_red.png')}
        self.cur_frame = 0
        self.image = load_image("triangle.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
        else:
            self.image = self.frames[0]


class PolygonStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.frames = {0: pygame.image.load('data/polygon.png'), 1: pygame.image.load('data/polygon_red.png')}
        self.cur_frame = 0
        self.image = load_image("polygon.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
        else:
            self.image = self.frames[0]


class StarStation(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.frames = {0: pygame.image.load('data/star.png'), 1: pygame.image.load('data/star_red.png')}
        self.cur_frame = 0
        self.image = load_image("star.png")
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
        else:
            self.image = self.frames[0]


class Stations:
    def __init__(self, all_sprites, path):
        self.board = list()
        with open(path) as f:
            text = f.read()
        for line in text.split('\n'):
            self.board.append(list(line))
        self.stations = [[0 for _ in range(1080)] for _ in range(720)]
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
        print("Add station", x, y)
