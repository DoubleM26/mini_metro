import pygame


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
        self.direction = direction