import os
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    img = pygame.image.load(fullname)
    return img
