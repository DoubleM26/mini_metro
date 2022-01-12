import pygame
from utils import load_image
from constants import *
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 25)


class Human(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bridge(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bridge_count = 2


class Locomotive(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.locomotive_count = 0


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.triggered = False

    def trigger(self):
        if not self.triggered:
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.rect.x -= 6
            self.rect.y -= 6
            self.triggered = True


class Panel:
    def __init__(self, group):
        self.dict = {0: RED, 1: YELLOW, 2: BLUE}
        self.people_count = 0
        self.buttons = [
                        Button(group, 490, 665, load_image("red_button.png")),
                        Button(group, 550, 665, load_image("yellow_button.png")),
                        Button(group, 610, 665, load_image("blue_button.png")),
                        ]
        self.buttons[0].trigger()
        self.color = RED

        self.bridges = Bridge(group, 710, 665, load_image("bridge.png"))
        self.bridge_number = myfont.render(str(self.bridges.bridge_count), False, (255, 255, 255))

        self.locomotives = Locomotive(group, 390, 665, load_image("locomotive.png"))
        self.locomotive_number = myfont.render(str(self.locomotives.locomotive_count), False, (255, 255, 255))

        self.people_counter = myfont.render(str(self.people_count), False, (255, 255, 255))
        self.human = Human(group, 990, 27, load_image("human.png"))

    def trigger(self, i):
        for button in self.buttons:
            if button.triggered:
                button.image = button.default_image
                button.rect.x += 6
                button.rect.y += 6
                button.triggered = False
        self.buttons[i].trigger()
        self.color = self.dict[i]
