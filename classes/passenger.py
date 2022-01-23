import pygame


class Passenger(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()

    def set_pos(self, number, station_x, station_y):
        if number < 4:
            self.rect.x = station_x * 36 + 40 + number * 16
            self.rect.y = station_y * 36 + 4
        else:
            self.rect.x = station_x * 36 + 40 + (number - 4) * 16
            self.rect.y = station_y * 36 + 20












