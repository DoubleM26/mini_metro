import pygame


class Passenger(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)