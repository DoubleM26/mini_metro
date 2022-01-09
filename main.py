import sys
from board import Board
import pygame
from pygame.locals import *
from constants import *
from stations import Stations
from main_menu import *

pygame.init()
clock = pygame.time.Clock()
game_condition = 0
screen = pygame.display.set_mode(WINDOW_SIZE)
mouse_pos = (0, 0)

menu_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

moscow = Minimap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"))
peter = Minimap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"))
novgorod = Minimap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"))
samara = Minimap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"))

while True:
    if game_condition == 0:
        screen.fill(BG_COLOR)
        screen.blit(BIG_MENU_FONT.render('MiniMetro', False, (255, 255, 255)), (400, 60))

        screen.blit(MAIN_MENU_FONT.render('Москва', False, (255, 255, 255)), (274, 340))
        screen.blit(MAIN_MENU_FONT.render('Санкт-Петербург', False, (255, 255, 255)), (599, 340))
        screen.blit(MAIN_MENU_FONT.render('Нижний Новгород', False, (255, 255, 255)), (190, 645))
        screen.blit(MAIN_MENU_FONT.render('Самара', False, (255, 255, 255)), (677, 645))

        menu_sprites.draw(screen)

        screen.blit(moscow_text, moscow_rect)
        screen.blit(peter_text, peter_rect)
        screen.blit(novgorod_text, novgorod_rect)
        screen.blit(samara_text, samara_rect)

        for n, el in enumerate(menu_sprites):
            if el.rect.collidepoint(mouse_pos):
                el.trigger(n)
            else:
                if el.triggered:
                    el.image = el.default_image
                    el.rect.x += 8
                    el.rect.y += 6
                    el.triggered = False
                    records[n].x -= 18
                    records[n].y += 6

    elif game_condition == 1:
        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        # board.draw_grid(screen)
    elif game_condition == 2:
        pass

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if game_condition == 0:
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                for n, el in enumerate(menu_sprites):
                    if el.rect.collidepoint(mouse_pos):
                        game_condition = 1
                        if n == 0:
                            board = Board('maps/map_moscow.txt')
                        elif n == 1:
                            board = Board('maps/map_peter.txt')
                        elif n == 2:
                            board = Board('maps/map_novgorod.txt')
                        elif n == 3:
                            board = Board('maps/map_samara.txt')
                        board.load_map(all_sprites)
                        stations = Stations(all_sprites)
                        stations.draw()

        elif game_condition == 1:
            pass
        elif game_condition == 2:
            pass

    clock.tick(60)
    pygame.display.update()
