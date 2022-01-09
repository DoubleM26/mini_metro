import sys
from board import Board
import pygame
from pygame.locals import *
from constants import *
from stations import Stations

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board('maps/map_peter.txt')

all_sprites = pygame.sprite.Group()
board.load_map(all_sprites)
stations = Stations(all_sprites)
stations.draw()

while True:
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)
    # board.draw_grid(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()
