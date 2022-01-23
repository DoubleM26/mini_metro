import pygame


class Train(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color):
        super().__init__(group)
        self.image = pygame.image.load('data/train.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.color = color
        self.stop_time = -1
        self.change_direction_cnt = 1
