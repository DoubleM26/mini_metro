import sys
from board import Board
import pygame
from pygame.locals import *
from constants import *
from stations import Stations
from time import time, sleep

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board('maps/map_peter.txt')

all_sprites = pygame.sprite.Group()
rivers = pygame.sprite.Group()
board.load_map(rivers)
stations = Stations(all_sprites, 'maps/map_peter.txt')
stations.draw()
screen.fill(BG_COLOR)
all_sprites.draw(screen)
# board.draw_grid(screen)
rivers.draw(screen)
previous_time = round(time())
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            stations.generate_station()
            stations.draw()
            all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.update()
    if round(time()) - previous_time > stations.duration:
        previous_time = round(time())
        stations.generate_station()
        stations.draw()
        all_sprites.draw(screen)
