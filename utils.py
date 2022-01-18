import os
import pygame
from constants import YELLOW, BLUE


def load_image(name):
    fullname = os.path.join('data', name)
    img = pygame.image.load(fullname)
    return img


def draw_line(first_point, end_point, screen, color):
    x, y = first_point
    x1, y1 = end_point
    lo = 0 # line offset
    if color == YELLOW:
        lo = 6
    elif color == BLUE:
        lo = -6
    if abs(x1 - x) < abs(y1 - y):
        if y1 > y:
            pygame.draw.line(screen, color, (x + lo, y), (x + lo, (y1 - abs(x - x1))), width=7)
            pygame.draw.line(screen, color, (x + lo, (y1 - abs(x - x1))), (x1 + lo, y1), width=7)
        else:
            pygame.draw.line(screen, color, (x + lo, y), (x + lo, (y1 + abs(x - x1))), width=7)
            pygame.draw.line(screen, color, (x + lo, (y1 + abs(x - x1))), (x1 + lo, y1), width=7)
    else:
        if x1 > x:
            if y1 > y:
                offset = (-3, -3)
            else:
                offset = (-3, 3)
            pygame.draw.line(screen, color, (x, y + lo), ((x1 - abs(y - y1)), y + lo), width=7)
            pygame.draw.line(screen, color, ((x1 - abs(y - y1)) + offset[0], y + offset[1] + lo), (x1, y1 + lo), width=7)
        else:
            if y1 < y:
                offset = (3, 3)
            else:
                offset = (3, -3)
            pygame.draw.line(screen, color, (x, y + lo), ((x1 + abs(y - y1)), y + lo), width=7)
            pygame.draw.line(screen, color, ((x1 + abs(y - y1)) + offset[0], y + offset[1] + lo), (x1, y1 + lo), width=7)





