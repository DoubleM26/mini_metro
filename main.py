import sys

from classes.board import Board
from pygame.locals import *
from classes.stations import Stations
from classes.main_menu import *
from time import time
from classes.panel import Panel
from utils import draw_line
from classes.line import Line
from db import DB

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)


flag = False
map_ind = 0
frame_count = 0
previous_time = [0, 0]
game_condition = 0
mouse_pos = (0, 0)


drawing = False

basic_rivers = list()
unfinished_line = False

rivers = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
stations_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
train_sprites = pygame.sprite.Group()
passengers_sprites = pygame.sprite.Group()


def set_overfilled(i):
    print(len(stations_sprites), i)
    if not list(stations_sprites)[i].overfilled:
        list(stations_sprites)[i].overfilled = True


panel = Panel(interface_sprites)
stations = Stations(stations_sprites, 'maps/map_moscow.txt', passengers_sprites, set_overfilled)
db = DB()
moscow = MiniMap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"), db, 0)
peter = MiniMap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"), db, 1)
novgorod = MiniMap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"), db, 2)
samara = MiniMap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"), db, 3)

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

    stations_sprites.draw(screen)
    train_sprites.draw(screen)
    interface_sprites.draw(screen)
    passengers_sprites.draw(screen)
    if flag:
        draw_line(first_point, mouse_pos, screen, panel.color)


