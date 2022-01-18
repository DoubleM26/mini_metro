import sys

import pygame.sprite
from trains import *
from board import Board
from pygame.locals import *
from stations import Stations
from main_menu import *
from time import time
from panel import Panel, myfont
from utils import draw_line
from line import Line

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)


flag = False
index = 0
n = 0
frame_count = 0
sign = 1
previous_time = 0
game_condition = 0
mouse_pos = (0, 0)
red_lines = list()
red_ends = [(0, 0), (0, 0)]
drawing = False
first_point = (0, 0)
red_points = list()
basic_rivers = list()
unfinished_line = Falseist()

rivers = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
train_sprites = pygame.sprite.Group()

panel = Panel(interface_sprites)
stations = Stations(all_sprites, 'maps/map_moscow.txt')

moscow = Minimap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"))
peter = Minimap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"))
novgorod = Minimap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"))
samara = Minimap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"))

red_line = Line(1)
blue_line = Line(2)
yellow_line = Line(3)


def update():
    screen.fill(BG_COLOR)
    screen.blit(panel.bridge_number, (750, 668))
    screen.blit(panel.people_counter, (1030, 30))
    rivers.draw(screen)


    for first, second in yellow_line.fragments:
        draw_line(first, second, screen, YELLOW)
    for first, second in blue_line.fragments:
        draw_line(first, second, screen, BLUE)
    for first, second in red_line.fragments:
        draw_line(first, second, screen, RED)

    all_sprites.draw(screen)
    train_sprites.draw(screen)
    interface_sprites.draw(screen)
    if unfinished_line:
        pygame.draw.line(screen, RED, first_point, mouse_pos, width=10)


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
        if round(time()) - previous_time > stations.duration:
            previous_time = round(time())
            stations.generate_station()
            stations.draw()
            update()

        for el in all_sprites:
            el.update()
            if el.game_end:
                game_condition = 2
                frame_count = 0

        for el in train_sprites:
            if el.color == RED:
                if el.rect.centerx == red_points[index + sign][0] and el.rect.centery == red_points[index + sign][1]:
                    index += sign
                    el.rect.centerx, el.rect.centery = red_points[index]
                    if index == len(red_points) - 1:
                        sign = -1
                    elif index == 0:
                        sign = 1

                else:
                    ax, ay = red_points[index]
                    bx, by = red_points[index + sign]
                    dx, dy = (bx - ax, by - ay)
                    stepx, stepy = (dx // 36, dy // 36)
                    el.rect.centerx += stepx
                    el.rect.centery += stepy

        update()

    elif game_condition == 2:
        frame_count += 1
        people = panel.people_count
        screen.fill(BG_COLOR)
        screen.blit(BIG_MENU_FONT.render(f'Игра окончена',
                                         False, (255, 255, 255)), (200, 100))
        screen.blit(BIG_MENU_FONT.render(f'Ваш результат: {people}',
                                         False, (255, 255, 255)), (200, 190))
        con = sqlite3.connect("data/records.db")
        cur = con.cursor()
        result = cur.execute("SELECT record FROM records WHERE id == ?", [n]).fetchall()[0][0]
        if people > result:
            cur.execute("UPDATE records SET record = ? WHERE id == ?", [people, n])
        con.commit()
        con.close()
        if frame_count == 300:
            game_condition = 0
            flag = False
            index = 0
            n = 0
            frame_count = 0
            sign = 1
            previous_time = 0
            mouse_pos = (0, 0)
            red_lines = list()
            red_ends = [(0, 0), (0, 0)]
            drawing = False
            first_point = (0, 0)
            red_points = list()
            basic_rivers = list()
            unfinished_line = False

            rivers = pygame.sprite.Group()
            menu_sprites = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            interface_sprites = pygame.sprite.Group()
            train_sprites = pygame.sprite.Group()

            panel = Panel(interface_sprites)
            stations = Stations(all_sprites, 'maps/map_moscow.txt')

            moscow = Minimap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"))
            peter = Minimap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"))
            novgorod = Minimap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"))
            samara = Minimap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"))

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
                        path = ""
                        if n == 0:
                            path = 'maps/map_moscow.txt'
                        elif n == 1:
                            path = 'maps/map_peter.txt'
                        elif n == 2:
                            path = 'maps/map_novgorod.txt'
                        elif n == 3:
                            path = 'maps/map_samara.txt'

                        screen.fill(BG_COLOR)

                        board = Board(path)
                        board.load_map(rivers)
                        rivers.draw(screen)

                        for el in rivers:
                            if el.direction == 'basic':

                                basic_rivers.append(el)

                        stations = Stations(all_sprites, path)
                        stations.draw()
                        all_sprites.draw(screen)

                        screen.blit(panel.bridge_number, (750, 668))
                        screen.blit(panel.people_counter, (1030, 30))
                        interface_sprites.draw(screen)

                        previous_time = round(time())
                        records[n].x -= 18
                        records[n].y += 6

        elif game_condition == 1:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if panel.buttons[0].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(0)
                    else:
                        red_line.clear(panel, myfont)
                        stations.clear_color(1)
                    update()
                elif panel.buttons[1].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(1)
                    else:
                        yellow_line.clear(panel, myfont)
                        stations.clear_color(3)
                    update()
                elif panel.buttons[2].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(2)

                    else:
                        blue_line.clear(panel, myfont)
                        stations.clear_color(2)
                    update()

                for el in all_sprites:
                    if el.rect.collidepoint(mouse_pos):
                        first_point = tuple([el.rect.centerx, el.rect.centery])
                        drawing = True

            if event.type == MOUSEBUTTONUP and event.button == 1:

                mouse_pos = pygame.mouse.get_pos()
                if drawing:
                    for el in all_sprites:
                        if el.rect.collidepoint(mouse_pos):
                            second_point = (el.rect.centerx, el.rect.centery)
                            if panel.color == RED:
                                red_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      myfont)
                            elif panel.color == YELLOW:
                                yellow_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      myfont)
                            elif panel.color == BLUE:
                                blue_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      myfont)
                drawing = False
                update()
            if event.type == MOUSEMOTION:
                if drawing:
                    flag = False
                    if panel.color == RED and (first_point in red_line.ends or red_line.ends == [(0, 0), (0, 0)]):
                        flag = True
                    if panel.color == BLUE and (first_point in blue_line.ends or blue_line.ends == [(0, 0), (0, 0)]):
                        flag = True
                    if panel.color == YELLOW and (first_point in yellow_line.ends or yellow_line.ends == [(0, 0), (0, 0)]):
                        flag = True
                    if flag:
                        mouse_pos = pygame.mouse.get_pos()
                        update()
                        draw_line(first_point, mouse_pos, screen, panel.color)

        elif game_condition == 2:
            pass

    if game_condition == 0:
        screen.fill(BG_COLOR)
        screen.blit(BIG_MENU_FONT.render('MiniMetro', False, (255, 255, 255)), (400, 60))




    elif game_condition == 1:
        if round(time()) - previous_time > stations.duration:
            previous_time = round(time())
            stations.generate_station()
            # stations.draw()
            all_sprites.draw(screen)
    elif game_condition == 2:
        pass

    clock.tick(60)
    pygame.display.update()

