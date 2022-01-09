import pygame
from constants import *

moscow_record = 1500
peter_record = 1500
novgorod_record = 1500
samara_record = 1500


class Minimap(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = pygame.transform.scale(image, (270, 180))
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.triggered = False

    def trigger(self, n):
        if not self.triggered:
            self.rect.x -= 8
            self.rect.y -= 6
            self.image = pygame.transform.scale(self.image, (297, 198))
            self.triggered = True
            records[n].x += 18
            records[n].y -= 6


moscow_text = SMALL_MENU_FONT.render(str(moscow_record), False, (234, 194, 53))
peter_text = SMALL_MENU_FONT.render(str(peter_record), False, (234, 194, 53))
novgorod_text = SMALL_MENU_FONT.render(str(novgorod_record), False, (234, 194, 53))
samara_text = SMALL_MENU_FONT.render(str(samara_record), False, (234, 194, 53))

moscow_rect = moscow_text.get_rect()
moscow_rect.x, moscow_rect.y = 435, 155
peter_rect = peter_text.get_rect()
peter_rect.x, peter_rect.y = 835, 155
novgorod_rect = novgorod_text.get_rect()
novgorod_rect.x, novgorod_rect.y = 435, 455
samara_rect = samara_text.get_rect()
samara_rect.x, samara_rect.y = 835, 455

records = [moscow_rect, peter_rect, novgorod_rect, samara_rect]