while True:
    if game_condition == 0:
        screen.fill(BG_COLOR)
        screen.blit(BIG_MENU_FONT.render('MiniMetro', False, (255, 255, 255)), (400, 60))

        screen.blit(MAIN_MENU_FONT.render('Москва', False, (255, 255, 255)), (274, 340))
        screen.blit(MAIN_MENU_FONT.render('Санкт-Петербург', False, (255, 255, 255)), (599, 340))
        screen.blit(MAIN_MENU_FONT.render('Нижний Новгород', False, (255, 255, 255)), (190, 645))
        screen.blit(MAIN_MENU_FONT.render('Самара', False, (255, 255, 255)), (677, 645))

        menu_sprites.draw(screen)

        screen.blit(moscow.record_text, moscow.record_text_rect)
        screen.blit(peter.record_text, peter.record_text_rect)
        screen.blit(samara.record_text, samara.record_text_rect)
        screen.blit(novgorod.record_text, novgorod.record_text_rect)

        for n, el in enumerate(menu_sprites):
            if el.rect.collidepoint(mouse_pos):
                el.trigger()
            else:
                if el.triggered:
                    el.un_trigger()

    elif game_condition == 1:
        if round(time()) - previous_time[0] > stations.duration:
            previous_time[0] = round(time())
            stations.generate_station()
            # stations.draw()
            update()
        if round(time() * 10) - previous_time[1] > stations.passenger_duration:
            previous_time[1] = round(time() * 10)
            stations.generate_passenger()
            update()

        # if round(time()) - previous_time > stations.duration:

        for el in stations_sprites:
            el.update()
            if el.game_end:
                game_condition = 2
                frame_count = 0

        for el in train_sprites:
            if el.color == RED:
                if el.rect.centerx == red_line.points[red_line.index + red_line.sign][0] \
                        and el.rect.centery == red_line.points[red_line.index + red_line.sign][1] \
                        and el.stop_time < round(time()):
                    red_line.index += red_line.sign
                    if el.change_direction_cnt % 2 == 0:
                        el.stop_time = round(time()) + 1
                    # el.rect.centerx, el.rect.centery = red_line.points[red_line.index]
                    if red_line.index == len(red_line.points) - 1:
                        red_line.sign = -1
                    elif red_line.index == 0:
                        red_line.sign = 1
                    el.change_direction_cnt += 1
                elif el.stop_time >= round(time()):
                    pass
                else:
                    ax, ay = red_line.points[red_line.index]
                    bx, by = red_line.points[red_line.index + red_line.sign]
                    dx, dy = (bx - ax, by - ay)
                    stepx, stepy = (dx // 36, dy // 36)
                    el.rect.centerx += stepx
                    el.rect.centery += stepy
            elif el.color == YELLOW:
                if el.rect.centerx == yellow_line.points[yellow_line.index + yellow_line.sign][0] \
                        and el.rect.centery == yellow_line.points[yellow_line.index + yellow_line.sign][1] \
                        and el.stop_time < round(time()):
                    yellow_line.index += yellow_line.sign
                    if el.change_direction_cnt % 2 == 0:
                        el.stop_time = round(time()) + 1
                    el.rect.centerx, el.rect.centery = yellow_line.points[yellow_line.index]
                    if yellow_line.index == len(yellow_line.points) - 1:
                        yellow_line.sign = -1
                    elif yellow_line.index == 0:
                        yellow_line.sign = 1

                    el.change_direction_cnt += 1
                elif el.stop_time >= round(time()):
                    pass
                else:
                    ax, ay = yellow_line.points[yellow_line.index]
                    bx, by = yellow_line.points[yellow_line.index + yellow_line.sign]
                    dx, dy = (bx - ax, by - ay)
                    stepx, stepy = (dx // 36, dy // 36)
                    el.rect.centerx += stepx
                    el.rect.centery += stepy
            elif el.color == BLUE:
                if el.rect.centerx == blue_line.points[blue_line.index + blue_line.sign][0] \
                        and el.rect.centery == blue_line.points[blue_line.index + blue_line.sign][1] \
                        and el.stop_time < round(time()):
                    blue_line.index += blue_line.sign
                    if el.change_direction_cnt % 2 == 0:
                        el.stop_time = round(time()) + 1
                    el.rect.centerx, el.rect.centery = blue_line.points[blue_line.index]
                    if blue_line.index == len(blue_line.points) - 1:
                        blue_line.sign = -1
                    elif blue_line.index == 0:
                        blue_line.sign = 1

                    el.change_direction_cnt += 1
                elif el.stop_time >= round(time()):
                    pass
                else:
                    ax, ay = blue_line.points[blue_line.index]
                    bx, by = blue_line.points[blue_line.index + blue_line.sign]
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

        db.update_record(map_ind, people)
        db.get_records()
        if frame_count == 200:
            game_condition = 0
            flag = False
            red_line.index = 0
            map_ind = 0
            frame_count = 0
            previous_time = [0, 0]
            mouse_pos = (0, 0)

            drawing = False
            basic_rivers = list()
            unfinished_line = False

            rivers = pygame.sprite.Group()
            menu_sprites = pygame.sprite.Group()
            stations_sprites = pygame.sprite.Group()
            train_sprites = pygame.sprite.Group()
            interface_sprites = pygame.sprite.Group()
            train_sprites = pygame.sprite.Group()

            red_line.clear(panel)
            blue_line.clear(panel)
            yellow_line.clear(panel)
            panel = Panel(interface_sprites)

            stations = Stations(stations_sprites, 'maps/map_moscow.txt', passengers_sprites, set_overfilled)

            moscow = MiniMap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"), db, 0)
            peter = MiniMap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"), db, 1)
            novgorod = MiniMap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"), db, 2)
            samara = MiniMap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"), db, 3)

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
                            map_ind = 0
                        elif n == 1:
                            path = 'maps/map_peter.txt'
                            map_ind = 1
                        elif n == 2:
                            path = 'maps/map_novgorod.txt'
                            map_ind = 2
                        elif n == 3:
                            path = 'maps/map_samara.txt'
                            map_ind = 4

                        screen.fill(BG_COLOR)

                        board = Board(path)
                        board.load_map(rivers)
                        rivers.draw(screen)

                        for el in rivers:
                            if el.direction == 'basic':

                                basic_rivers.append(el)

                        stations = Stations(stations_sprites, path, passengers_sprites, set_overfilled)
                        stations.draw()
                        stations_sprites.draw(screen)

                        screen.blit(panel.bridge_number, (750, 668))
                        screen.blit(panel.people_counter, (1030, 30))
                        interface_sprites.draw(screen)

                        previous_time = [round(time()), round(time() * 10)]
                        # records[n].x -= 18
                        # records[n].y += 6

        elif game_condition == 1:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if panel.buttons[0].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(0)
                    else:
                        red_line.clear(panel)
                        for el in train_sprites:
                            if el.color == RED:
                                train_sprites.remove(el)
                        stations.clear_color(1)
                    update()
                elif panel.buttons[1].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(1)
                    else:
                        yellow_line.clear(panel)
                        for el in train_sprites:
                            if el.color == YELLOW:
                                train_sprites.remove(el)
                        stations.clear_color(3)
                    update()
                elif panel.buttons[2].rect.collidepoint(mouse_pos):
                    if event.button == 1:
                        panel.trigger(2)
                    else:
                        blue_line.clear(panel)
                        for el in train_sprites:
                            if el.color == BLUE:
                                train_sprites.remove(el)
                        stations.clear_color(2)
                    update()

                for el in stations_sprites:
                    if el.rect.collidepoint(mouse_pos):
                        first_point = tuple([el.rect.centerx, el.rect.centery])
                        drawing = True

            if event.type == MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if drawing:
                    for el in stations_sprites:
                        if el.rect.collidepoint(mouse_pos):
                            second_point = (el.rect.centerx, el.rect.centery)
                            if panel.color == RED:
                                red_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      train_sprites)
                            elif panel.color == YELLOW:
                                yellow_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      train_sprites)
                            elif panel.color == BLUE:
                                blue_line.add_fragment(first_point, second_point, stations, panel, basic_rivers, screen,
                                                      train_sprites)
                drawing = False
                flag = False
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

        elif game_condition == 2:
            pass

    clock.tick(40)
    pygame.display.update()

