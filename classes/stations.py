import pygame
from utils import load_image
import random
from classes.station import Station
from classes.passenger import Passenger


class CircleStation(Station):
    def __init__(self, *group):
        self.frames = {0: pygame.image.load('data/circle.png'), 1: pygame.image.load('data/circle_2.png')}
        self.image = load_image("circle.png")
        super().__init__(*group)


class RectangleStation(Station):
    def __init__(self, *group):
        self.frames = {0: pygame.image.load('data/Rectangle.png'), 1: pygame.image.load('data/rectangle_2.png')}
        self.image = load_image("rectangle.png")
        super().__init__(*group)


class TriangleStation(Station):
    def __init__(self, *group):
        self.frames = {0: pygame.image.load('data/triangle.png'), 1: pygame.image.load('data/triange_2.png')}
        self.image = load_image("triangle.png")
        super().__init__(*group)


class PolygonStation(Station):
    def __init__(self, *group):
        self.frames = {0: pygame.image.load('data/polygon.png'), 1: pygame.image.load('data/polygon_2.png')}
        self.image = load_image("polygon.png")
        super().__init__(*group)


class StarStation(Station):
    def __init__(self, *group):
        self.frames = {0: pygame.image.load('data/star.png'), 1: pygame.image.load('data/star_2.png')}
        self.image = load_image("star.png")
        super().__init__(*group)


class CirclePassenger(Passenger):
    def __init__(self, *group):
        self.image = load_image("passengers/circle.png")
        super().__init__(*group)


class RectanglePassenger(Passenger):
    def __init__(self, *group):
        self.image = load_image("passengers/rectangle.png")
        super().__init__(*group)


class TrianglePassenger(Passenger):
    def __init__(self, *group):
        self.image = load_image("passengers/triangle.png")
        super().__init__(*group)


class StarPassenger(Passenger):
    def __init__(self, *group):
        self.image = load_image("passengers/star.png")
        super().__init__(*group)


class PolygonPassenger(Passenger):
    def __init__(self, *group):
        self.image = load_image("passengers/polygon.png")
        super().__init__(*group)


class Stations:
    def __init__(self, all_sprites, path, passengers_sprites, set_overfilled):
        self.board = list()
        self.set_overfilled = set_overfilled
        with open(path) as f:
            text = f.read()
        for line in text.split('\n'):
            self.board.append(list(line))
        self.stations = [[0 for _ in range(1080 // 36)] for _ in range(720 // 36)]
        self.colors = [[[] for _ in range(1080 // 36)] for _ in range(720 // 36)]
        self.passengers = [[[] for _ in range(1080 // 36)] for _ in range(720 // 36)]
        self.available_station_types = [0, 1, 1, 1, 0, 0]
        self.passengers_sprites = passengers_sprites
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

        self.duration = 6
        self.stations_cnt = 0
        self.passenger_duration = 4

    def check(self, x, y):
        if x == 18 and 9 < y < 24:
            return False
        if x < 2 and y > 26:
            return False
        if self.stations[x][y - 2] or self.stations[x][y + 2]:
            return False
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

        x, y, = random.randint(1, 18), random.randint(1, 27)
        while not self.check(x, y):
            x, y, = random.randint(1, 18), random.randint(1, 27)
        if self.stations_cnt == 12:
            new_station = random.choice([4, 5])
            self.available_station_types[new_station] = 1
            self.stations[x][y] = new_station
        elif self.stations_cnt > 12:
            new_station = random.choice([1, 1, 1, 1, 2, 2, 3, 3, 4, 5])
            self.available_station_types[new_station] = 1
            self.stations[x][y] = new_station
        else:
            self.stations[x][y] = random.choice([1, 1, 1, 2, 3])
        self.draw_station(x, y)

    def clear_color(self, color_index):
        for i in range(len(self.colors)):
            for j in range(len(self.colors[0])):
                if color_index in self.colors[i][j]:
                    self.colors[i][j].remove(color_index)

    def generate_passenger(self):
        offset = random.randint(0, self.stations_cnt + 2)
        cnt = 0
        for i in range(len(self.stations)):
            for j in range(len(self.stations[0])):
                if self.stations[i][j]:
                    if len(self.passengers[i][j]) == 6 or offset != 0:
                        offset -= 1
                    if len(self.passengers[i][j]) == 6:
                            self.set_overfilled(cnt)
                    else:
                        available_passengers = [i for i in range(len(self.available_station_types))
                                                if self.available_station_types[i]]
                        available_passengers.remove(self.stations[i][j])
                        new_passenger = random.choice(available_passengers)
                        print("generated new passenger:", new_passenger)
                        if new_passenger == 1:
                            passenger = CirclePassenger(self.passengers_sprites)
                        elif new_passenger == 2:
                            passenger = RectanglePassenger(self.passengers_sprites)
                        elif new_passenger == 3:
                            passenger = TrianglePassenger(self.passengers_sprites)
                        elif new_passenger == 4:
                            passenger = PolygonPassenger(self.passengers_sprites)
                        elif new_passenger == 5:
                            passenger = StarPassenger(self.passengers_sprites)
                        passenger.set_pos(len(self.passengers[i][j]), j, i)

                        self.passengers[i][j].append(random.choice(available_passengers))
                        return
                    cnt += 1



















