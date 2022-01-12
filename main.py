import sys
from board import Board
from pygame.locals import *
from stations import Stations
from main_menu import *
from time import time
from panel import Panel, myfont

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)

previous_time = 0
game_condition = 0
mouse_pos = (0, 0)
red_lines = list()
red_ends = [(0, 0), (0, 0)]
drawing = False
first_point = (0, 0)
points = list()
basic_rivers = list()

rivers = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()

panel = Panel(interface_sprites)
stations = Stations(all_sprites, 'maps/map_moscow.txt')

moscow = Minimap(menu_sprites, 200, 150, pygame.image.load("data/moscow.png"))
peter = Minimap(menu_sprites, 600, 150, pygame.image.load("data/saint_p.png"))
novgorod = Minimap(menu_sprites, 200, 450, pygame.image.load("data/novgorod.png"))
samara = Minimap(menu_sprites, 600, 450, pygame.image.load("data/samara.png"))


def update():
    screen.fill(BG_COLOR)
    screen.blit(panel.bridge_number, (750, 668))
    screen.blit(panel.locomotive_number, (430, 668))
    screen.blit(panel.people_counter, (1030, 30))
    rivers.draw(screen)

    for first, second in red_lines:
        pygame.draw.line(screen, RED, first, second, width=10)

    all_sprites.draw(screen)
    interface_sprites.draw(screen)


while True:
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
                        screen.blit(panel.locomotive_number, (430, 668))
                        screen.blit(panel.people_counter, (1030, 30))
                        interface_sprites.draw(screen)

                        previous_time = round(time())

        elif game_condition == 1:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if panel.buttons[0].rect.collidepoint(mouse_pos):
                    panel.trigger(0)
                    update()
                elif panel.buttons[1].rect.collidepoint(mouse_pos):
                    panel.trigger(1)
                    update()
                elif panel.buttons[2].rect.collidepoint(mouse_pos):
                    panel.trigger(2)
                    update()

                for el in all_sprites:
                    if el.rect.collidepoint(mouse_pos):
                        first_point = tuple([el.rect.centerx, el.rect.centery])
                        drawing = True

            if event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if drawing:
                    for el in all_sprites:
                        if el.rect.collidepoint(mouse_pos):
                            if panel.color == RED:
                                second_point = tuple([el.rect.centerx, el.rect.centery])
                                if second_point not in points:
                                    if red_ends == [(0, 0), (0, 0)]:
                                        for river in basic_rivers:
                                            if pygame.draw.line(screen, BG_COLOR, first_point, second_point) \
                                                    .colliderect(river):
                                                if panel.bridges.bridge_count > 0:
                                                    red_ends[0], red_ends[1] = first_point, second_point
                                                    red_lines.append(tuple([first_point, second_point]))
                                                    panel.bridges.bridge_count -= 1
                                                    points.append(second_point)
                                                    points.append(first_point)
                                                    panel.bridge_number = myfont.render(
                                                        str(panel.bridges.bridge_count), False, (255, 255, 255))
                                                break
                                        else:
                                            print('che')
                                            red_ends[0], red_ends[1] = first_point, second_point
                                            red_lines.append(tuple([first_point, second_point]))
                                            points.append(second_point)
                                            points.append(first_point)

                                    else:
                                        if first_point == red_ends[0]:
                                            for river in basic_rivers:
                                                if pygame.draw.line(screen, BG_COLOR, first_point, second_point)\
                                                        .colliderect(river):
                                                    if panel.bridges.bridge_count > 0:
                                                        red_ends[0] = second_point
                                                        red_lines.insert(0, tuple([first_point, second_point]))
                                                        panel.bridges.bridge_count -= 1
                                                        points.append(second_point)
                                                        panel.bridge_number = myfont.render(
                                                            str(panel.bridges.bridge_count), False, (255, 255, 255))
                                                    break
                                            else:
                                                red_ends[0] = second_point
                                                red_lines.insert(0, tuple([first_point, second_point]))
                                                points.append(second_point)

                                        elif first_point == red_ends[1]:
                                            for river in basic_rivers:
                                                if pygame.draw.line(screen, BG_COLOR, first_point, second_point)\
                                                        .colliderect(river):
                                                    if panel.bridges.bridge_count > 0:
                                                        red_ends[1] = second_point
                                                        red_lines.append(tuple([first_point, second_point]))
                                                        points.append(second_point)
                                                        panel.bridges.bridge_count -= 1
                                                        panel.bridge_number = myfont.render(
                                                            str(panel.bridges.bridge_count), False, (255, 255, 255))
                                                    break
                                            else:
                                                red_ends[1] = second_point
                                                red_lines.append(tuple([first_point, second_point]))
                                                points.append(second_point)
                drawing = False
                update()
            if event.type == MOUSEMOTION:
                if drawing:
                    mouse_pos = pygame.mouse.get_pos()
                    update()
                    pygame.draw.line(screen, RED, first_point, mouse_pos, width=10)

        elif game_condition == 2:
            pass

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
            all_sprites.draw(screen)
    elif game_condition == 2:
        pass

    clock.tick(60)
    pygame.display.update()
