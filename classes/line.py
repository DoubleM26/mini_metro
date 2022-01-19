from classes.trains import *
from constants import *
from utils import *


class Line:
    def __init__(self, color):
        self.color = color
        self.ends = [(0, 0), (0, 0)]
        self.fragments = []
        self.dict = {1: RED, 3: YELLOW, 2: BLUE}
        self.points = list()
        self.index = 0
        self.sign = 1
        self.used_bridges = 0
    
    def set_ends(self, fp, sp, stations):
        if self.ends == [(0, 0), (0, 0)]:
            self.ends[0], self.ends[1] = fp, sp
            stations.colors[fp[1] // 36][fp[0] // 36].append(self.color)
        elif fp == self.ends[0]:
            self.ends[0] = sp
        elif fp == self.ends[1]:
            self.ends[1] = sp

    def add_point(self, group, fp, sp):
        if self.ends == [(0, 0), (0, 0)]:
            Train(group, fp[0], fp[1],
                  self.dict[self.color])
            self.points.append(fp)
            self.points.append(point(fp, sp))
            self.points.append(sp)
        if self.ends[0] == fp:
            self.points.insert(0, point(fp, sp))
            self.points.insert(0, sp)
            self.index += 2
        elif self.ends[1] == fp:
            self.points.append(point(fp, sp))
            self.points.append(sp)
    
    def add_fragment(self, fp, sp, stations, panel, basic_rivers, screen, group):
        if self.color in stations.colors[sp[1] // 36][sp[0] // 36]:
            return

        if self.ends[0] == fp or self.ends[1] == fp or self.ends == [(0, 0), (0, 0)]:
            for river in basic_rivers:
                if pygame.draw.line(screen, BG_COLOR, fp, sp) \
                        .colliderect(river):
                    if panel.bridges.bridge_count > 0:
                        self.add_point(group, fp, sp)

                        self.set_ends(fp, sp, stations)
                        self.fragments.append((fp, sp))
                        stations.colors[sp[1] // 36][sp[0] // 36].append(self.color)
                        panel.bridges.bridge_count -= 1
                        self.used_bridges += 1
                        panel.bridge_number = font.render(
                            str(panel.bridges.bridge_count), False, (255, 255, 255))
                    break
            else:
                self.add_point(group, fp, sp)

                self.set_ends(fp, sp, stations)
                stations.colors[sp[1] // 36][sp[0] // 36].append(self.color)
                self.fragments.append((fp, sp))

    def clear(self, panel):
        self.points = list()
        self.index = 0
        self.sign = 1
        self.ends = [(0, 0), (0, 0)]
        self.fragments = []
        panel.bridges.bridge_count += self.used_bridges
        self.used_bridges = 0
        panel.bridge_number = font.render(
            str(panel.bridges.bridge_count), False, (255, 255, 255))
